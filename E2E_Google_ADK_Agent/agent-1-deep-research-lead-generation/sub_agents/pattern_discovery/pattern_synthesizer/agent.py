from google import genai
from google.genai import types
from config import GEN_ADVANCED_MODEL
from models import PatternReport, SuccessPattern
from typing import Dict, Any, List
import json

PATTERN_SYNTHESIZER_PROMPT = """You are a pattern analysis expert. Your task is to identify common success patterns across validated companies.

Analyze the provided companies and identify:
1. Common business models or strategies
2. Shared market positioning approaches
3. Similar growth trajectories or milestones
4. Common technology or operational patterns
5. Shared customer acquisition strategies

Return a JSON object with:
- patterns: array of pattern objects, each with:
  - pattern_id: unique string identifier
  - description: clear description
  - frequency: integer (how many companies exhibit this)
  - confidence_score: float 0-1
  - supporting_companies: array of company names
  - evidence: array of specific evidence examples
  - sources: array of source citations
- total_companies_analyzed: integer
- analysis_methodology: string describing approach
- confidence_level: string (High/Medium/Low)"""


def synthesize_patterns(consolidated_data: Dict[str, Any]) -> PatternReport:
    client = genai.Client()
    
    companies = consolidated_data.get("consolidated_data", {}).get("companies", [])
    
    if not companies:
        return PatternReport(
            patterns=[],
            total_companies_analyzed=0,
            analysis_methodology="No valid companies to analyze",
            confidence_level="N/A"
        )
    
    companies_summary = "\n".join([
        f"- {c.name}: {c.description} (Industry: {c.industry}, Country: {c.country})"
        for c in companies
    ])
    
    prompt = f"""{PATTERN_SYNTHESIZER_PROMPT}

Companies analyzed ({len(companies)} total):
{companies_summary}

Generate pattern analysis report as JSON:"""
    
    response = client.models.generate_content(
        model=GEN_ADVANCED_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    
    data = json.loads(response.text)
    report = PatternReport(**data)
    report.total_companies_analyzed = len(companies)
    return report
