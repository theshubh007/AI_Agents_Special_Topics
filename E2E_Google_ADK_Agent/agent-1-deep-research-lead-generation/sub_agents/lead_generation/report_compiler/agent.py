from google import genai
from google.genai import types
from config import GEN_ADVANCED_MODEL
from models import LeadReport
from typing import Dict, Any
import json

REPORT_COMPILER_PROMPT = """You are a lead generation report specialist. Your task is to compile a comprehensive lead report.

Create an executive summary highlighting:
- Total leads found and analyzed
- Key findings and patterns
- Quality distribution of leads

Return a JSON object with:
- executive_summary: string with key highlights
- total_leads_found: integer (will be set by system)
- high_priority_leads: array (will be set by system)
- medium_priority_leads: array (will be set by system)
- pattern_match_analysis: object showing which patterns were most common
- recommendations: array of actionable recommendations for sales team
- methodology_notes: string explaining the analysis process"""


def compile_report(consolidated_data: Dict[str, Any]) -> LeadReport:
    client = genai.Client()
    
    high_priority = consolidated_data.get("high_priority", [])
    medium_priority = consolidated_data.get("medium_priority", [])
    
    summary = f"""
Total leads analyzed: {consolidated_data.get('total_analyzed', 0)}
Valid leads: {consolidated_data.get('total_valid', 0)}
High priority: {len(high_priority)}
Medium priority: {len(medium_priority)}

High Priority Leads:
{chr(10).join([f"- {r.lead.company.name}: {r.lead.company.description[:100]}" for r in high_priority[:5]])}
"""
    
    prompt = f"""{REPORT_COMPILER_PROMPT}

Lead Analysis Summary:
{summary}

Generate comprehensive lead report as JSON:"""
    
    response = client.models.generate_content(
        model=GEN_ADVANCED_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    
    data = json.loads(response.text)
    report = LeadReport(
        executive_summary=data.get("executive_summary", ""),
        total_leads_found=consolidated_data.get('total_valid', 0),
        high_priority_leads=high_priority,
        medium_priority_leads=medium_priority,
        pattern_match_analysis=data.get("pattern_match_analysis", {}),
        recommendations=data.get("recommendations", []),
        methodology_notes=data.get("methodology_notes", "")
    )
    
    return report
