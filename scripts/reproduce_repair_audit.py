"""Reproduce sample repair audit statistics and inspect real trace cases."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACE_DIR = ROOT / 'artifacts' / 'icassp2027' / 'repair_traces'


def verify_repair_audit():
    with open(TRACE_DIR / 'repair_audit_summary.json', 'r', encoding='utf-8') as f:
        summary = json.load(f)
        
    print('=' * 75)
    print(f'DataRSI: {summary["study_title"]}')
    print('=' * 75)
    print(f'Scope: {summary["evaluation_scope"]}')
    print(f'Note:  {summary["audit_note"]}')
    print('-' * 75)
    print(f'Total Registered Candidates:     {summary["total_candidates"]}')
    print(f'Initially Passed:                {summary["initially_passed"]} ({summary["initial_pass_rate_pct"]}%)')
    print(f'Initially Failed:                {summary["initially_failed"]} ({summary["initial_defect_rate_pct"]}%)')
    print(f'Repair-Eligible Defects:         {summary["repair_eligible_defects"]}')
    print(f'Successfully Recovered (<= 2 r): {summary["successfully_recovered"]}')
    print(f'Final Compliant Samples:         {summary["final_compliant_samples"]} / {summary["total_candidates"]} ({summary["final_compliance_rate_pct"]}%)')
    print('=' * 75)
    
    print('\nExamining Trace Case 1 (Underexposure -> Radiometric EV Tuning):')
    with open(TRACE_DIR / 'trace_case1_underexposure.json', 'r', encoding='utf-8') as f:
        c1 = json.load(f)
    print(f'  - Asset: {c1["identity"]}, Coordinates: {c1["coordinates"]}')
    print(f'  - Diagnosed Defect: {c1["initial_render"]["vlm_inspection"]["defects"]}')
    print(f'  - Action: {c1["repair_round_1"]["action"]}')
    print(f'  - Outcome: {c1["final_verdict"]}')
    
    print('\nExamining Trace Case 2 (Ground Intersection -> Support Staging Lift):')
    with open(TRACE_DIR / 'trace_case2_ground_intersection.json', 'r', encoding='utf-8') as f:
        c2 = json.load(f)
    print(f'  - Asset: {c2["identity"]}, Coordinates: {c2["coordinates"]}')
    print(f'  - Diagnosed Defect: {c2["initial_render"]["vlm_inspection"]["defects"]}')
    print(f'  - Action: {c2["repair_round_1"]["action"]}')
    print(f'  - Outcome: {c2["final_verdict"]}')
    print('=' * 75)


if __name__ == '__main__':
    verify_repair_audit()
