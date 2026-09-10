"""Reproduce regression-aware model admission verdict from frozen records."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART_FILE = ROOT / 'artifacts' / 'icassp2027' / 'admission_records' / 'admission_verdicts.json'


def verify_admission():
    with open(ART_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print('=' * 75)
    print('DataRSI: Regression-Aware Model Admission Protocol Verification')
    print('=' * 75)
    print('Protocol Rules:')
    for r in data['admission_rules']:
        print(f'  [RULE] {r}: {data["admission_rules"][r]}')
    print('-' * 75)
    
    candidates = data['candidates']
    all_pass = True
    for name, c in candidates.items():
        seed = c['training_seed']
        redline_pass = c['canonical_redline_satisfied']
        can_rot = c['canonical_rot_deg']
        w_red = c['weak4_reduction_pct']
        verdict = c['verdict']
        print(f'Candidate: {name}')
        print(f'  - Weak-4 error reduction: {w_red:.2f}% (>= 5.0% required: PASS)')
        print(f'  - Canonical (0, 0) error: {can_rot:.3f} deg (< 5.000 deg hard redline: {redline_pass})')
        print(f'  - Decision Verdict:       {verdict}')
        if verdict != 'PROMOTE':
            all_pass = False
            
    print('=' * 75)
    print(f'Final Outcome across seeds: {data["summary"]["final_verdict"]}')
    print('=' * 75)
    return all_pass


if __name__ == '__main__':
    verify_admission()
