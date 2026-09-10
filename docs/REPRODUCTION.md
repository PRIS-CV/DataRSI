# DataRSI Reproduction Guide

This guide provides instructions to reproduce the experimental results reported in our ICASSP 2027 paper:
**"DataRSI: A 3D Data Harness for Failure-to-Data Evolution"**.

Reviewers can verify all primary claims and tables in under **30 seconds** via the Evaluation-Only pathway without downloading massive model weights.

---

## 1. Environment Setup

### Prerequisites
- Python 3.10+
- PyTorch 2.1+
- CUDA 11.8+ (only needed for full GPU training)

```bash
git clone https://github.com/PRIS-CV/DataRSI.git
cd DataRSI
pip install -r requirements.txt
pip install -e .
```

---

## 2. Fast Evaluation-Only Reproduction (< 30 Seconds)

All numeric claims, seed evaluations, contrast differentials, and admission verdicts can be independently recomputed directly from the frozen, audited artifacts in `artifacts/icassp2027/`.

### Step 2.1: Reproduce Table 1 and Table 3
Reproduces Historical Adaptation (Table 1a), Mechanism Audit (Table 1b), and Matched-Budget Allocation (Table 3):
```bash
python scripts/reproduce_tables.py
# or: bash scripts/reproduce_tables.sh
```

### Step 2.2: Verify 3/3 Model Admission Verdicts
Verifies that all three seeds (42, 43, 44) satisfy the frozen regression guards and receive `PROMOTE`:
```bash
python scripts/reproduce_admission.py
```
- **Seed 42**: Weak-4 error reduction $65.39\%$, canonical error $4.382^\circ < 5.0^\circ \to$ **PROMOTE**
- **Seed 43**: Weak-4 error reduction $69.86\%$, canonical error $4.195^\circ < 5.0^\circ \to$ **PROMOTE**
- **Seed 44**: Weak-4 error reduction $69.84\%$, canonical error $4.251^\circ < 5.0^\circ \to$ **PROMOTE**

### Step 2.3: Verify Executable Sample Repair Audit
Inspects the 72-candidate repair study and individual repair trace logs:
```bash
python scripts/reproduce_repair_audit.py
```
- Total Candidates: 72
- Initial Pass / Fail: 29 / 43 ($59.72\%$ defect rate)
- Eligible for repair: 7
- Successfully recovered: 2 within $\le 2$ rounds
- Final compliant samples: 31 / 72 ($43.06\%$)

### Step 2.4: Inspect Failure Localization and Factor Space
Inspects the 96-view factor space $\mathcal{A} \times \mathcal{H} \times \mathcal{R}$ and Weak-4 cells:
```bash
python scripts/reproduce_diagnosis.py
```
- Diagnosed Weak-4 Cells: $(135^\circ, 60^\circ)$, $(225^\circ, -30^\circ)$, $(135^\circ, -30^\circ)$, $(225^\circ, 30^\circ)$
- Calibration signal: Pooled Spearman $\rho = 0.779$, Weak-4 agreement $75\%$ ($3/4$).

---

## 3. Full Training & Inference Pipeline

To run the end-to-end training and inference pipeline from scratch:

### Step 3.1: Download Base Model & Author Assets
Download the base model checkpoint (`Qwen-Image-Edit-2511`) and authored 3D assets to `data/` or configure via `configs/icassp2027/protocol.yaml`.

### Step 3.2: Generate Supervision under Budget ($M=72$)
Compile requests for Targeted-72 or Uniform-72:
```bash
bash scripts/reproduce_targeted72.sh
bash scripts/reproduce_uniform72.sh
```

### Step 3.3: Run LoRA Candidate Training
Train rank-32 LoRA adapters across the 3 registered seeds (42, 43, 44):
```bash
# Targeted-72 training across seeds
python -m datarsi.training.train --config configs/icassp2027/targeted72.yaml --seed 42
python -m datarsi.training.train --config configs/icassp2027/targeted72.yaml --seed 43
python -m datarsi.training.train --config configs/icassp2027/targeted72.yaml --seed 44
```

### Step 3.4: Evaluate Model Candidates on Frozen Development Split
Run geometric evaluation via OriAnyV2:
```bash
bash scripts/evaluate_rotation.sh
```
