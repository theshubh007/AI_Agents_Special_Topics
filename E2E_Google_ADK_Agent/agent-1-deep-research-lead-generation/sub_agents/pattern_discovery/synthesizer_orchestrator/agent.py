from typing import List, Dict, Any
from models import ValidationResult


def consolidate_research_data(validation_results: List[ValidationResult]) -> Dict[str, Any]:
    """Gather and consolidate validated data from parallel pipelines."""
    valid_companies = [r for r in validation_results if r.is_valid]
    invalid_companies = [r for r in validation_results if not r.is_valid]
    
    return {
        "valid_companies": valid_companies,
        "invalid_companies": invalid_companies,
        "total_analyzed": len(validation_results),
        "validation_rate": len(valid_companies) / len(validation_results) if validation_results else 0,
        "consolidated_data": {
            "companies": [r.company for r in valid_companies],
            "validation_scores": [r.validation_score for r in valid_companies]
        }
    }
