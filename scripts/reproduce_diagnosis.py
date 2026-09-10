"""Reproduce failure localization over structured factor space."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEAK_FILE = ROOT / 'artifacts' / 'icassp2027' / 'requests' / 'weak4_cells.json'


def verify_diagnosis():
    with open(WEAK_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print('=' * 75)
    print('DataRSI: Failure Localization & Calibration Evidence')
    print('=' * 75)
    fs = data['factor_space']
    print(f'Structured Factor Space: A x H x R = {len(fs["azimuths_deg"])} x {len(fs["elevations_deg"])} x {len(fs["distance_scales_m"])} = {fs["total_views"]} views ({fs["total_cells"]} cells)')
    print('-' * 75)
    print('Diagnosed Weak-4 Cells (K=4 top failure slices):')
    for c in data['weak4_cells']:
        print(f'  - Cell: ({c["azimuth_deg"]} deg, {c["elevation_deg"]} deg) -> {c["name"]}')
    print('-' * 75)
    calib = data['calibration_evidence']
    print(f'Calibration Signal: Pooled rank correlation rho = {calib["pooled_rank_correlation_rho"]}')
    print(f'Weak-4 Agreement:  {calib["weak4_overlap"]}')
    print(f'GT Median Error:   {calib["median_gt_error_deg"]} deg (Acc@30: {calib["acc_30_pct"]}%)')
    print('=' * 75)


if __name__ == '__main__':
    verify_diagnosis()
