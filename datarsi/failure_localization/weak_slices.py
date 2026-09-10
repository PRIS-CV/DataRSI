"""Weak-slice localization over structured 3D factor space."""
from typing import Dict, List, Tuple

FROZEN_WEAK4_CELLS = [
    (135, 60),
    (225, -30),
    (135, -30),
    (225, 30)
]


def rank_cells_by_error(cell_errors: Dict[Tuple[int, int], float]) -> List[Tuple[Tuple[int, int], float]]:
    """Rank azimuth-elevation cells by descending diagnostic error order."""
    return sorted(cell_errors.items(), key=lambda x: x[1], reverse=True)


def localize_weak_slices(
    cell_errors: Dict[Tuple[int, int], float],
    k: int = 4
) -> List[Tuple[int, int]]:
    """Extract top-K weak slice cells from diagnostic failure profile S_0^diag."""
    ranked = rank_cells_by_error(cell_errors)
    return [cell for cell, _ in ranked[:k]]
