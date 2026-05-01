"""Upload the final LoRA adapter and model card to Hugging Face."""

from __future__ import annotations

import argparse
import os
import shutil
import tempfile
from pathlib import Path

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
ADAPTER_DIR = ROOT / "training" / "adapter"
MODEL_CARD_PATH = ROOT / "training" / "model_card.md"

ALLOWED_FILES = [
    "adapter_config.json",
    "adapter_model.safetensors",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-id", default="abdulaziz0111/tenacious-judge-v0.1")
    parser.add_argument("--dataset-repo", default="abdulaziz0111/tenacious-bench-v0.1")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def build_readme(dataset_repo: str) -> str:
    body = MODEL_CARD_PATH.read_text(encoding="utf-8")
    link = f"\n\nDataset: https://huggingface.co/datasets/{dataset_repo}\n"
    return body + link


def main() -> int:
    args = parse_args()
    load_dotenv(dotenv_path=ROOT / ".env")
    token = os.getenv("HUGGINGFACE_TOKEN")

    missing = [name for name in ALLOWED_FILES if not (ADAPTER_DIR / name).exists()]
    if missing:
        raise SystemExit(f"Missing adapter files: {missing}")
    if not MODEL_CARD_PATH.exists():
        raise SystemExit("Missing training/model_card.md")

    if args.dry_run:
        print("Adapter upload dry run passed.")
        print(f"repo_id={args.repo_id}")
        print(f"dataset_repo={args.dataset_repo}")
        print(f"token_present={bool(token)}")
        print(f"allowed_files={','.join(ALLOWED_FILES)}")
        return 0

    try:
        from huggingface_hub import HfApi
    except ImportError as exc:
        raise SystemExit("huggingface_hub is required for adapter upload.") from exc

    if not token:
        raise SystemExit("HUGGINGFACE_TOKEN is missing from .env")

    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        for name in ALLOWED_FILES:
            shutil.copy2(ADAPTER_DIR / name, tmpdir / name)
        (tmpdir / "README.md").write_text(build_readme(args.dataset_repo), encoding="utf-8")
        api = HfApi(token=token)
        api.create_repo(repo_id=args.repo_id, repo_type="model", private=False, exist_ok=True)
        api.upload_folder(folder_path=str(tmpdir), repo_id=args.repo_id, repo_type="model")

    print(f"Adapter uploaded: https://huggingface.co/{args.repo_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
