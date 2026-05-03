# Sales-bench-AI: Tenacious-Bench v0.1

Tenacious-Bench v0.1 is a domain-specific evaluation and training system for B2B sales outreach reliability.  
This project is designed for the Tenacious workflow where correctness is not just linguistic quality, but grounded, honest, policy-safe behavior under real prospect signals.

Unlike generic agent benchmarks, this repository targets business-critical failure modes:

- weak or missing public-signal grounding
- over-commitment of engineering capacity
- tone drift away from Tenacious voice standards
- confidence-inappropriate phrasing on uncertain signals
- incorrect qualification and call-to-action behavior
- contamination leakage between train/dev/held-out

The repo implements the full Week 11 arc: benchmark design, dataset authoring, training data prep, Path B judge training scaffolding, ablation framework, publication artifacts, and demo dashboard.

---

## 1. Executive Summary

This project answers a practical question:  
How do we evaluate and improve an outreach agent for Tenacious-specific sales quality, not generic benchmark performance?

The solution in this repository includes:

- a machine-verifiable schema and scoring evaluator
- a multi-source dataset pipeline (trace-derived, programmatic, synthesis, adversarial)
- contamination-resistant partitioning rules
- Path B preference-pair training data and leakage prevention
- training and ablation scaffolding with statistical decision gates
- publication artifacts (dataset/model cards, memo, evidence graph)
- a Streamlit dashboard for live demo and verification

Current headline benchmark metrics (from recorded ablation artifacts):

- Delta A: `+0.3785`
- Delta A 95% CI: `[0.3487, 0.4084]`
- Delta A p-value: `0.0000`
- Delta B: `+0.1033`
- Cost per task baseline: `$0.0029`
- Cost per task with judge: `$0.0047`

---

## 2. What Tenacious-Bench Measures

Tenacious-Bench evaluates whether generated outreach is defensible for real B2B sales deployment:

1. Grounded
- references at least one concrete public signal
- avoids fabricated funding, hiring, or competitor facts

2. Honest
- respects known uncertainty and confidence level
- avoids unsupported pricing/capacity claims

3. Professional
- follows channel and style constraints
- excludes banned phrases and vendor-cliche language

4. Non-condescending
- frames gaps as research-backed questions
- avoids accusatory or shaming framing

5. Actionable
- includes one clear ask and proper CTA structure
- uses policy-safe next steps (calendar/scoping routing where valid)

---

## 3. Repository Scope by Phase

### Phase 1: Audit and Schema

Core files:

- [audit/audit_memo.md](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/audit/audit_memo.md)
- [audit/gap_analysis.md](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/audit/gap_analysis.md)
- [audit/schema.json](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/audit/schema.json)
- [audit/scoring_evaluator.py](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/audit/scoring_evaluator.py)
- [audit/methodology.md](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/audit/methodology.md)

Deliverable state:

- gap taxonomy defined
- scoring contract implemented as `(task, agent_output) -> numeric score`
- rubric dimensions decomposed into mechanical checks

---

### Phase 2: Dataset Authoring

Authoring modes implemented:

- Trace-derived tasks
- Programmatic parameter sweeps
- Multi-LLM synthesis + judge filter
- Hand-authored adversarial tasks

Dataset and script files:

- [dataset/adversarial_tasks.jsonl](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/dataset/adversarial_tasks.jsonl)
- [dataset/adversarial_notes.md](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/dataset/adversarial_notes.md)
- [dataset/contamination_check.json](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/dataset/contamination_check.json)
- [generation_scripts/trace_derived.py](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/generation_scripts/trace_derived.py)
- [generation_scripts/programmatic_sweep.py](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/generation_scripts/programmatic_sweep.py)
- [generation_scripts/multi_llm_synthesis.py](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/generation_scripts/multi_llm_synthesis.py)
- [generation_scripts/judge_filter.py](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/generation_scripts/judge_filter.py)
- [generation_scripts/dedup.py](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/generation_scripts/dedup.py)
- [generation_scripts/contamination_check.py](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/generation_scripts/contamination_check.py)

Current counts (from project artifacts):

| Artifact | Count |
|---|---:|
| Trace-derived tasks | 72 |
| Programmatic sweep tasks | 216 |
| Synthesis accepted | 60 |
| Adversarial tasks | 30 |
| Combined deduped | 336 |
| Train split | 168 |
| Dev split | 101 |
| Held-out split | 67 |

