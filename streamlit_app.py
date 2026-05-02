"""Streamlit dashboard for Week 11/Phase 6 delivery artifacts."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import streamlit as st


ROOT = Path(__file__).resolve().parent
PHASE_CHECKS = {
    "Phase 1 - Audit & Schema": {
        "script": "tests/verify_audit_phase.py",
        "artifacts": [
            "audit/audit_memo.md",
            "audit/schema.json",
            "audit/scoring_evaluator.py",
        ],
    },
    "Phase 2 - Dataset Authoring": {
        "script": "tests/verify_dataset_authoring.py",
        "artifacts": [
            "dataset/train/tasks.jsonl",
            "dataset/dev/tasks.jsonl",
            "dataset/held_out/tasks.jsonl",
            "dataset/contamination_check.json",
        ],
    },
    "Phase 3 - Training Data Prep": {
        "script": "tests/verify_training_prep.py",
        "artifacts": [
            "training/preference_pairs.jsonl",
            "training/leakage_prevention_log.md",
            "training/train_contamination_check.json",
        ],
    },
    "Phase 4 - Train/Ablate/Measure": {
        "script": "tests/verify_phase4_scaffold.py",
        "artifacts": [
            "training/training_run.log",
            "training/adapter/adapter_config.json",
            "training/adapter/adapter_model.safetensors",
            "ablations/ablation_results.json",
            "ablations/held_out_traces.jsonl",
        ],
    },
    "Phase 5 - Publish & Engage": {
        "script": "tests/verify_phase5_publish.py",
        "artifacts": [
            "dataset/README.md",
            "dataset/hf_upload.py",
            "training/hf_push_adapter.py",
            "docs/blog_post.md",
        ],
    },
    "Phase 6 - Synthesis Memos": {
        "script": "tests/verify_synthesis_memos.py",
        "artifacts": [
            "synthesis_memos/synthetic_data_liu2024.md",
            "synthesis_memos/dpo_rafailov2023.md",
            "synthesis_memos/preference_leakage_li2025.md",
        ],
    },
}


def read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl_count(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def file_exists(path: Path) -> bool:
    return path.exists()


def run_verify(script: str) -> tuple[int, str]:
    cmd = [sys.executable, str(ROOT / script)]
    completed = subprocess.run(cmd, capture_output=True, text=True)
    output = (completed.stdout + "\n" + completed.stderr).strip()
    return completed.returncode, output


def status_chip(ok: bool, label: str) -> None:
    if ok:
        st.success(f"{label}: PASS")
    else:
        st.error(f"{label}: FAIL")


def section_title(label: str) -> None:
    st.markdown(f"### {label}")


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: #f7fafc;
            color: #0f172a;
        }
        [data-testid="stAppViewContainer"] {
            background: #f7fafc;
        }
        [data-testid="stHeader"] {
            background: rgba(247, 250, 252, 0.92);
        }
        [data-testid="stSidebar"] {
            background: #ffffff;
        }
        p, li, span, label, div {
            color: #0f172a;
        }
        .hero-card {
            border-radius: 18px;
            padding: 1rem 1.2rem;
            margin-bottom: 0.6rem;
            background: #ffffff;
            color: #0f172a;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.18);
            border: 1px solid #dbe3ee;
        }
        .hero-title {
            font-size: 1.35rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
            color: #0f172a !important;
        }
        .hero-sub {
            font-size: 0.95rem;
            opacity: 0.95;
            color: #334155 !important;
        }
        .phase-chip {
            display: inline-block;
            margin: 0.2rem 0.25rem 0.2rem 0;
            padding: 0.2rem 0.6rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 600;
            background: #dbeafe;
            color: #1e3a8a;
            border: 1px solid #bfdbfe;
        }
        [data-testid="stMetricValue"] {
            color: #0f172a;
        }
        [data-testid="stMetricLabel"] {
            color: #334155;
        }
        .stButton button {
            border-radius: 10px;
            border: 1px solid #cbd5e1;
            color: #0f172a;
            background: #ffffff;
        }
        .stButton button:hover {
            border-color: #93c5fd;
            background: #f8fbff;
            color: #0b3a66;
        }
        .stDownloadButton button {
            border-radius: 10px;
            background: #0b3a66;
            color: #ffffff;
            border: 1px solid #0b3a66;
        }
        .stDownloadButton button:hover {
            background: #dbeafe;
            border-color: #93c5fd;
            color: #0b3a66;
        }
        /* Dropdown controls and menu options */
        div[data-baseweb="select"] > div {
            background: #3b0764 !important;
            border-color: #6d28d9 !important;
            color: #ffffff !important;
        }
        div[data-baseweb="select"] * {
            color: #ffffff !important;
        }
        /* Ensure selected value, placeholder, tags, and input text are white */
        div[data-baseweb="select"] span,
        div[data-baseweb="select"] div,
        div[data-baseweb="select"] input,
        div[data-baseweb="select"] p {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        div[data-baseweb="select"] input::placeholder {
            color: #d1d5db !important;
            -webkit-text-fill-color: #d1d5db !important;
        }
        div[role="listbox"] {
            background: #ffffff !important;
            color: #0b3a66 !important;
            border: 1px solid #94a3b8 !important;
        }
        /* Force all dropdown popover panels to white */
        [data-baseweb="popover"] {
            background: #ffffff !important;
            color: #0b3a66 !important;
        }
        [data-baseweb="popover"] * {
            background-color: #ffffff !important;
            color: #0b3a66 !important;
        }
        div[role="option"] {
            background: #ffffff !important;
            color: #0b3a66 !important;
            font-weight: 600 !important;
        }
        div[role="option"][aria-selected="true"] {
            background: #dbeafe !important;
            color: #1e3a8a !important;
        }
        div[role="option"][aria-selected="true"] * {
            color: #1e3a8a !important;
        }
        div[role="option"]:hover {
            background: #eaf2ff !important;
            color: #1e3a8a !important;
        }
        div[role="option"]:hover * {
            color: #1e3a8a !important;
        }
        /* Light hover for expanders/dropdowns to avoid dark unreadable states */
        details summary:hover,
        [data-testid="stExpander"] summary:hover,
        [data-baseweb="menu"] [role="option"]:hover,
        [data-baseweb="popover"] [role="option"]:hover {
            background: #eef6ff !important;
            color: #0b3a66 !important;
        }
        details summary:hover *,
        [data-testid="stExpander"] summary:hover *,
        [data-baseweb="menu"] [role="option"]:hover *,
        [data-baseweb="popover"] [role="option"]:hover * {
            color: #0b3a66 !important;
        }
        div[role="option"] *,
        div[role="listbox"] * {
            color: #0b3a66 !important;
        }
        textarea, .stTextArea textarea {
            background: #111827 !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            border: 1px solid #374151 !important;
        }
        [data-testid="stTextArea"] label,
        [data-testid="stTextArea"] p,
        [data-testid="stTextArea"] span,
        [data-testid="stTextArea"] div {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        [data-testid="stCodeBlock"] {
            background: #111827 !important;
            color: #ffffff !important;
            border: 1px solid #374151 !important;
            border-radius: 10px;
        }
        [data-testid="stCodeBlock"] pre,
        [data-testid="stCodeBlock"] code {
            background: #111827 !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        [data-testid="stCodeBlock"] *,
        pre, code {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        [data-testid="stJson"] {
            background: #111827 !important;
            border: 1px solid #374151 !important;
            border-radius: 10px;
            padding: 0.35rem;
        }
        [data-testid="stJson"],
        [data-testid="stJson"] * {
            color: #f9fafb !important;
            -webkit-text-fill-color: #f9fafb !important;
        }
        .summary-card {
            background: #111827;
            color: #f9fafb;
            border: 1px solid #374151;
            border-radius: 12px;
            padding: 0.75rem 0.9rem;
            margin-top: 0.4rem;
        }
        .summary-card,
        .summary-card * {
            color: #f9fafb !important;
            -webkit-text-fill-color: #f9fafb !important;
        }
        .result-console {
            background: #0f172a;
            color: #ffffff;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 0.75rem 0.9rem;
            white-space: pre-wrap;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            font-size: 0.84rem;
            line-height: 1.45;
            margin-top: 0.35rem;
            margin-bottom: 0.35rem;
        }
        .result-console,
        .result-console * {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        .result-console a,
        .summary-card a,
        [data-testid="stJson"] a {
            color: #ffffff !important;
            text-decoration: underline !important;
        }
        /* Safety net: if any component is rendered on dark background, force readable text */
        [style*="background: #111827"],
        [style*="background-color: #111827"],
        [style*="background:#111827"],
        [style*="background: #0f172a"],
        [style*="background-color: #0f172a"],
        [style*="background:#0f172a"] {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        [style*="background: #111827"] *,
        [style*="background-color: #111827"] *,
        [style*="background:#111827"] *,
        [style*="background: #0f172a"] *,
        [style*="background-color: #0f172a"] *,
        [style*="background:#0f172a"] * {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        .demo-card {
            background: #ffffff;
            border: 1px solid #dbe3ee;
            border-radius: 12px;
            padding: 0.75rem 0.9rem;
            margin-top: 0.4rem;
            margin-bottom: 0.6rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_phase_chips() -> None:
    chips = "".join([f"<span class='phase-chip'>{name}</span>" for name in PHASE_CHECKS.keys()])
    st.markdown(chips, unsafe_allow_html=True)


DEMO_STEPS = [
    {
        "title": "Step 1 - Project Overview",
        "goal": "Introduce the Week 11 objective and show headline metrics.",
        "show": "Use Phase Overview cards: Delta A, p-value, Delta B, and cost delta.",
        "files": ["README.md", "ablations/ablation_results.json"],
    },
    {
        "title": "Step 2 - Audit and Schema",
        "goal": "Show that Tenacious-specific gaps are documented and machine-gradable.",
        "show": "Run Phase 1 verification and preview audit/schema files.",
        "files": ["audit/audit_memo.md", "audit/schema.json", "audit/scoring_evaluator.py"],
    },
    {
        "title": "Step 3 - Dataset Authoring",
        "goal": "Show partitioned dataset quality and contamination checks.",
        "show": "Run Phase 2 verification, then show task counts and contamination panel.",
        "files": ["dataset/train/tasks.jsonl", "dataset/dev/tasks.jsonl", "dataset/held_out/tasks.jsonl", "dataset/contamination_check.json"],
    },
    {
        "title": "Step 4 - Training Data Prep",
        "goal": "Show preference pairs and leakage prevention for Path B.",
        "show": "Run Phase 3 verification and show pair count + contamination zeroes.",
        "files": ["training/preference_pairs.jsonl", "training/leakage_prevention_log.md", "training/train_contamination_check.json"],
    },
    {
        "title": "Step 5 - Training Run",
        "goal": "Show actual ORPO run config and losses.",
        "show": "Open Training tab and show hyperparameters + loss curve from training_run.log.",
        "files": ["training/train.py", "training/training_run.log", "training/adapter/adapter_config.json", "training/adapter/adapter_model.safetensors"],
    },
    {
        "title": "Step 6 - Ablation Results",
        "goal": "Show Delta A significance, Delta B honesty, and cost tradeoff.",
        "show": "Open Ablations tab and highlight JSON entries + deployment gate pass.",
        "files": ["ablations/ablation_results.json", "ablations/cost_pareto.json", "ablations/held_out_traces.jsonl"],
    },
    {
        "title": "Step 7 - Publish Artifacts",
        "goal": "Show public Hugging Face dataset/model links and publish readiness.",
        "show": "Open Publish panel links and run Phase 5 publish verifier.",
        "files": ["dataset/hf_upload.py", "training/hf_push_adapter.py", "dataset/README.md", "training/model_card.md"],
        "links": [
            "https://huggingface.co/datasets/abdulaziz0111/tenacious-bench-v0.1",
            "https://huggingface.co/abdulaziz0111/tenacious-judge-v0.1",
        ],
    },
    {
        "title": "Step 8 - Community and Executive Artifacts",
        "goal": "Show community engagement file, 2-page memo, and evidence graph.",
        "show": "Run Phase 5 executive verifier and preview docs artifacts.",
        "files": ["docs/community_engagement.md", "docs/memo.pdf", "docs/evidence_graph.json"],
    },
    {
        "title": "Step 9 - Synthesis Memos",
        "goal": "Show all 8 memos include disagreement/adaptation evidence.",
        "show": "Run Phase 6 verifier and preview memo list.",
        "files": ["synthesis_memos/synthetic_data_liu2024.md", "synthesis_memos/simpo_or_orpo.md", "synthesis_memos/preference_leakage_li2025.md"],
    },
]


def build_demo_report(metrics: dict[str, Any]) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    ab = metrics.get("ablation", {})
    da = ab.get("delta_a", {})
    db = ab.get("delta_b", {})
    cp = ab.get("cost_pareto", {})
    tr = metrics.get("training_log", {})
    lines = [
        "# Tenacious Week 11 Demo Report",
        "",
        f"Generated: {stamp}",
        "",
        "## Headline Metrics",
        f"- Delta A: {da.get('delta', 0):+.4f}",
        f"- Delta A p-value: {da.get('p_value', 1):.4f}",
        f"- Delta B: {db.get('delta', 0):+.4f}",
        f"- Cost per task baseline: ${cp.get('cost_per_task_baseline', 0):.4f}",
        f"- Cost per task with judge: ${cp.get('cost_per_task_with_judge', 0):.4f}",
        "",
        "## Training Summary",
        f"- Run ID: {tr.get('run_id', 'N/A')}",
        f"- Backbone: {tr.get('backbone', 'N/A')}",
        f"- Training method: {tr.get('training_method', 'N/A')}",
        f"- Training pairs used: {tr.get('training_pairs_used', 'N/A')}",
        f"- Validation pairs used: {tr.get('validation_pairs_used', 'N/A')}",
        f"- Final train loss: {tr.get('final_train_loss', 'N/A')}",
        f"- Final val loss: {tr.get('final_val_loss', 'N/A')}",
        "",
        "## Phase Status",
    ]
    phase_results = st.session_state.get("phase_results", {})
    for phase_name, config in PHASE_CHECKS.items():
        result = phase_results.get(phase_name)
        if result is None:
            state = "NOT RUN"
        else:
            state = "PASS" if result["code"] == 0 else f"FAIL (exit {result['code']})"
        lines.append(f"- {phase_name}: {state}")
        for rel in config["artifacts"]:
            lines.append(f"  - {rel}: {'yes' if file_exists(ROOT / rel) else 'no'}")
    lines += [
        "",
        "## Publish Links",
        "- Dataset: https://huggingface.co/datasets/abdulaziz0111/tenacious-bench-v0.1",
        "- Model: https://huggingface.co/abdulaziz0111/tenacious-judge-v0.1",
    ]
    return "\n".join(lines)


def preview_text(path: Path, max_chars: int = 900) -> str:
    if not path.exists():
        return f"(missing) {path.relative_to(ROOT)}"
    text = path.read_text(encoding="utf-8", errors="ignore")
    return text[:max_chars] + ("\n..." if len(text) > max_chars else "")


def render_result_console(output: str) -> None:
    safe_output = (output or "(no output)").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    st.markdown(f"<div class='result-console'>{safe_output}</div>", unsafe_allow_html=True)


def render_artifact_buttons(step_files: list[str], step_idx: int) -> None:
    if not step_files:
        st.info("No artifacts configured for this step.")
        return
    for i, rel in enumerate(step_files):
        p = ROOT / rel
        b1, b2 = st.columns([4, 1])
        with b1:
            if st.button(f"Open: {rel}", key=f"open_artifact_{step_idx}_{i}", use_container_width=True):
                if not p.exists():
                    st.error(f"Missing file: {rel}")
                else:
                    ext = p.suffix.lower()
                    if ext in {".json"}:
                        data = read_json(p)
                        if data is None:
                            st.code(preview_text(p), language="text")
                        else:
                            st.json(data, expanded=False)
                    elif ext in {".jsonl"}:
                        st.code(preview_text(p, max_chars=2200), language="json")
                    elif ext in {".md", ".py", ".txt", ".log"}:
                        lang = "python" if ext == ".py" else "markdown" if ext == ".md" else "text"
                        st.code(preview_text(p, max_chars=2200), language=lang)
                    else:
                        st.write(f"Preview not supported for `{ext}`. File exists at `{rel}`.")
        with b2:
            status_chip(p.exists(), "exists")


def render_demo_snapshot(step_title: str, metrics: dict[str, Any]) -> None:
    st.markdown("**Live demo content**")
    st.markdown("<div class='demo-card'>", unsafe_allow_html=True)

    if step_title == "Step 1 - Project Overview":
        da = metrics.get("ablation", {}).get("delta_a", {})
        db = metrics.get("ablation", {}).get("delta_b", {})
        cp = metrics.get("ablation", {}).get("cost_pareto", {})
        c1, c2, c3 = st.columns(3)
        c1.metric("Delta A", f"{da.get('delta', 0):+.4f}")
        c2.metric("Delta B", f"{db.get('delta', 0):+.4f}")
        c3.metric("Cost Δ/task", f"${(cp.get('cost_per_task_with_judge', 0) - cp.get('cost_per_task_baseline', 0)):.4f}")
    elif step_title == "Step 2 - Audit and Schema":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("`audit/audit_memo.md` preview")
            st.code(preview_text(ROOT / "audit" / "audit_memo.md"), language="markdown")
        with col2:
            st.markdown("`audit/schema.json` key fields")
            schema = read_json(ROOT / "audit" / "schema.json") or {}
            st.write(
                {
                    "name": schema.get("name"),
                    "version": schema.get("version"),
                    "example_count": len(schema.get("examples", [])),
                    "difficulty_levels": schema.get("fields", {}).get("difficulty", []),
                }
            )
    elif step_title == "Step 3 - Dataset Authoring":
        c1, c2, c3 = st.columns(3)
        c1.metric("Train", read_jsonl_count(ROOT / "dataset" / "train" / "tasks.jsonl"))
        c2.metric("Dev", read_jsonl_count(ROOT / "dataset" / "dev" / "tasks.jsonl"))
        c3.metric("Held-out", read_jsonl_count(ROOT / "dataset" / "held_out" / "tasks.jsonl"))
        contam = read_json(ROOT / "dataset" / "contamination_check.json") or {}
        st.write(
            {
                "dataset_ngram_violations": len(contam.get("ngram_violations", [])),
                "dataset_embedding_violations": len(contam.get("embedding_violations", [])),
                "timeshift_verified": contam.get("timeshift_verified"),
            }
        )
    elif step_title == "Step 4 - Training Data Prep":
        contam = metrics.get("train_contam", {})
        st.metric("Preference Pairs", read_jsonl_count(ROOT / "training" / "preference_pairs.jsonl"))
        st.write(
            {
                "held_out_ngram_violations": len(contam.get("training_vs_held_out", {}).get("ngram_violations", [])),
                "held_out_embedding_violations": len(contam.get("training_vs_held_out", {}).get("embedding_violations", [])),
            }
        )
        st.markdown("`training/leakage_prevention_log.md` preview")
        st.code(preview_text(ROOT / "training" / "leakage_prevention_log.md"), language="markdown")
    elif step_title == "Step 5 - Training Run":
        log = metrics.get("training_log", {})
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Method", str(log.get("training_method", "N/A")))
        c2.metric("Backbone", str(log.get("backbone", "N/A")))
        c3.metric("Train Loss", str(log.get("final_train_loss", "N/A")))
        c4.metric("Val Loss", str(log.get("final_val_loss", "N/A")))
        curve = log.get("loss_curve", [])
        rows = []
        for row in curve:
            if row.get("loss") is not None:
                rows.append({"step": row.get("step"), "loss": row.get("loss"), "type": "train"})
            if row.get("eval_loss") is not None:
                rows.append({"step": row.get("step"), "loss": row.get("eval_loss"), "type": "eval"})
        if rows:
            st.line_chart(rows, x="step", y="loss", color="type")
    elif step_title == "Step 6 - Ablation Results":
        da = metrics.get("ablation", {}).get("delta_a", {})
        db = metrics.get("ablation", {}).get("delta_b", {})
        cp = metrics.get("ablation", {}).get("cost_pareto", {})
        c1, c2, c3 = st.columns(3)
        c1.metric("Delta A", f"{da.get('delta', 0):+.4f}")
        c2.metric("95% CI", f"[{da.get('95_ci', [0,0])[0]:.4f}, {da.get('95_ci', [0,0])[1]:.4f}]")
        c3.metric("p-value", f"{da.get('p_value', 1):.4f}")
        st.write(
            {
                "delta_b": db.get("delta"),
                "cost_baseline": cp.get("cost_per_task_baseline"),
                "cost_with_judge": cp.get("cost_per_task_with_judge"),
            }
        )
    elif step_title == "Step 7 - Publish Artifacts":
        st.link_button("Open Dataset Page", "https://huggingface.co/datasets/abdulaziz0111/tenacious-bench-v0.1")
        st.link_button("Open Model Page", "https://huggingface.co/abdulaziz0111/tenacious-judge-v0.1")
        st.markdown("`dataset/README.md` preview")
        st.code(preview_text(ROOT / "dataset" / "README.md"), language="markdown")
    elif step_title == "Step 8 - Community and Executive Artifacts":
        st.markdown("`docs/community_engagement.md` preview")
        st.code(preview_text(ROOT / "docs" / "community_engagement.md"), language="markdown")
        evidence = read_json(ROOT / "docs" / "evidence_graph.json") or {"claims": []}
        st.metric("Evidence Claims", len(evidence.get("claims", [])))
        st.write({"memo_pdf_exists": file_exists(ROOT / "docs" / "memo.pdf")})
    elif step_title == "Step 9 - Synthesis Memos":
        memo_dir = ROOT / "synthesis_memos"
        files = sorted([p.name for p in memo_dir.glob("*.md")]) if memo_dir.exists() else []
        st.metric("Memo Count", len(files))
        st.write(files)
        if files:
            st.markdown("Sample memo preview")
            st.code(preview_text(memo_dir / files[0]), language="markdown")

    st.markdown("</div>", unsafe_allow_html=True)


def guided_demo_panel(metrics: dict[str, Any]) -> None:
    section_title("Guided Video Demo")
    st.caption("Use this sequence while recording: click Next Step and run the suggested verifier/action.")

    if "demo_step_idx" not in st.session_state:
        st.session_state["demo_step_idx"] = 0

    current = st.session_state["demo_step_idx"]
    total = len(DEMO_STEPS)
    step = DEMO_STEPS[current]

    c1, c2, c3, c4 = st.columns([1, 1, 1, 2])
    with c1:
        if st.button("Previous Step") and current > 0:
            st.session_state["demo_step_idx"] = current - 1
            st.rerun()
    with c2:
        if st.button("Next Step") and current < total - 1:
            st.session_state["demo_step_idx"] = current + 1
            st.rerun()
    with c3:
        if st.button("Reset Demo"):
            st.session_state["demo_step_idx"] = 0
            st.rerun()
    with c4:
        st.progress((current + 1) / total, text=f"Step {current + 1} of {total}")

    st.markdown(f"#### {step['title']}")
    st.info(f"Goal: {step['goal']}")
    st.write(f"Show on screen: {step['show']}")

    st.markdown("**Artifacts to open during recording**")
    render_artifact_buttons(step.get("files", []), current)
    render_demo_snapshot(step["title"], metrics)

    if step.get("links"):
        st.markdown("**Public links for this step**")
        for link in step["links"]:
            st.link_button(link, link)

    st.markdown("**Run step check**")
    phase_map = {
        "Step 2 - Audit and Schema": "Phase 1 - Audit & Schema",
        "Step 3 - Dataset Authoring": "Phase 2 - Dataset Authoring",
        "Step 4 - Training Data Prep": "Phase 3 - Training Data Prep",
        "Step 5 - Training Run": "Phase 4 - Train/Ablate/Measure",
        "Step 6 - Ablation Results": "Phase 4 - Train/Ablate/Measure",
        "Step 7 - Publish Artifacts": "Phase 5 - Publish & Engage",
        "Step 8 - Community and Executive Artifacts": "Phase 5 - Publish & Engage",
        "Step 9 - Synthesis Memos": "Phase 6 - Synthesis Memos",
    }
    phase_name = phase_map.get(step["title"])
    if phase_name:
        script = PHASE_CHECKS[phase_name]["script"]
        if st.button("Run verification for this step", key=f"guided_verify_{current}"):
            code, output = run_verify(script)
            if code == 0:
                st.success("Step verification PASS")
            else:
                st.error(f"Step verification FAIL (exit {code})")
            render_result_console(output)

    st.markdown("**Demo actions (real outputs)**")
    a1, a2, a3 = st.columns(3)
    with a1:
        if st.button("Open first artifact preview", key=f"guided_action_preview_{current}"):
            first = step.get("files", [None])[0]
            if first:
                st.code(preview_text(ROOT / first), language="markdown")
            else:
                st.info("No artifact configured for this step.")
    with a2:
        if st.button("Run scoring evaluator", key=f"guided_action_score_{current}"):
            evaluator = ROOT / "audit" / "scoring_evaluator.py"
            if evaluator.exists():
                code, output = run_verify("audit/scoring_evaluator.py")
                if code == 0:
                    st.success("Scoring evaluator run PASS")
                else:
                    st.error(f"Scoring evaluator run FAIL (exit {code})")
                render_result_console(output)
            else:
                st.warning("`audit/scoring_evaluator.py` not found.")
    with a3:
        if st.button("Show key numbers", key=f"guided_action_numbers_{current}"):
            da = metrics.get("ablation", {}).get("delta_a", {})
            db = metrics.get("ablation", {}).get("delta_b", {})
            cp = metrics.get("ablation", {}).get("cost_pareto", {})
            st.json(
                {
                    "delta_a": da.get("delta"),
                    "delta_a_p_value": da.get("p_value"),
                    "delta_b": db.get("delta"),
                    "cost_per_task_baseline": cp.get("cost_per_task_baseline"),
                    "cost_per_task_with_judge": cp.get("cost_per_task_with_judge"),
                },
                expanded=True,
            )


def load_core_metrics() -> dict[str, Any]:
    ablation = read_json(ROOT / "ablations" / "ablation_results.json") or {}
    training_log = read_json(ROOT / "training" / "training_run.log") or {}
    train_contam = read_json(ROOT / "training" / "train_contamination_check.json") or {}
    dataset_contam = read_json(ROOT / "dataset" / "contamination_check.json") or {}
    evidence_graph = read_json(ROOT / "docs" / "evidence_graph.json") or {"claims": []}
    return {
        "ablation": ablation,
        "training_log": training_log,
        "train_contam": train_contam,
        "dataset_contam": dataset_contam,
        "evidence_graph": evidence_graph,
    }


def phase_overview(metrics: dict[str, Any]) -> None:
    section_title("Phase Overview")
    col1, col2, col3, col4 = st.columns(4)

    delta_a = metrics["ablation"].get("delta_a", {})
    delta_b = metrics["ablation"].get("delta_b", {})
    cost = metrics["ablation"].get("cost_pareto", {})

    col1.metric("Delta A", f"{delta_a.get('delta', 0):+.4f}")
    col2.metric("Delta A p-value", f"{delta_a.get('p_value', 1):.4f}")
    col3.metric("Delta B", f"{delta_b.get('delta', 0):+.4f}")
    col4.metric(
        "Cost/Task Delta",
        f"${(cost.get('cost_per_task_with_judge', 0) - cost.get('cost_per_task_baseline', 0)):.4f}",
    )

    st.caption(
        "Source: ablations/ablation_results.json. "
        "Deployment threshold target: Delta A positive with p < 0.05."
    )


def artifact_health(metrics: dict[str, Any]) -> None:
    section_title("Artifact Health")
    left, right = st.columns(2)

    with left:
        status_chip(file_exists(ROOT / "training" / "adapter" / "adapter_config.json"), "Adapter config")
        status_chip(file_exists(ROOT / "training" / "adapter" / "adapter_model.safetensors"), "Adapter weights")
        status_chip(file_exists(ROOT / "training" / "model_card.md"), "Model card")
        status_chip(file_exists(ROOT / "docs" / "memo.pdf"), "Executive memo PDF")
        status_chip(file_exists(ROOT / "docs" / "evidence_graph.json"), "Evidence graph")

    with right:
        status_chip(file_exists(ROOT / "dataset" / "README.md"), "HF dataset README")
        status_chip(file_exists(ROOT / "dataset" / "datasheet.md"), "Datasheet")
        status_chip(file_exists(ROOT / "dataset" / "data_card.md"), "Data card")
        status_chip(file_exists(ROOT / "docs" / "blog_post.md"), "Technical blog draft")
        status_chip(file_exists(ROOT / "docs" / "community_engagement.md"), "Community engagement record")

    summary = {
        "train_tasks": read_jsonl_count(ROOT / "dataset" / "train" / "tasks.jsonl"),
        "dev_tasks": read_jsonl_count(ROOT / "dataset" / "dev" / "tasks.jsonl"),
        "held_out_tasks": read_jsonl_count(ROOT / "dataset" / "held_out" / "tasks.jsonl"),
        "preference_pairs": read_jsonl_count(ROOT / "training" / "preference_pairs.jsonl"),
        "held_out_trace_rows": read_jsonl_count(ROOT / "ablations" / "held_out_traces.jsonl"),
        "evidence_claims": len(metrics["evidence_graph"].get("claims", [])),
    }
    st.markdown("<div class='summary-card'><b>Dataset and Evidence Summary</b></div>", unsafe_allow_html=True)
    st.json(summary, expanded=True)


def training_panel(metrics: dict[str, Any]) -> None:
    section_title("Training")
    log = metrics["training_log"]
    if not log:
        st.warning("training/training_run.log not found.")
        return

    st.json(
        {
            "run_id": log.get("run_id"),
            "backbone": log.get("backbone"),
            "training_method": log.get("training_method"),
            "lora_rank": log.get("lora_rank"),
            "lora_alpha": log.get("lora_alpha"),
            "learning_rate": log.get("learning_rate"),
            "batch_size": log.get("batch_size"),
            "gradient_accumulation_steps": log.get("gradient_accumulation_steps"),
            "num_epochs": log.get("num_epochs"),
            "seed": log.get("seed"),
            "total_wall_time_minutes": log.get("total_wall_time_minutes"),
            "training_pairs_used": log.get("training_pairs_used"),
            "validation_pairs_used": log.get("validation_pairs_used"),
            "final_train_loss": log.get("final_train_loss"),
            "final_val_loss": log.get("final_val_loss"),
        }
    )

    curve = log.get("loss_curve", [])
    if curve:
        chart_rows = []
        for row in curve:
            if row.get("loss") is not None:
                chart_rows.append({"step": row.get("step"), "loss": row.get("loss"), "type": "train"})
            if row.get("eval_loss") is not None:
                chart_rows.append({"step": row.get("step"), "loss": row.get("eval_loss"), "type": "eval"})
        st.line_chart(chart_rows, x="step", y="loss", color="type")


def ablation_panel(metrics: dict[str, Any]) -> None:
    section_title("Ablations")
    ab = metrics["ablation"]
    if not ab:
        st.warning("ablations/ablation_results.json not found.")
        return
    st.json(ab)

    da = ab.get("delta_a", {})
    gate = da.get("delta", 0) > 0 and (da.get("p_value", 1) < 0.05)
    status_chip(gate, "Delta A deployment gate (delta > 0 and p < 0.05)")


def contamination_panel(metrics: dict[str, Any]) -> None:
    section_title("Contamination")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Dataset contamination**")
        st.json(metrics["dataset_contam"] or {"missing": True})
    with c2:
        st.markdown("**Training contamination**")
        st.json(metrics["train_contam"] or {"missing": True})


def publish_panel() -> None:
    section_title("Publish Links")
    dataset_url = "https://huggingface.co/datasets/abdulaziz0111/tenacious-bench-v0.1"
    model_url = "https://huggingface.co/abdulaziz0111/tenacious-judge-v0.1"
    c1, c2 = st.columns(2)
    with c1:
        st.link_button("Open HuggingFace Dataset", dataset_url, use_container_width=True)
        st.markdown(f"[{dataset_url}]({dataset_url})")
    with c2:
        st.link_button("Open HuggingFace Model", model_url, use_container_width=True)
        st.markdown(f"[{model_url}]({model_url})")
    st.markdown(
        "Community submission status is tracked in "
        "`docs/community_engagement.md`."
    )


def phase_result_summary(phase_name: str, metrics: dict[str, Any]) -> None:
    if phase_name == "Phase 2 - Dataset Authoring":
        c1, c2, c3 = st.columns(3)
        c1.metric("Train Tasks", read_jsonl_count(ROOT / "dataset" / "train" / "tasks.jsonl"))
        c2.metric("Dev Tasks", read_jsonl_count(ROOT / "dataset" / "dev" / "tasks.jsonl"))
        c3.metric("Held-out Tasks", read_jsonl_count(ROOT / "dataset" / "held_out" / "tasks.jsonl"))
    elif phase_name == "Phase 3 - Training Data Prep":
        st.metric("Preference Pairs", read_jsonl_count(ROOT / "training" / "preference_pairs.jsonl"))
        train_contam = metrics.get("train_contam", {})
        if train_contam:
            st.write(
                {
                    "held_out_ngram_violations": len(train_contam.get("training_vs_held_out", {}).get("ngram_violations", [])),
                    "held_out_embedding_violations": len(train_contam.get("training_vs_held_out", {}).get("embedding_violations", [])),
                }
            )
    elif phase_name == "Phase 4 - Train/Ablate/Measure":
        da = metrics.get("ablation", {}).get("delta_a", {})
        db = metrics.get("ablation", {}).get("delta_b", {})
        c1, c2, c3 = st.columns(3)
        c1.metric("Delta A", f"{da.get('delta', 0):+.4f}")
        c2.metric("Delta B", f"{db.get('delta', 0):+.4f}")
        c3.metric("Delta A p", f"{da.get('p_value', 1):.4f}")
    elif phase_name == "Phase 5 - Publish & Engage":
        st.link_button(
            "Dataset URL",
            "https://huggingface.co/datasets/abdulaziz0111/tenacious-bench-v0.1",
            use_container_width=True,
        )
        st.link_button(
            "Model URL",
            "https://huggingface.co/abdulaziz0111/tenacious-judge-v0.1",
            use_container_width=True,
        )
    elif phase_name == "Phase 6 - Synthesis Memos":
        st.metric("Memo Files", len(list((ROOT / "synthesis_memos").glob("*.md"))))


def demo_flow_panel(metrics: dict[str, Any]) -> None:
    section_title("Demo Flow")
    st.caption("Run each project phase with a dedicated button, or run the full sequence.")

    if "phase_results" not in st.session_state:
        st.session_state["phase_results"] = {}

    col_a, col_b = st.columns([3, 2])
    with col_a:
        selected_phase = st.selectbox("Select phase", list(PHASE_CHECKS.keys()))
    with col_b:
        if st.button("Run Full Sequence"):
            for phase_name, config in PHASE_CHECKS.items():
                code, output = run_verify(config["script"])
                st.session_state["phase_results"][phase_name] = {"code": code, "output": output}

    st.download_button(
        "Download Demo Report",
        data=build_demo_report(metrics),
        file_name="tenacious_demo_report.md",
        mime="text/markdown",
        use_container_width=True,
    )

    cols = st.columns(3)
    for idx, (phase_name, config) in enumerate(PHASE_CHECKS.items()):
        with cols[idx % 3]:
            if st.button(f"Run {phase_name}", key=f"btn_{phase_name}"):
                code, output = run_verify(config["script"])
                st.session_state["phase_results"][phase_name] = {"code": code, "output": output}

    st.markdown("---")
    st.markdown(f"#### {selected_phase}")
    config = PHASE_CHECKS[selected_phase]
    phase_result_summary(selected_phase, metrics)

    artifact_status = {}
    for rel in config["artifacts"]:
        artifact_status[rel] = file_exists(ROOT / rel)
    st.write({"artifacts": artifact_status})

    result = st.session_state["phase_results"].get(selected_phase)
    if result:
        if result["code"] == 0:
            st.success("Verification: PASS")
        else:
            st.error(f"Verification: FAIL (exit {result['code']})")
        render_result_console(result["output"])
    else:
        st.info("No run result yet for this phase. Click its button to execute verification.")


def verifier_panel() -> None:
    section_title("Verification Runner")
    options = [
        ("Audit", "tests/verify_audit_phase.py"),
        ("Dataset Authoring", "tests/verify_dataset_authoring.py"),
        ("Inter-rater + Docs", "tests/verify_inter_rater_and_docs.py"),
        ("Training Prep", "tests/verify_training_prep.py"),
        ("Training Contamination", "tests/verify_training_contamination.py"),
        ("Phase 4", "tests/verify_phase4_scaffold.py"),
        ("Model Card", "tests/verify_model_card.py"),
        ("Phase 5 Publish", "tests/verify_phase5_publish.py"),
        ("Phase 5 Exec", "tests/verify_phase5_exec.py"),
        ("Synthesis Memos", "tests/verify_synthesis_memos.py"),
    ]

    label_to_script = {label: script for label, script in options}
    selected = st.multiselect("Select checks", [label for label, _ in options], default=["Phase 4", "Model Card"])

    if st.button("Run selected checks"):
        for label in selected:
            script = label_to_script[label]
            code, output = run_verify(script)
            if code == 0:
                st.success(f"{label}: PASS")
            else:
                st.error(f"{label}: FAIL (exit {code})")
            render_result_console(output)


def docs_preview_panel() -> None:
    section_title("Document Preview")
    candidates = [
        "README.md",
        "docs/blog_post.md",
        "docs/community_engagement.md",
        "training/model_card.md",
        "audit/methodology.md",
    ]
    selected = st.selectbox("Preview file", candidates)
    path = ROOT / selected
    if path.exists():
        st.markdown(f"**File:** `{selected}`")
        st.text_area("Content", path.read_text(encoding="utf-8"), height=360)
    else:
        st.warning(f"Missing file: {selected}")


def main() -> None:
    st.set_page_config(page_title="Tenacious Week 11 Dashboard", layout="wide")
    inject_styles()
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">Tenacious Week 11 Delivery Dashboard</div>
            <div class="hero-sub">Interactive control room for benchmark authoring, training, ablations, publication, and executive evidence.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_phase_chips()

    metrics = load_core_metrics()
    phase_overview(metrics)
    artifact_health(metrics)

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        ["Guided Demo", "Demo Flow", "Training", "Ablations", "Contamination", "Verify", "Docs"]
    )
    with tab1:
        guided_demo_panel(metrics)
    with tab2:
        demo_flow_panel(metrics)
    with tab3:
        training_panel(metrics)
    with tab4:
        ablation_panel(metrics)
    with tab5:
        contamination_panel(metrics)
        publish_panel()
    with tab6:
        verifier_panel()
    with tab7:
        docs_preview_panel()


if __name__ == "__main__":
    main()
