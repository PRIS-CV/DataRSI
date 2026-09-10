# Experimental Results and Evaluation Ledger

This document details the quantitative results reported in the ICASSP 2027 paper.

---

## 1. Historical Task Adaptation Feasibility (Table 1a)

Evaluated on **DataRSI-Bench** ($N=384, 512 \times 512$ resolution) across 4 object identities, 8 azimuths, 4 elevations, and 3 distances. This comparison establishes the baseline feasibility of adapting the editor with synthetic supervision.

| Model Checkpoint | Description | PSNR (dB) $\uparrow$ | SSIM $\uparrow$ | LPIPS $\downarrow$ | FID $\downarrow$ | Acc@$45^\circ$ (\%) $\uparrow$ |
|---|---|:---:|:---:|:---:|:---:|:---:|
| **Base** | Qwen-Image-Edit-2511 | 12.82 | 0.6679 | 0.5595 | 95.88 | 12.50% |
| **fal (ref.)** | Multiple-Angles LoRA | 12.93 | 0.6804 | 0.5597 | 93.05 | 22.40% |
| **Data-Evolved** | Recipe-driven supervision (420 pairs) | 13.29 | 0.6813 | 0.5303 | 89.41 | 22.92% |
| **Historical DataRSI** | First-pass harness adapter (96 views, rank-32) | **14.36** | **0.7223** | **0.5058** | **89.19** | **33.33%** |

> [!NOTE]
> This table establishes domain adaptation feasibility across different data configurations. It is distinct from the matched-budget allocation experiment in Section 2.

---

## 2. Controlled Experiment: Uniform-72 vs. Targeted-72 (Table 3)

The primary controlled experiment isolates the effect of failure-directed request allocation under an identical **72-request synthesis budget** ($M=72$) evaluated across three random training seeds (42, 43, 44).

### Aggregate Results (Means $\pm$ SD across seeds)

| Metric | Base | Uniform-72 | Targeted-72 | Delta ($\text{Targeted} - \text{Uniform}$) |
|---|:---:|:---:|:---:|:---:|
| **Weak-4 Rotation Error ($^\circ$) $\downarrow$** | 112.23 | $50.45 \pm 2.15$ | $\mathbf{35.50 \pm 3.23}$ | $\mathbf{-14.950 \pm 1.097^\circ}$ |
| **Weak-4 PSNR (dB) $\uparrow$** | 12.22 | $13.88 \pm 0.07$ | $\mathbf{14.43 \pm 0.09}$ | $\mathbf{+0.543 \pm 0.023\text{ dB}}$ |
| **Overall LPIPS $\downarrow$** | 0.2636 | $0.2058 \pm 0.0028$ | $\mathbf{0.2014 \pm 0.0030}$ | $\mathbf{-0.0044 \pm 0.0003}$ |

### Seed-by-Seed Paired Breakdown (Weak-4 Rotation Error)

| Seed | Base | Uniform-72 | Targeted-72 | Paired Difference ($\Delta$) | Targeted Wins? |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **42** | $112.23^\circ$ | $52.62^\circ$ | $38.83^\circ$ | $-13.790^\circ$ | Yes ($\checkmark$) |
| **43** | $112.23^\circ$ | $49.79^\circ$ | $33.82^\circ$ | $-15.970^\circ$ | Yes ($\checkmark$) |
| **44** | $112.23^\circ$ | $48.94^\circ$ | $33.85^\circ$ | $-15.090^\circ$ | Yes ($\checkmark$) |
| **Mean $\pm$ SD** | $112.23^\circ$ | $50.45 \pm 2.15^\circ$ | $35.50 \pm 3.23^\circ$ | $\mathbf{-14.950 \pm 1.097^\circ}$ | **3 / 3 Seeds** |

### Trade-off and Non-Target Slices
- **Non-weak rotation trade-off**: $+2.370 \pm 0.046^\circ$ ($34.64^\circ$ for Targeted vs. $32.27^\circ$ for Uniform), both vastly superior to Base ($64.13^\circ$).
- **Overall rotation change**: $+0.205 \pm 0.125^\circ$ (effectively preserved).

---

## 3. Failure Localization Calibration Evidence

- **Structured Factor Space**: $\mathcal{A} \times \mathcal{H} \times \mathcal{R} = 8 \times 4 \times 3 = 96$ views across 32 azimuth-elevation slice cells.
- **Top-4 Diagnosed Weak Slices (Weak-4)**:
  - $(135^\circ, 60^\circ)$
  - $(225^\circ, -30^\circ)$
  - $(135^\circ, -30^\circ)$
  - $(225^\circ, 30^\circ)$
- **Calibration Signal**: Pooled Spearman rank correlation $\rho = 0.779$; Weak-4 overlap with downstream geometric error agreement: $75\%$ ($3/4$).

---

## 4. Regression-Aware Model Admission Verdicts

Under frozen rule protocol $g_{\mathrm{RA}}$ ($\ge 5\%$ Weak-4 reduction, canonical $(0^\circ, 0^\circ) < 5.000^\circ$):

- **Seed 42**: Weak-4 reduction $65.39\%$, canonical error $4.382^\circ \to$ **PROMOTE**
- **Seed 43**: Weak-4 reduction $69.86\%$, canonical error $4.195^\circ \to$ **PROMOTE**
- **Seed 44**: Weak-4 reduction $69.84\%$, canonical error $4.251^\circ \to$ **PROMOTE**
- **Final Verdict**: **PROMOTE 3 / 3 seeds**