Contamination status:

- n-gram violations: `0`
- embedding violations: `0`
- time-shift verification: `true`

---

### Phase 3: Training Data Preparation (Path B)

Core files:

- [training/preference_pairs.jsonl](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/training/preference_pairs.jsonl)
- [training/pair_construction.py](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/training/pair_construction.py)
- [training/leakage_prevention_log.md](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/training/leakage_prevention_log.md)
- [training/train_contamination_check.json](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/training/train_contamination_check.json)
- [training/methodology_rationale.md](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/training/methodology_rationale.md)

What is enforced:

- chosen vs rejected preference structure
- score-gated quality checks
- no same-family generate-and-judge leakage
- contamination checks against dev and held-out

---

### Phase 4: Train, Ablate, Measure

Core files:

- [training/train.py](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/training/train.py)
- [training/training_run.log](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/training/training_run.log)
- [training/model_card.md](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/training/model_card.md)
- [ablations/run_ablations.py](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/ablations/run_ablations.py)
- [ablations/ablation_results.json](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/ablations/ablation_results.json)
- [ablations/cost_pareto.json](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/ablations/cost_pareto.json)
- [ablations/held_out_traces.jsonl](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/ablations/held_out_traces.jsonl)
- [ablations/bootstrap_test.py](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/ablations/bootstrap_test.py)

Training and ablation expectations:

- LoRA adapter only (no merged full backbone upload)
- Delta A positive and significant (`p < 0.05`)
- Delta B reported honestly
- cost/latency deltas explicitly documented

---

### Phase 5: Publish and Engage

Core files:

- [dataset/README.md](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/dataset/README.md)
- [dataset/hf_upload.py](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/dataset/hf_upload.py)
- [training/hf_push_adapter.py](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/training/hf_push_adapter.py)
- [docs/blog_post.md](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/docs/blog_post.md)
- [docs/community_engagement.md](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/docs/community_engagement.md)
- [docs/memo.pdf](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/docs/memo.pdf)
- [docs/evidence_graph.json](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/docs/evidence_graph.json)

Published artifact URLs:

- Dataset: `https://huggingface.co/datasets/abdulaziz0111/tenacious-bench-v0.1`
- Model: `https://huggingface.co/abdulaziz0111/tenacious-judge-v0.1`

---

### Phase 6: Synthesis Memos

All memo files live under:

- [synthesis_memos](/C:/Users/user/Desktop/mll/week11/Sales-bench-AI/synthesis_memos)

Expected structure:

- each memo includes disagreement/adaptation
- decisions tie back to Week 10/11 evidence, not summary-only prose

---

## 4. Project Structure

```text
Sales-bench-AI/
  audit/
    audit_memo.md
    gap_analysis.md
    methodology.md
    schema.json
    scoring_evaluator.py

  dataset/
    train/tasks.jsonl
    dev/tasks.jsonl
    held_out/tasks.jsonl
    adversarial_tasks.jsonl
    adversarial_notes.md
    contamination_check.json
    datasheet.md
    data_card.md
    README.md
    hf_upload.py

  generation_scripts/
    trace_derived.py
    programmatic_sweep.py
    multi_llm_synthesis.py
    judge_filter.py
    dedup.py
    partition_dataset.py
    contamination_check.py
    logs/

  training/
    pair_construction.py
    preference_pairs.jsonl
    leakage_prevention_log.md
    train.py
    training_run.log
    train_contamination_check.json
    methodology_rationale.md
    model_card.md
    hf_push_adapter.py
    adapter/

  ablations/
    run_ablations.py
    bootstrap_test.py
    ablation_results.json
    cost_pareto.json
    held_out_traces.jsonl

  docs/
    blog_post.md
    community_engagement.md
    memo.pdf
    evidence_graph.json

  synthesis_memos/
    *.md

  tests/
    verify_audit_phase.py
    verify_dataset_authoring.py
    verify_training_prep.py
    verify_phase4_scaffold.py
    verify_phase5_publish.py
    verify_phase5_exec.py
    verify_synthesis_memos.py

  streamlit_app.py
  requirements.txt
```

---

## 5. Environment Setup

### Python

- Recommended: `Python 3.11+`

