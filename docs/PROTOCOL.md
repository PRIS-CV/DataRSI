# DataRSI Formal Protocol Specification ($\Gamma$)

This document specifies the formal bounded-revision protocol $\Gamma$ governing the DataRSI 3D data harness for the ICASSP 2027 testbed.

---

## 1. Harness Transaction Flow

At revision $t$, the current champion $\theta_t^*$ is frozen and denoted $\theta_0$. All hyperparameters, spaces, budgets, and criteria are compiled into an immutable protocol:

$$\Gamma = (\mathcal{D}, \mathcal{P}, M, \mathcal{G}, \mathcal{F}_{\mathrm{diag}}, g_{\mathrm{sample}}, \mathcal{T}, \mathcal{F}_{\mathrm{adm}}, g_{\mathrm{RA}})$$

The revision follows the deterministic execution sequence:

$$\Gamma, \theta_0 \xrightarrow{\mathcal{F}_{\mathrm{diag}}} S_0^{\mathrm{diag}} \xrightarrow{\preceq_{\mathrm{diag}}} W \xrightarrow{\operatorname{Alloc}_\Gamma} Q \xrightarrow{\mathcal{G}} C_Q \xrightarrow{g_{\mathrm{sample}}} A_Q \xrightarrow{\mathcal{T}} \theta_Q$$

followed by:

$$(\theta_0, \theta_Q) \xrightarrow{\mathcal{F}_{\mathrm{adm}}} (S_0^{\mathrm{adm}}, S_Q^{\mathrm{adm}}) \xrightarrow{g_{\mathrm{RA}}(\cdot; W)} \{\textsc{Promote}, \textsc{Rollback}\}$$

---

## 2. Factor Space & Failure Localization

- **Factor Space**: $\mathcal{P} = \mathcal{A} \times \mathcal{H} \times \mathcal{R}$
  - Azimuths $\mathcal{A}$: 8 angles ($0^\circ, 45^\circ, 90^\circ, 135^\circ, 180^\circ, 225^\circ, 270^\circ, 315^\circ$)
  - Elevations $\mathcal{H}$: 4 angles ($-30^\circ, 0^\circ, 30^\circ, 60^\circ$)
  - Radii $\mathcal{R}$: 3 distances ($2.4, 4.0, 7.2$\,m)
  - Total discrete viewpoints: $8 \times 4 \times 3 = 96$ across 32 azimuth-elevation slice cells $\mathcal{C}$.
- **Diagnostic Evaluator $\mathcal{F}_{\mathrm{diag}}$**: VGGT.
- **Weak-4 Slices ($W$)**: Top-$K$ ($K=4$) cells ranked by descending error:
  1. $(135^\circ, 60^\circ)$
  2. $(225^\circ, -30^\circ)$
  3. $(135^\circ, -30^\circ)$
  4. $(225^\circ, 30^\circ)$
- **Calibration Signal**: Evaluated on 288 GT validation pairs, OriAnyV2 achieves a pooled rank correlation $\rho = 0.779$ and $75\%$ ($3/4$) agreement with frozen Weak-4 diagnosis (median GT rotation error: $7.22^\circ$, Acc@$30^\circ$: $79.51\%$).

---

## 3. Two-Level Revision Control

### Level 1: Deterministic Sample Contract ($g_{\mathrm{sample}}$)
Candidate supervision $C_Q = \mathcal{G}(Q)$ is admitted into $A_Q$ if and only if $g_{\mathrm{sample}}(x; \Gamma) = 1$:
1. **Bounding Box Margin**: $\ge 5\%$ margin to image frame borders.
2. **Mask Coverage**: $\ge 1\%$ foreground pixel ratio.
3. **Raycast Visible-to-Amodal Ratio**: $\ge 0.80$ evaluated on a $96 \times 96$ ray grid.
4. **Mesh Intersection**: Disallowed (zero mesh penetration with support plane).

Eligible defects (underexposure, overexposure, ground occlusion/intersection) enter bounded environment repair ($\le 2$ rounds) before final contract evaluation. Non-compliant samples are rejected.

### Level 2: Regression-Aware Model Admission ($g_{\mathrm{RA}}$)
Candidate model $\theta_Q = \mathcal{T}(\theta_0, A_Q)$ replaces the champion ($\theta^* \leftarrow \theta_Q$) if and only if $g_{\mathrm{RA}}(S_0^{\mathrm{adm}}, S_Q^{\mathrm{adm}}; W) = \textsc{Promote}$:
1. **Weak-4 Utility Gain**: $\ge 5.0\%$ reduction in mean Weak-4 rotation error relative to $\theta_0$.
2. **Non-Target Regression Guard**: Non-target cell regressions $\le 2.0\%$ vs Base without aggregate compensation.
3. **Canonical Hard Redline**: Canonical view $(0^\circ, 0^\circ)$ rotation error $< 5.000^\circ$.
