"""Verify Phase 5 community and executive memo artifacts."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "docs" / "community_engagement.md"
MEMO = ROOT / "docs" / "memo.pdf"
EVIDENCE = ROOT / "docs" / "evidence_graph.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def page_count(pdf_path: Path) -> int:
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        from pypdf import PdfReader
    reader = PdfReader(str(pdf_path))
    return len(reader.pages)


def main() -> int:
    require(COMMUNITY.exists(), "Missing docs/community_engagement.md")
    require(MEMO.exists(), "Missing docs/memo.pdf")
    require(EVIDENCE.exists(), "Missing docs/evidence_graph.json")

    community_text = COMMUNITY.read_text(encoding="utf-8")
    require("Submission Type" in community_text, "Community engagement doc missing submission type")
    require("Public URL" in community_text, "Community engagement doc missing public URL field")
    require("https://huggingface.co/datasets/abdulaziz0111/tenacious-bench-v0.1" in community_text, "Community engagement doc must link the dataset")

    require(page_count(MEMO) == 2, "memo.pdf must be exactly 2 pages")

    graph = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    require("claims" in graph and len(graph["claims"]) >= 10, "Evidence graph must have claim mappings")

    print("Phase 5 executive artifact verification passed.")
    print(f"memo_pages={page_count(MEMO)}")
    print(f"evidence_claims={len(graph['claims'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
