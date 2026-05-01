"""Train the Path B Tenacious judge with ORPO on preference pairs.

This script is intended to run on a GPU runtime such as Google Colab T4.
Use `--dry-run` locally to validate config, data loading, and output paths.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PREFERENCE_PAIRS_PATH = ROOT / "training" / "preference_pairs.jsonl"
ADAPTER_DIR = ROOT / "training" / "adapter"
LATEST_LOG_PATH = ROOT / "training" / "training_run.log"

BACKBONE = os.getenv("TENACIOUS_BACKBONE", "unsloth/Qwen2.5-0.5B-Instruct")
LORA_RANK = 16
LORA_ALPHA = 32
LEARNING_RATE = 5e-5
BATCH_SIZE = 2
GRADIENT_ACCUMULATION_STEPS = 4
NUM_EPOCHS = 2
SEED = 42
TRAINING_METHOD = "ORPO"
MAX_SEQ_LENGTH = 2048


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def build_examples(rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    return [
        {
            "prompt": row["prompt"],
            "chosen": row["chosen"],
            "rejected": row["rejected"],
        }
        for row in rows
    ]


def split_examples(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    shuffled = list(rows)
    random.Random(SEED).shuffle(shuffled)
    eval_size = max(32, round(len(shuffled) * 0.1))
    eval_rows = shuffled[:eval_size]
    train_rows = shuffled[eval_size:]
    return train_rows, eval_rows


def ensure_dirs() -> None:
    ADAPTER_DIR.mkdir(parents=True, exist_ok=True)


def write_log(log: dict[str, Any], run_id: str) -> Path:
    run_log_path = ROOT / "training" / f"training_run_{run_id}_seed{SEED}.log"
    text = json.dumps(log, indent=2)
    run_log_path.write_text(text, encoding="utf-8")
    LATEST_LOG_PATH.write_text(text, encoding="utf-8")
    return run_log_path


def latest_metric(history: list[dict[str, Any]], key: str) -> float | None:
    for entry in reversed(history):
        if key in entry:
            return float(entry[key])
    return None


def training_curve(history: list[dict[str, Any]]) -> list[dict[str, Any]]:
    curve = []
    for entry in history:
        if "loss" in entry or "eval_loss" in entry:
            curve.append(
                {
                    "step": entry.get("step"),
                    "loss": entry.get("loss"),
                    "eval_loss": entry.get("eval_loss"),
                    "epoch": entry.get("epoch"),
                }
            )
    return curve


def push_adapter_if_requested(repo_id: str | None) -> str | None:
    if not repo_id:
        return None
    try:
        from huggingface_hub import HfApi
    except ImportError as exc:
        raise SystemExit("huggingface_hub is required for --push-repo.") from exc

    api = HfApi()
    api.create_repo(repo_id=repo_id, repo_type="model", exist_ok=True)
    api.upload_folder(folder_path=str(ADAPTER_DIR), repo_id=repo_id, repo_type="model")
    return f"https://huggingface.co/{repo_id}"


def run_training(push_repo: str | None) -> int:
    try:
        import unsloth  # noqa: F401
        import torch
        from datasets import Dataset, DatasetDict
        from trl import ORPOConfig, ORPOTrainer
        from unsloth import FastLanguageModel
    except ImportError as exc:
        raise SystemExit(
            "Missing training dependencies. Install unsloth, trl, datasets, torch in Colab first."
        ) from exc

    rows = read_jsonl(PREFERENCE_PAIRS_PATH)
    examples = build_examples(rows)
    train_rows, eval_rows = split_examples(examples)

    torch.manual_seed(SEED)
    random.seed(SEED)
    start_time = time.time()
    run_id = f"{TRAINING_METHOD.lower()}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=BACKBONE,
        max_seq_length=MAX_SEQ_LENGTH,
        load_in_4bit=False,
    )
    model = FastLanguageModel.get_peft_model(
        model,
        r=LORA_RANK,
        lora_alpha=LORA_ALPHA,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        lora_dropout=0.05,
        bias="none",
    )

    dataset = DatasetDict(
        {
            "train": Dataset.from_list(train_rows),
            "dev": Dataset.from_list(eval_rows),
        }
    )
    args = ORPOConfig(
        output_dir=str(ADAPTER_DIR),
        num_train_epochs=NUM_EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=GRADIENT_ACCUMULATION_STEPS,
        learning_rate=LEARNING_RATE,
        seed=SEED,
        logging_steps=5,
        eval_strategy="epoch",
        save_strategy="epoch",
        report_to=[],
    )
    trainer = ORPOTrainer(
        model=model,
        args=args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["dev"],
        processing_class=tokenizer,
    )
    trainer.train()

    total_minutes = round((time.time() - start_time) / 60, 2)
    history = trainer.state.log_history
    final_train_loss = latest_metric(history, "train_loss")
    if final_train_loss is None:
        final_train_loss = latest_metric(history, "loss")
    final_eval_loss = latest_metric(history, "eval_loss")

    ensure_dirs()
    model.save_pretrained(str(ADAPTER_DIR))
    tokenizer.save_pretrained(str(ADAPTER_DIR))

    hf_url = push_adapter_if_requested(push_repo)
    log = {
        "run_id": run_id,
        "backbone": BACKBONE,
        "lora_rank": LORA_RANK,
        "lora_alpha": LORA_ALPHA,
        "learning_rate": LEARNING_RATE,
        "batch_size": BATCH_SIZE,
        "gradient_accumulation_steps": GRADIENT_ACCUMULATION_STEPS,
        "training_method": TRAINING_METHOD,
        "num_epochs": NUM_EPOCHS,
        "seed": SEED,
        "max_seq_length": MAX_SEQ_LENGTH,
        "total_wall_time_minutes": total_minutes,
        "training_pairs_used": len(train_rows),
        "validation_pairs_used": len(eval_rows),
        "final_train_loss": round(float(final_train_loss or 0.0), 4),
        "final_val_loss": round(float(final_eval_loss or 0.0), 4),
        "loss_curve": training_curve(history),
        "adapter_dir": str(ADAPTER_DIR.relative_to(ROOT)),
        "huggingface_url": hf_url,
    }
    run_log_path = write_log(log, run_id)
    print(f"Training complete. Log saved to {run_log_path}")
    if hf_url:
        print(f"Adapter pushed to {hf_url}")
    return 0


def dry_run() -> int:
    rows = read_jsonl(PREFERENCE_PAIRS_PATH)
    examples = build_examples(rows)
    train_rows, eval_rows = split_examples(examples)
    ensure_dirs()
    print("Dry run passed.")
    print(f"backbone={BACKBONE}")
    print(f"training_method={TRAINING_METHOD}")
    print(f"seed={SEED}")
    print(f"train_pairs={len(train_rows)}")
    print(f"eval_pairs={len(eval_rows)}")
    print(f"adapter_dir={ADAPTER_DIR}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Validate config and dataset without training.")
    parser.add_argument("--push-repo", default=None, help="Optional Hugging Face repo id, e.g. user/tenacious-judge-adapter")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.dry_run:
        return dry_run()
    return run_training(args.push_repo)


if __name__ == "__main__":
    raise SystemExit(main())
