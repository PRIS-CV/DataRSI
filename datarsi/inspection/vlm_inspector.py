"""Multimodal inspection provider for defect diagnosis on synthetic candidate renders."""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

INSPECTION_RUBRIC = (
    "Inspect SOURCE and TARGET renders of the same authored object. "
    "Diagnose visible defects only: ground_occlusion, ground_intersection, "
    "underexposure, overexposure, clipping, identity_error, other_geometry_error. "
    "Valid intended perspective or an occlusion already present in the requested "
    "scene is not automatically a defect. Return JSON with defects, evidence, uncertain."
)

ELIGIBLE_REPAIR_DEFECTS = {'underexposure', 'overexposure', 'ground_occlusion', 'ground_intersection'}
INELIGIBLE_DEFECTS = {'clipping', 'identity_error', 'other_geometry_error'}


@dataclass
class InspectionResult:
    defects: List[str]
    evidence: str
    uncertain: bool
    is_repair_eligible: bool


def parse_inspection_response(response: Dict[str, Any]) -> InspectionResult:
    """Parse multimodal inspector response into typed inspection result."""
    defects = response.get('defects', [])
    evidence = response.get('evidence', '')
    uncertain = response.get('uncertain', False)
    
    defect_set = set(defects)
    eligible = bool(defect_set & ELIGIBLE_REPAIR_DEFECTS) and not bool(defect_set & INELIGIBLE_DEFECTS)
    
    return InspectionResult(
        defects=defects,
        evidence=evidence,
        uncertain=uncertain,
        is_repair_eligible=eligible
    )
