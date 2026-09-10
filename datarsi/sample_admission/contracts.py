"""Deterministic Sample Contract implementation.

Evaluates synthetic supervision samples before admission into candidate training.
"""
from dataclasses import dataclass
from typing import Dict, Any, Tuple


@dataclass
class ContractConfig:
    min_bbox_margin: float = 0.05
    min_mask_coverage: float = 0.01
    ray_grid_resolution: int = 96
    min_ray_ratio: float = 0.80
    disallow_mesh_intersection: bool = True


def evaluate_sample_contract(
    metrics: Dict[str, Any],
    config: ContractConfig = ContractConfig()
) -> Tuple[bool, Dict[str, bool]]:
    """Evaluate deterministic sample admission contract g_sample(x; Gamma).

    Args:
        metrics: Dictionary containing measured geometric properties:
            - bbox_margin: minimum distance to image borders [0, 1]
            - mask_coverage: foreground area ratio [0, 1]
            - visible_amodal_ray_ratio: ratio of visible to amodal rays on 96x96 grid
            - mesh_intersection: boolean flag indicating support plane penetration
        config: Contract thresholds and parameters.

    Returns:
        (is_admitted, check_details)
    """
    checks = {
        'bbox_margin_pass': metrics.get('bbox_margin', 0.0) >= config.min_bbox_margin,
        'mask_coverage_pass': metrics.get('mask_coverage', 0.0) >= config.min_mask_coverage,
        'ray_ratio_pass': metrics.get('visible_amodal_ray_ratio', 0.0) >= config.min_ray_ratio,
        'no_intersection_pass': not metrics.get('mesh_intersection', False) if config.disallow_mesh_intersection else True
    }
    admitted = all(checks.values())
    return admitted, checks
