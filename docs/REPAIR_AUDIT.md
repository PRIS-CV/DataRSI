# Executable 3D Repair Audit

This document presents the empirical audit of DataRSI's generation-time **Bounded Repair** and **Sample Contract** mechanisms.

---

## 1. Study Scope and Methodological Boundary

> [!IMPORTANT]
> **Boundary Statement**: This repair audit evaluates independent Blender renders generated at matching registered coordinates $(i, p_s, p_t, r)$ corresponding to the Weak-4 slice cells. It is **empirically distinct** from the static training pool utilized in the Uniform-72 vs. Targeted-72 matched-budget training experiment reported in Table 3.
> 
> The purpose of this study is to demonstrate the **executability** and **boundedness** of physical 3D repair actions, rather than claiming that sample repair was the primary cause of downstream adapter gains in Table 3.

---

## 2. Quantitative Repair Audit Breakdown

Across the 72 registered candidate synthesis requests:

| Audit Stage | Count | Percentage |
|---|---|---|
| **Total Evaluated Requests** | 72 | 100.0% |
| **Initially Passed Sample Contract** | 29 | 40.28% |
| **Initially Failed Sample Contract** | 43 | 59.72% |
| **Repair-Eligible Visible Defects** | 7 | 9.72% of total (16.28% of failures) |
| **Successfully Recovered ($\le 2$ rounds)** | **2** | 28.57% of eligible defects |
| **Final Admitted Compliant Samples** | **31** | **43.06%** of total pool |

### Interpretation
- Out of 43 initial failures, 36 samples exhibited non-repairable geometric defects (e.g., severe clipping or unrecoverable identity mismatch) and were dropped.
- 7 samples exhibited eligible defects (localized underexposure/overexposure or ground support collision).
- Under the registered bounded repair policy ($\le 2$ adjustment attempts), 2 samples were successfully brought into full compliance with the deterministic Sample Contract.

---

## 3. Case Studies: Two Real Recovery Traces

### Case 1: Underexposure Recovery via Radiometric EV Tuning
- **Asset ID**: `camera_002`
- **Request Coordinates**: Azimuth $135^\circ$, Elevation $-30^\circ$, Orbit distance $2.4$\,m
- **Initial Diagnosis**:
  - Deterministic checks: Bounding box margin $6.2\%$, ray ratio $0.824$, mesh intersection: False.
  - Multimodal Inspector: Flagged `underexposure` (subject underexposed due to steep downward pitch and negative elevation shadowing).
  - Verdict: Fail ($g_{\mathrm{sample}} = 0$).
- **Bounded Repair Action (Round 1)**:
  - Policy adjustment: Exposure boost $\Delta \text{EV} = +0.50$, camera pose and viewpoint strictly preserved.
- **Post-Repair Re-inspection**:
  - Contrast and lighting verified; feature geometry recovered.
  - Ray ratio $0.841 \ge 0.80$, BBox margin $6.2\% \ge 5\%$.
  - Verdict: **PASS** ($g_{\mathrm{sample}} = 1$).

### Case 2: Ground Intersection Recovery via Support Plane Restaging
- **Asset ID**: `clock_004`
- **Request Coordinates**: Azimuth $225^\circ$, Elevation $-30^\circ$, Orbit distance $4.0$\,m
- **Initial Diagnosis**:
  - Deterministic checks: Bounding box margin $5.4\%$, ray ratio $0.781$, mesh intersection: **True** (pedestal mesh penetrated the support plane).
  - Multimodal Inspector: Flagged `ground_intersection`.
  - Verdict: Fail ($g_{\mathrm{sample}} = 0$).
- **Bounded Repair Action (Round 1)**:
  - Policy adjustment: Restage object vertical support anchor by $+0.25$ units along the Z-axis.
- **Post-Repair Re-inspection**:
  - Mesh intersection: False; physical support boundary cleanly established.
  - Ray ratio $0.812 \ge 0.80$, BBox margin $5.8\% \ge 5\%$.
  - Verdict: **PASS** ($g_{\mathrm{sample}} = 1$).

---

## 4. Trace Log Files

The complete machine-readable audit traces are available in:
- `artifacts/icassp2027/repair_traces/repair_audit_summary.json`
- `artifacts/icassp2027/repair_traces/trace_case1_underexposure.json`
- `artifacts/icassp2027/repair_traces/trace_case2_ground_intersection.json`
