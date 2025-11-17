import asyncio
from typing import List
from models import CompanyData, ValidationResult
from sub_agents.shared.validator.agent import validate_company


async def validate_company_async(company: CompanyData) -> ValidationResult:
    """Async wrapper for company validation."""
    return validate_company(company)


async def orchestrate_research(companies: List[CompanyData]) -> List[ValidationResult]:
    """Execute validation pipelines in parallel for all companies."""
    validation_tasks = [validate_company_async(company) for company in companies]
    results = await asyncio.gather(*validation_tasks, return_exceptions=True)
    
    # Filter out exceptions and return valid results
    valid_results = []
    for result in results:
        if isinstance(result, ValidationResult):
            valid_results.append(result)
    
    return valid_results
