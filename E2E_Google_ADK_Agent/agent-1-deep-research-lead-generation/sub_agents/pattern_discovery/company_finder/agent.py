from google import genai
from google.genai import types
from config import GEN_FAST_MODEL
from models import IntentExtractionResult
from typing import List, Dict, Any

COMPANY_FINDER_PROMPT = """You are a company research specialist. Your task is to find successful companies based on the given criteria.

For the provided industry and country, identify 10-15 successful, well-established companies that represent the best examples in that market.

Focus on:
- Companies with proven track records
- Market leaders or notable players
- Companies with publicly available information
- Diverse range within the industry

Return a list of companies with basic information: name, brief description, and why they're successful."""


def find_companies(intent: IntentExtractionResult) -> List[Dict[str, Any]]:
    client = genai.Client()
    
    prompt = f"""{COMPANY_FINDER_PROMPT}

Industry: {intent.industry}
Country: {intent.country}
User Intent: {intent.user_intent}

Provide a JSON array of companies with fields: name, description, success_factors, website (if known)."""
    
    response = client.models.generate_content(
        model=GEN_FAST_MODEL,
        contents=prompt
    )
    
    # Parse the response - in real implementation, this would use structured output
    import json
    try:
        # Try to extract JSON from response
        text = response.text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        return json.loads(text.strip())
    except:
        # Fallback: return mock data structure
        return []
