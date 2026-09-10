"""Diagnostic evaluator for failure profiling across factor space."""
from typing import Dict, Tuple, List, Any


def compute_slice_profile(
    predictions: List[Dict[str, Any]],
    factor_cells: List[Tuple[int, int]]
) -> Dict[Tuple[int, int], float]:
    """Compute slice failure profile S_0^diag from predictions over cells C."""
    cell_totals = {c: 0.0 for c in factor_cells}
    cell_counts = {c: 0 for c in factor_cells}
    
    for p in predictions:
        cell = (p['azimuth_deg'], p['elevation_deg'])
        if cell in cell_totals:
            cell_totals[cell] += p.get('rotation_error_deg', 0.0)
            cell_counts[cell] += 1
            
    return {
        c: (cell_totals[c] / cell_counts[c]) if cell_counts[c] > 0 else 0.0
        for c in factor_cells
    }
