"""Compile downstream localized weaknesses into registered executable 3D synthesis requests."""
from typing import List, Dict, Any, Tuple


def compile_synthesis_requests(
    cells: List[Tuple[int, int]],
    identities: List[str],
    distances: List[float],
    budget: int = 72,
    allocation: str = 'targeted'
) -> List[Dict[str, Any]]:
    """Compile registered 3D requests Q = Alloc_Gamma(W, M).

    Args:
        cells: List of (azimuth, elevation) tuples.
        identities: List of authored 3D asset IDs.
        distances: List of orbit distance scales (meters).
        budget: Total request quota M (default: 72).
        allocation: 'targeted' or 'uniform'.

    Returns:
        List of registered synthesis request dictionaries.
    """
    requests = []
    req_idx = 1
    
    if allocation == 'targeted':
        # Allocate across identities, weak cells, and distances
        for ident in identities:
            for az, el in cells:
                for dist in distances:
                    if len(requests) >= budget:
                        break
                    requests.append({
                        'request_id': f'req_{allocation}_{req_idx:03d}',
                        'identity_id': ident,
                        'azimuth_deg': az,
                        'elevation_deg': el,
                        'distance_m': dist,
                        'source_pose': {'azimuth_deg': 0, 'elevation_deg': 0, 'distance_m': 4.0},
                        'allocation_mode': 'targeted',
                        'target_cell': f'({az}, {el})'
                    })
                    req_idx += 1
    else:
        # Uniform allocation across available factor space
        for ident in identities:
            for az, el in cells:
                if len(requests) >= budget:
                    break
                requests.append({
                    'request_id': f'req_{allocation}_{req_idx:03d}',
                    'identity_id': ident,
                    'azimuth_deg': az,
                    'elevation_deg': el,
                    'distance_m': 4.0,
                    'source_pose': {'azimuth_deg': 0, 'elevation_deg': 0, 'distance_m': 4.0},
                    'allocation_mode': 'uniform',
                    'target_cell': f'({az}, {el})'
                })
                req_idx += 1
                
    return requests[:budget]
