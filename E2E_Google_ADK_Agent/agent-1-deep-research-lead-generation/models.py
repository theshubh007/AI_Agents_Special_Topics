from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class IntentExtractionResult(BaseModel):
    industry: str
    country: str
    user_intent: str
    additional_criteria: Optional[Dict[str, Any]] = None


class CompanyData(BaseModel):
    name: str
    industry: str
    country: str
    website: Optional[str] = None
    description: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ValidationResult(BaseModel):
    company: CompanyData
    is_valid: bool
    validation_score: float
    validation_details: Dict[str, Any] = Field(default_factory=dict)
    rejection_reasons: Optional[List[str]] = None


class SuccessPattern(BaseModel):
    pattern_id: str
    description: str
    frequency: int
    confidence_score: float
    supporting_companies: List[str]
    evidence: List[str]
    sources: List[str]


class PatternReport(BaseModel):
    patterns: List[SuccessPattern]
    total_companies_analyzed: int
    analysis_methodology: str
    confidence_level: str


class LeadData(BaseModel):
    company: CompanyData
    match_score: float
    matching_patterns: List[str]
    discovery_source: str


class SignalAnalysis(BaseModel):
    lead: LeadData
    detected_signals: List[str]
    signal_strength: Dict[str, float]
    growth_indicators: List[str]
    risk_factors: List[str]
    recommendation_score: float


class LeadAnalysisResult(BaseModel):
    lead: LeadData
    validation: ValidationResult
    signals: SignalAnalysis


class LeadReport(BaseModel):
    executive_summary: str
    total_leads_found: int
    high_priority_leads: List[LeadAnalysisResult]
    medium_priority_leads: List[LeadAnalysisResult]
    pattern_match_analysis: Dict[str, Any]
    recommendations: List[str]
    methodology_notes: str


class SessionState(BaseModel):
    session_id: str
    current_stage: str = "intent"
    intent_data: Optional[IntentExtractionResult] = None
    pattern_report: Optional[PatternReport] = None
    lead_report: Optional[LeadReport] = None
    conversation_history: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
