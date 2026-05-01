"""Upload Tenacious-Bench v0.1 to Hugging Face as a dataset repo."""

from __future__ import annotations

import argparse
import os
import shutil
import tempfile
from pathlib import Path

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT / "dataset"


def required_paths() -> list[Path]:
    return [
        DATASET_DIR / "README.md",
        DATASET_DIR / "datasheet.md",
        DATASET_DIR / "data_card.md",
        DATASET_DIR / "contamination_check.json",
        DATASET_DIR / "inter_rater_agreement.md",
        DATASET_DIR / "train" / "tasks.jsonl",
        DATASET_DIR / "dev" / "tasks.jsonl",
        DATASET_DIR / "held_out" / "tasks.jsonl",
    ]


def stage_repo(tmpdir: Path) -> None:
    shutil.copy2(DATASET_DIR / "README.md", tmpdir / "README.md")
    shutil.copy2(DATASET_DIR / "datasheet.md", tmpdir / "datasheet.md")
    shutil.copy2(DATASET_DIR / "data_card.md", tmpdir / "data_card.md")
    shutil.copy2(DATASET_DIR / "contamination_check.json", tmpdir / "contamination_check.json")
    shutil.copy2(DATASET_DIR / "inter_rater_agreement.md", tmpdir / "inter_rater_agreement.md")
    shutil.copy2(DATASET_DIR / "train" / "tasks.jsonl", tmpdir / "train.jsonl")
    shutil.copy2(DATASET_DIR / "dev" / "tasks.jsonl", tmpdir / "dev.jsonl")
    shutil.copy2(DATASET_DIR / "held_out" / "tasks.jsonl", tmpdir / "held_out.jsonl")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-id", default="abdulaziz0111/tenacious-bench-v0.1")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    load_dotenv(dotenv_path=ROOT / ".env")
    token = os.getenv("HUGGINGFACE_TOKEN")
    missing = [str(path.relative_to(ROOT)) for path in required_paths() if not path.exists()]
    if missing:
        raise SystemExit(f"Missing required dataset files: {missing}")

    if args.dry_run:
        print("Dataset upload dry run passed.")
        print(f"repo_id={args.repo_id}")
        print("staged_files=README.md,datasheet.md,data_card.md,contamination_check.json,inter_rater_agreement.md,train.jsonl,dev.jsonl,held_out.jsonl")
        print(f"token_present={bool(token)}")
        return 0

    try:
        from huggingface_hub import HfApi
    except ImportError as exc:
        raise SystemExit("huggingface_hub is required for dataset upload.") from exc

    if not token:
        raise SystemExit("HUGGINGFACE_TOKEN is missing from .env")

    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        stage_repo(tmpdir)
        api = HfApi(token=token)
        api.create_repo(repo_id=args.repo_id, repo_type="dataset", private=False, exist_ok=True)
        api.upload_folder(
            folder_path=str(tmpdir),
            repo_id=args.repo_id,
            repo_type="dataset",
        )
    print(f"Dataset uploaded: https://huggingface.co/datasets/{args.repo_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
