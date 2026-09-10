"""Evaluation metrics and reporting utilities."""
from typing import List, Dict, Any
import statistics as st

def aggregate_paired_metrics(
    uniform_values: List[float],
    targeted_values: List[float]
) -> Dict[str, float]:
    """Compute paired contrast statistics (mean, sample std)."""
    deltas = [t - u for u, t in zip(uniform_values, targeted_values)]
    return {
        'mean_delta': st.fmean(deltas),
        'sample_std': st.stdev(deltas) if len(deltas) > 1 else 0.0,
        'count': len(deltas)
    }
