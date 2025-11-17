from typing import List, Dict, Any
from models import LeadData, CompanyData

def format_leads(raw_leads: List[Dict[str, Any]], pattern_ids: List[str]) -> List[LeadData]:
    """Standardize raw lead data into LeadData objects."""
    formatted = []
    seen_names = set()
    
    for raw in raw_leads:
        name = raw.get("name", "").strip()
        
        if not name or name.lower() in seen_names:
            continue
        
        seen_names.add(name.lower())
        
        company = CompanyData(
            name=name,
            industry=raw.get("industry", ""),
            country=raw.get("country", ""),
            website=raw.get("website"),
            description=raw.get("description", ""),
            metadata={"raw_data": raw}
        )
        
        # Get matching patterns and ensure they're strings
        matching_patterns_raw = raw.get("matching_pattern_ids", pattern_ids[:2])
        # Convert to strings if they're integers
        matching_patterns = [str(p) for p in matching_patterns_raw] if matching_patterns_raw else []
        match_score = len(matching_patterns) / max(len(pattern_ids), 1) if pattern_ids else 0.5
        
        lead = LeadData(
            company=company,
            match_score=match_score,
            matching_patterns=matching_patterns,
            discovery_source="pattern_based_search"
        )
        formatted.append(lead)
    
    return formatted