### Install

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Optional training/runtime extras

If local GPU training is not available, run Phase 4 training in Colab/RunPod and sync artifacts back into this repo.

---

## 6. Configuration and Secrets

Use `.env` (gitignored) for sensitive keys:

- `OPENROUTER_API_KEY`
- `HUGGINGFACE_TOKEN`
- `ANTHROPIC_API_KEY` (if running eval-tier scripts that require it)

Never commit `.env`.

---

## 7. Core Verification Commands

Run from repo root:

```powershell
python tests\verify_audit_phase.py
python tests\verify_dataset_authoring.py
python tests\verify_training_prep.py
python tests\verify_phase4_scaffold.py
python tests\verify_model_card.py
python tests\verify_phase5_publish.py
python tests\verify_phase5_exec.py
python tests\verify_synthesis_memos.py
```

If you want one broad smoke run quickly:

```powershell
python tests\verify_phase4_scaffold.py
```

---

## 8. Rebuild Pipeline (Dataset + Training Inputs)

### Dataset authoring

```powershell
python generation_scripts\trace_derived.py
python generation_scripts\programmatic_sweep.py
python generation_scripts\multi_llm_synthesis.py
python generation_scripts\judge_filter.py
python generation_scripts\build_adversarial_tasks.py
python generation_scripts\dedup.py
python generation_scripts\partition_dataset.py
python generation_scripts\contamination_check.py
```

### Preference pair construction

```powershell
python training\pair_construction.py
python training\train_contamination_check.py
```

---

## 9. Training and Ablations

### Train

```powershell
python training\train.py
```

### Run ablations

```powershell
python ablations\run_ablations.py
python ablations\bootstrap_test.py
```

Artifacts expected after Phase 4:

- `training/adapter/adapter_config.json`
- `training/adapter/adapter_model.safetensors`
- `training/training_run.log`
- `ablations/ablation_results.json`
- `ablations/cost_pareto.json`
- `ablations/held_out_traces.jsonl`

---

## 10. Streamlit Demo Dashboard

Run:

```powershell
streamlit run streamlit_app.py
```

Dashboard includes:

- Phase overview metrics
- Guided 9-step demo flow
- Per-step artifact preview buttons
- Live verification triggers
- Training/ablation summaries
- Publication link panel
- Downloadable demo report

Suggested recording flow:

1. Project Overview
2. Audit and Schema
3. Dataset Authoring
4. Training Data Prep
5. Training Run
6. Ablation Results
7. Publish Artifacts
8. Community and Executive Artifacts
9. Synthesis Memos

---

## 11. Publication and Compliance Checklist

Before final public release:

- datasheet complete (all required sections)
- data card layered details complete
- held-out policy respected for benchmark integrity
- model card complete and consistent with ablation numbers
- license metadata present in HF cards
- evidence graph links every numeric claim to a source artifact

---

## 12. Known Risks and Mitigations

1. Local environment drift  
- Mitigation: run verifier scripts before every commit.

2. API/provider model availability changes  
- Mitigation: keep model routing configurable; log exact model IDs in methodology logs.

3. Leakage between generation and judge models  
- Mitigation: documented family rotation plus contamination checks.

4. Visual demo mismatch due browser cache  
- Mitigation: hard refresh (`Ctrl+F5`) after CSS/dashboard updates.

---

## 13. Troubleshooting

### `ModuleNotFoundError`

Install dependencies in active venv:

```powershell
pip install -r requirements.txt
```

### OpenRouter connectivity/proxy errors

- disable inherited proxy in test session where needed
- verify key is loaded from `.env`
- use currently available model IDs

### Hugging Face `whoami` `KeyError: 'email'`

Some responses include username but not email.  
Treat successful username return as valid authentication.

### Colab `load_dotenv()` assertion issue

Use explicit path:

```python
load_dotenv(dotenv_path=".env")
```

---

## 14. Contribution Notes

When adding features:

- preserve evaluator contract and rubric semantics
- update verifier scripts with any new required artifacts
- keep model cards, datasheets, and evidence graph in sync with metric changes
- prefer deterministic scripts and log all generated counts

---

## 15. License

Repository code and scripts follow the repository license terms.  
Dataset publication target for Tenacious-Bench v0.1 is CC-BY-4.0 unless explicitly changed with rationale.

