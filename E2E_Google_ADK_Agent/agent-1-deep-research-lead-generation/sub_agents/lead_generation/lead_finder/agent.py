from google import genai
from config import GEN_FAST_MODEL
from models import PatternReport
from typing import List, Dict, Any
import json

LEAD_FINDER_PROMPT = """You are a lead discovery specialist. Your task is to find companies that match the success patterns identified in the pattern report.

Use the patterns to construct targeted searches for similar companies. Look for:
- Companies exhibiting similar characteristics
- Businesses in related markets or adjacent industries
- Organizations showing similar growth indicators
- Companies with comparable business models

Return 20-30 potential leads with basic information."""


def find_leads(pattern_report: PatternReport) -> List[Dict[str, Any]]:
    client = genai.Client()
    
    patterns_summary = "\n".join([
        f"- {p.description} (Confidence: {p.confidence_score}, Frequency: {p.frequency})"
        for p in pattern_report.patterns
    ])
    
    prompt = f"""{LEAD_FINDER_PROMPT}

Success Patterns Identified:
{patterns_summary}

Total companies analyzed: {pattern_report.total_companies_analyzed}

Find potential leads matching these patterns. Return JSON array with fields: name, description, industry, country, website, matching_pattern_ids (array of strings like ["pattern_1", "pattern_2"])."""
    
    response = client.models.generate_content(
        model=GEN_FAST_MODEL,
        contents=prompt
    )
    
    try:
        text = response.text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        return json.loads(text.strip())
    except:
        return []
