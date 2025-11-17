import asyncio
from models import PatternReport, LeadReport
from sub_agents.lead_generation.lead_finder.agent import find_leads
from sub_agents.lead_generation.lead_formatter.agent import format_leads
from sub_agents.lead_generation.lead_research_orchestrator.agent import orchestrate_lead_research
from sub_agents.lead_generation.report_orchestrator.agent import consolidate_lead_data
from sub_agents.lead_generation.report_compiler.agent import compile_report


async def run_lead_generation(pattern_report: PatternReport) -> LeadReport:
    """Execute the complete Lead Generation workflow."""
    
    # Step 1: Find leads
    print(f"🔍 Finding leads based on {len(pattern_report.patterns)} patterns...")
    raw_leads = find_leads(pattern_report)
    
    # Step 2: Format leads
    pattern_ids = [p.pattern_id for p in pattern_report.patterns]
    print(f"📋 Formatting {len(raw_leads)} leads...")
    formatted_leads = format_leads(raw_leads, pattern_ids)
    
    if not formatted_leads:
        return LeadReport(
            executive_summary="No leads found matching the patterns.",
            total_leads_found=0,
            high_priority_leads=[],
            medium_priority_leads=[],
            pattern_match_analysis={},
            recommendations=[],
            methodology_notes="No leads to analyze"
        )
    
    # Step 3: Lead research orchestration (parallel validation + analysis)
    print(f"✅ Analyzing {len(formatted_leads)} leads in parallel...")
    analysis_results = await orchestrate_lead_research(formatted_leads)
    
    # Step 4: Consolidate results
    print(f"🔄 Consolidating analysis results...")
    consolidated_data = consolidate_lead_data(analysis_results)
    
    # Step 5: Compile report
    print(f"📊 Compiling final report...")
    lead_report = compile_report(consolidated_data)
    
    return lead_report


def lead_generation_workflow(pattern_report: PatternReport) -> LeadReport:
    """Synchronous wrapper for lead generation."""
    return asyncio.run(run_lead_generation(pattern_report))
