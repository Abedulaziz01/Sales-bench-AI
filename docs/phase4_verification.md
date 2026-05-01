# Phase 4 Verification

## Training Preflight

Run this locally before moving to Colab:

```powershell
python training\train.py --dry-run
```

Expected:

- `Dry run passed.`
- backbone prints as `unsloth/Qwen2.5-0.5B-Instruct`
- ORPO method, seed, and train/eval pair counts are shown

## Real GPU Training

Run this in Google Colab with a T4 GPU:

```python
!python training/train.py --push-repo abdulaziz0111/tenacious-judge-adapter
```

After the run finishes, verify:

```python
!ls training/adapter
!cat training/training_run.log
```

Expected adapter artifacts:

- `adapter_config.json`
- `adapter_model.safetensors`

Expected log fields:

- `backbone`
- `lora_rank`
- `lora_alpha`
- `learning_rate`
- `batch_size`
- `gradient_accumulation_steps`
- `training_method`
- `num_epochs`
- `seed`
- `total_wall_time_minutes`
- `training_pairs_used`
- `final_train_loss`
- `final_val_loss`

## Ablations

Run the local scaffold:

```powershell
python ablations\run_ablations.py --scorer local
python ablations\bootstrap_test.py
```

Expected current result:

- Delta A positive
- Delta A `p_value < 0.05`
- Delta B reported explicitly
- cost and latency fields populated

## One-Command Check

```powershell
python tests\verify_phase4_scaffold.py
```

Expected:

- `Phase 4 scaffold verification passed.`
