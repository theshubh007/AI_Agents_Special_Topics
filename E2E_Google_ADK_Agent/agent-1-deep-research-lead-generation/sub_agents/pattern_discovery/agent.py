import asyncio
from models import IntentExtractionResult, PatternReport
from sub_agents.pattern_discovery.company_finder.agent import find_companies
from sub_agents.pattern_discovery.company_formatter.agent import format_companies
from sub_agents.pattern_discovery.research_orchestrator.agent import orchestrate_research
from sub_agents.pattern_discovery.synthesizer_orchestrator.agent import consolidate_research_data
from sub_agents.pattern_discovery.pattern_synthesizer.agent import synthesize_patterns


async def run_pattern_discovery(intent: IntentExtractionResult) -> PatternReport:
    """Execute the complete Pattern Discovery workflow."""
    
    # Step 1: Find companies
    print(f"🔍 Finding companies in {intent.industry} ({intent.country})...")
    raw_companies = find_companies(intent)
    
    # Step 2: Format companies
    print(f"📋 Formatting {len(raw_companies)} companies...")
    formatted_companies = format_companies(raw_companies)
    
    if not formatted_companies:
        return PatternReport(
            patterns=[],
            total_companies_analyzed=0,
            analysis_methodology="No companies found",
            confidence_level="N/A"
        )
    
    # Step 3: Research orchestration (parallel validation)
    print(f"✅ Validating {len(formatted_companies)} companies in parallel...")
    validation_results = await orchestrate_research(formatted_companies)
    
    # Step 4: Synthesize data
    print(f"🔄 Consolidating validation results...")
    consolidated_data = consolidate_research_data(validation_results)
    
    # Step 5: Pattern synthesis
    print(f"🎯 Synthesizing patterns from {consolidated_data['total_analyzed']} companies...")
    pattern_report = synthesize_patterns(consolidated_data)
    
    return pattern_report


def pattern_discovery_workflow(intent: IntentExtractionResult) -> PatternReport:
    """Synchronous wrapper for pattern discovery."""
    return asyncio.run(run_pattern_discovery(intent))
