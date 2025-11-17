from google import genai
from google.genai import types
from config import GEN_FAST_MODEL
from models import CompanyData, ValidationResult
import json

VALIDATOR_PROMPT = """You are a company validation specialist. Your task is to verify if a company meets quality criteria.

Evaluate the company on:
1. Business legitimacy (is this a real, operating company?)
2. Industry classification accuracy
3. Geographic location confirmation
4. Data completeness
5. Success indicators presence

Return ONLY a JSON object with:
- is_valid: boolean (true if company passes validation)
- validation_score: float 0-1 (confidence in validation)
- validation_details: object with scores for each criterion
- rejection_reasons: array of strings or null (if invalid, why?)

Example:
{
  "is_valid": true,
  "validation_score": 0.85,
  "validation_details": {"legitimacy": 0.9, "accuracy": 0.8},
  "rejection_reasons": null
}"""


def validate_company(company: CompanyData) -> ValidationResult:
    client = genai.Client()
    
    prompt = f"""{VALIDATOR_PROMPT}

Company to validate:
Name: {company.name}
Industry: {company.industry}
Country: {company.country}
Description: {company.description}
Website: {company.website}

Provide validation assessment as JSON:"""
    
    response = client.models.generate_content(
        model=GEN_FAST_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    
    data = json.loads(response.text)
    result = ValidationResult(company=company, **data)
    return result
