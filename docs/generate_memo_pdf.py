"""Generate the two-page executive memo PDF for Phase 5."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "docs" / "memo.pdf"


PAGE1 = [
    "Decision Memo",
    "The Week 11 Path B judge materially improved Tenacious-Bench held-out performance over the Week 10 baseline, lifting the score from 0.4848 to 0.8633 for a Delta A gain of +0.3785 with a 95% confidence interval of [0.3487, 0.4084]. The trained judge also beat the prompt-only alternative by +0.1033 on the same held-out slice, while per-task cost increased from $0.0029 to $0.0047. Recommendation: deploy with caveat, using the judge as a gating or reranking layer for outbound drafts rather than as a fully autonomous commitment engine, because the quality lift is strong and statistically significant but the benchmark still under-covers some high-risk multi-turn edge cases.",
    "Key supporting facts: the ORPO LoRA run finished in 4.45 minutes on Colab, used 605 training pairs and 67 validation pairs, and ended at a final training loss of 2.2945 with validation loss 0.9481. Delta A passed the deployment threshold with p-value 0.0. Delta B was positive rather than merely neutral, which means the trained judge added measurable value beyond prompt engineering alone.",
    "Operational deployment note: treat cost growth as real but acceptable at the current lift level. The current economics add roughly $0.0018 per task compared with the baseline path, so the judge should first be inserted where a failed outbound message has the highest brand or pipeline cost rather than everywhere indiscriminately.",
]

PAGE2 = [
    "Skeptic's Appendix",
    "Failure modes still missing from Tenacious-Bench v0.1: (1) multi-turn pricing and contract negotiation where the right action is to defer rather than draft, (2) long-thread memory and continuity failures after multiple prior touches, (3) cross-channel behavior where email, LinkedIn, and human handoff interact, and (4) high-stakes partial-capacity cases where a prospect asks for a ramp shape rather than a simple yes/no commitment. A v0.2 benchmark should add explicit tasks for each of these.",
    "Public-signal lossiness remains a real limitation. Even grounded tasks only see the public footprint, which means hiring urgency, internal budget timing, and vendor constraints can still be hidden from the benchmark. The unresolved training failure is that the current adapter is much stronger on single-message judgment than on rich multi-turn decision quality, especially when a realistic answer should partially refuse, defer, or escalate.",
    "Kill-switch trigger: disable or bypass the trained judge if a seven-day rolling sample shows either repeated false approvals on unsupported capacity or a held-out-like monitored score drop of more than 10 percentage points from the current trained level. The judge should also be bypassed automatically for messages that imply contract value, multi-phase pricing, or any staffing commitment not directly supported by the structured capacity input.",
]


def build_story():
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "MemoTitle",
        parent=styles["Heading1"],
        fontSize=18,
        leading=22,
        spaceAfter=12,
    )
    body = ParagraphStyle(
        "MemoBody",
        parent=styles["BodyText"],
        fontSize=10.5,
        leading=14,
        spaceAfter=10,
    )
    story = []
    story.append(Paragraph(PAGE1[0], title))
    for para in PAGE1[1:]:
        story.append(Paragraph(para, body))
    story.append(PageBreak())
    story.append(Paragraph(PAGE2[0], title))
    for para in PAGE2[1:]:
        story.append(Paragraph(para, body))
    return story


def main() -> int:
    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=LETTER,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
    )
    doc.build(build_story())
    print(f"Wrote {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
