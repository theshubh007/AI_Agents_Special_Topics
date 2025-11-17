from google import genai
from google.genai import types
from config import GEN_FAST_MODEL
from models import IntentExtractionResult
import json

INTENT_EXTRACTOR_PROMPT = """You are an intent extraction specialist. Your job is to parse user requests for lead generation and extract structured information.

Extract the following from the user's request:
- industry: The target industry or business sector (e.g., "SaaS", "E-commerce", "FinTech")
- country: The target geographic location - can be a country, state, or region (e.g., "Germany", "California", "United States", "France")
- user_intent: A clear summary of what the user wants to achieve
- additional_criteria: Any extra requirements or preferences mentioned as a JSON object (optional, can be null)

IMPORTANT: 
- If a US state like "California" is mentioned, use it as the country field
- additional_criteria must be null or a JSON object (not a string)
- Be precise and thorough

Return ONLY a JSON object with these exact fields.

Example outputs:
{
  "industry": "SaaS",
  "country": "Germany",
  "user_intent": "Find successful SaaS companies for lead generation",
  "additional_criteria": null
}

{
  "industry": "E-commerce",
  "country": "California",
  "user_intent": "Find e-commerce businesses in California",
  "additional_criteria": null
}"""


def create_intent_extractor_agent():
    client = genai.Client()
    return client, INTENT_EXTRACTOR_PROMPT


def extract_intent(user_input: str) -> IntentExtractionResult:
    client, prompt = create_intent_extractor_agent()
    
    response = client.models.generate_content(
        model=GEN_FAST_MODEL,
        contents=f"{prompt}\n\nUser request: {user_input}\n\nProvide the JSON response:",
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    
    # Parse JSON response
    data = json.loads(response.text)
    return IntentExtractionResult(**data)
