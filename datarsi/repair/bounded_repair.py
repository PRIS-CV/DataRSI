"""Bounded environment repair policy for synthetic supervision candidates."""
from typing import Dict, Any, Optional, Set


def compute_repair_action(
    contract_checks: Dict[str, bool],
    defects: Set[str],
    attempt: int
) -> Optional[Dict[str, float]]:
    """Compute bounded environment repair adjustment under registered policy.

    Args:
        contract_checks: Results from deterministic contract evaluation.
        defects: Set of defect tags from multimodal inspector.
        attempt: Repair attempt counter (1 or 2; <= 2 allowed).

    Returns:
        Adjustment parameters dict (lift, ev) or None if ineligible.
    """
    if attempt not in (1, 2):
        return None  # Repair budget exhausted
        
    # Hard geometry check failures are non-repairable
    if not contract_checks.get('bbox_margin_pass', True):
        return None
        
    # Ineligible defects cannot be repaired via staging/radiometric adjustments
    ineligible = {'clipping', 'identity_error', 'other_geometry_error'}
    if defects & ineligible:
        return None
        
    # Conflicting exposure diagnoses cannot be reconciled
    if {'underexposure', 'overexposure'} <= defects:
        return None
        
    lift = 0.0
    if defects & {'ground_occlusion', 'ground_intersection'}:
        lift = 0.25 if attempt == 1 else 0.50
        
    ev = 0.0
    if defects & {'underexposure', 'overexposure'}:
        magnitude = 0.50 if attempt == 1 else 1.00
        ev = magnitude if 'underexposure' in defects else -magnitude
        
    if lift == 0.0 and ev == 0.0:
        return None
        
    return {'lift': lift, 'ev': ev}
