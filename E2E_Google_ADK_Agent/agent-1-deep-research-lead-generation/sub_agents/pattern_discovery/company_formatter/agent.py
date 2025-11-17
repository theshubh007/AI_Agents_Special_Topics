from typing import List, Dict, Any
from models import CompanyData

def format_companies(raw_companies: List[Dict[str, Any]]) -> List[CompanyData]:
    """Transform raw company data into standardized CompanyData objects."""
    formatted = []
    seen_names = set()
    
    for raw in raw_companies:
        name = raw.get("name", "").strip()
        
        # Deduplication
        if not name or name.lower() in seen_names:
            continue
        
        seen_names.add(name.lower())
        
        company = CompanyData(
            name=name,
            industry=raw.get("industry", ""),
            country=raw.get("country", ""),
            website=raw.get("website"),
            description=raw.get("description", ""),
            metadata={
                "success_factors": raw.get("success_factors", []),
                "raw_data": raw
            }
        )
        formatted.append(company)
    
    return formatted
