from google import genai
from google.genai import types
from config import GEN_FAST_MODEL
from models import LeadData, SignalAnalysis
import json

SIGNAL_ANALYZER_PROMPT = """You are a lead signal analysis expert. Your task is to identify success signals and growth indicators in potential leads.

Analyze the lead for:
1. Growth indicators (expansion, hiring, funding, new products)
2. Market positioning signals (awards, partnerships, media coverage)
3. Technology adoption patterns
4. Customer acquisition signals
5. Risk factors (financial issues, negative press, market challenges)

Return a JSON object with:
- detected_signals: array of specific signals found
- signal_strength: object mapping signal types to strength scores (0-1)
- growth_indicators: array of positive growth signs
- risk_factors: array of potential concerns
- recommendation_score: float 0-1 for pursuing this lead"""


def analyze_signals(lead: LeadData) -> SignalAnalysis:
    client = genai.Client()
    
    prompt = f"""{SIGNAL_ANALYZER_PROMPT}

Lead to analyze:
Company: {lead.company.name}
Industry: {lead.company.industry}
Country: {lead.company.country}
Description: {lead.company.description}
Match Score: {lead.match_score}
Matching Patterns: {', '.join(lead.matching_patterns)}

Provide signal analysis as JSON:"""
    
    response = client.models.generate_content(
        model=GEN_FAST_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    
    data = json.loads(response.text)
    result = SignalAnalysis(lead=lead, **data)
    return result
