def sop_enhancement_prompt(process: dict, full_package: str) -> str:
    return f"""
You are an operations documentation specialist.
Improve the SOP documentation package below while preserving the same structure and facts.
Do not invent policies, legal requirements, safety rules, HR rules, company-specific rules, pricing, or promises.
If information is missing, keep it as a missing information item.
Make the writing cleaner, more professional, and easier for a manager to use.

Process context:
{process}

Rules-based SOP package:
{full_package}
"""
