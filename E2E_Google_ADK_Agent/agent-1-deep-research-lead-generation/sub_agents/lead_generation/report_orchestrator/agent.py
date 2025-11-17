from typing import List, Dict, Any
from models import LeadAnalysisResult


def consolidate_lead_data(analysis_results: List[LeadAnalysisResult]) -> Dict[str, Any]:
    """Consolidate all lead analysis results and rank by priority."""
    
    # Filter valid leads
    valid_leads = [r for r in analysis_results if r.validation.is_valid]
    
    # Sort by combined score
    def calculate_priority_score(result: LeadAnalysisResult) -> float:
        return (
            result.validation.validation_score * 0.3 +
            result.lead.match_score * 0.3 +
            result.signals.recommendation_score * 0.4
        )
    
    sorted_leads = sorted(valid_leads, key=calculate_priority_score, reverse=True)
    
    # Categorize
    high_priority = [r for r in sorted_leads if calculate_priority_score(r) >= 0.7]
    medium_priority = [r for r in sorted_leads if 0.5 <= calculate_priority_score(r) < 0.7]
    
    return {
        "all_leads": sorted_leads,
        "high_priority": high_priority,
        "medium_priority": medium_priority,
        "total_analyzed": len(analysis_results),
        "total_valid": len(valid_leads)
    }
