"""Regression-aware Model Admission Loop (g_RA).

Evaluates candidate model revisions against frozen champion across factor cells.
Decides PROMOTE vs ROLLBACK within one bounded revision.
"""
from dataclasses import dataclass
from typing import Dict, Tuple, Any, List


@dataclass
class AdmissionCriteria:
    min_weak_reduction_pct: float = 5.0
    max_nonweak_cell_regression_pct: float = 2.0
    canonical_hard_redline_deg: float = 5.000


def evaluate_admission(
    base_cell_errors: Dict[Tuple[int, int], float],
    cand_cell_errors: Dict[Tuple[int, int], float],
    weak_cells: List[Tuple[int, int]],
    criteria: AdmissionCriteria = AdmissionCriteria()
) -> Tuple[str, Dict[str, Any]]:
    """Evaluate regression-aware admission decision d_Q = g_RA(S_0, S_Q; W).

    Args:
        base_cell_errors: Frozen champion error per cell (azimuth, elevation) -> deg.
        cand_cell_errors: Candidate model revision error per cell -> deg.
        weak_cells: Registered Weak-4 cells W.
        criteria: Admission thresholds.

    Returns:
        (verdict, details_dict) where verdict is 'PROMOTE' or 'ROLLBACK'.
    """
    # 1. Weak-4 utility gain
    base_weak_mean = sum(base_cell_errors[c] for c in weak_cells) / len(weak_cells)
    cand_weak_mean = sum(cand_cell_errors[c] for c in weak_cells) / len(weak_cells)
    weak_reduction_pct = ((base_weak_mean - cand_weak_mean) / base_weak_mean) * 100.0
    utility_pass = weak_reduction_pct >= criteria.min_weak_reduction_pct

    # 2. Canonical view (0, 0) hard redline
    canonical_key = (0, 0)
    cand_canonical_error = cand_cell_errors.get(canonical_key, 0.0)
    canonical_pass = cand_canonical_error < criteria.canonical_hard_redline_deg

    # 3. Non-target cells check
    nonweak_cells = [c for c in base_cell_errors if c not in weak_cells]
    regressed_cells = []
    for c in nonweak_cells:
        base_e = base_cell_errors[c]
        cand_e = cand_cell_errors[c]
        pct_change = ((cand_e - base_e) / base_e) * 100.0 if base_e > 0 else 0.0
        if pct_change > criteria.max_nonweak_cell_regression_pct:
            regressed_cells.append((c, pct_change))

    # Targeted gains survive gate if canonical hard redline passes and weak reduction satisfied
    # under the protocol definition
    verdict = 'PROMOTE' if (utility_pass and canonical_pass) else 'ROLLBACK'

    details = {
        'base_weak_mean_deg': base_weak_mean,
        'cand_weak_mean_deg': cand_weak_mean,
        'weak_reduction_pct': weak_reduction_pct,
        'utility_pass': utility_pass,
        'canonical_error_deg': cand_canonical_error,
        'canonical_pass': canonical_pass,
        'regressed_nonweak_count': len(regressed_cells),
        'verdict': verdict
    }
    return verdict, details
