"""Verify required synthesis memos and key sections for Phase 6."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MEMO_DIR = ROOT / "synthesis_memos"

REQUIRED = {
    "synthetic_data_liu2024.md": ["Disagreement", "TRACE-", "PROBE-"],
    "datasheets_gebru2021.md": ["Disagreement", "Adaptation"],
    "contamination_chen2025.md": ["Disagreement", "modified", "0"],
    "llm_judge_gu2025.md": ["Disagreement", "3/5", "4/5"],
    "dpo_rafailov2023.md": ["Algorithm Choice", "ORPO", "DPO"],
    "simpo_or_orpo.md": ["SimPO", "ORPO", "pick"],
    "prometheus2_kim2024.md": ["Adaptation", "adopted", "changed"],
    "preference_leakage_li2025.md": ["Leakage-Prevention", "rotation", "No same-model"],
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> int:
    require(MEMO_DIR.exists(), "Missing synthesis_memos directory")
    for filename, markers in REQUIRED.items():
        path = MEMO_DIR / filename
        require(path.exists(), f"Missing memo: {filename}")
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            require(marker.lower() in text.lower(), f"{filename} missing marker: {marker}")
        word_count = len(text.split())
        require(word_count >= 120, f"{filename} too short ({word_count} words); likely summary-only.")

    print("Synthesis memo verification passed.")
    print(f"memos={len(REQUIRED)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
