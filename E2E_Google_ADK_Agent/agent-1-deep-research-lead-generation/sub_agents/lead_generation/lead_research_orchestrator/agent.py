import asyncio
from typing import List
from models import LeadData, LeadAnalysisResult, ValidationResult, SignalAnalysis
from sub_agents.shared.validator.agent import validate_company
from sub_agents.lead_generation.signal_analyzer.agent import analyze_signals


async def analyze_lead_async(lead: LeadData) -> LeadAnalysisResult:
    """Run validator and signal analyzer in parallel for a single lead."""
    validation_task = asyncio.to_thread(validate_company, lead.company)
    signals_task = asyncio.to_thread(analyze_signals, lead)
    
    validation, signals = await asyncio.gather(validation_task, signals_task)
    
    return LeadAnalysisResult(
        lead=lead,
        validation=validation,
        signals=signals
    )


async def orchestrate_lead_research(leads: List[LeadData]) -> List[LeadAnalysisResult]:
    """Execute analysis pipelines in parallel for all leads."""
    analysis_tasks = [analyze_lead_async(lead) for lead in leads]
    results = await asyncio.gather(*analysis_tasks, return_exceptions=True)
    
    valid_results = []
    for result in results:
        if isinstance(result, LeadAnalysisResult):
            valid_results.append(result)
    
    return valid_results
