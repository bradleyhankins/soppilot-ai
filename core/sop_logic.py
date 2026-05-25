def clean_steps(steps: str) -> list[str]:
    cleaned = [step.strip(" -•\t") for step in steps.splitlines() if step.strip()]
    return cleaned or [
        "Confirm the process trigger and required information",
        "Gather necessary tools, documents, or context",
        "Complete the process according to company standards",
        "Document the completed work",
        "Review for accuracy and escalate issues if needed",
    ]


def determine_complexity(frequency: str, risk: str, team_size: str) -> tuple[str, str, int]:
    score = {"Daily": 3, "Weekly": 2, "Monthly": 1, "Rarely / As Needed": 1}.get(frequency, 1)
    score += {"High": 3, "Medium": 2, "Low": 1}.get(risk, 1)
    score += {"1-3 people": 1, "4-10 people": 2, "11+ people": 3}.get(team_size, 1)
    if score >= 8:
        return "High Complexity", "Use a detailed SOP, training checklist, quality checks, manager review, and clear escalation path.", score
    if score >= 5:
        return "Medium Complexity", "Use a clear SOP, checklist, basic quality standards, and routine spot checks.", score
    return "Low Complexity", "A simple SOP and checklist should be enough for this process.", score


def role_guidance(owner_role: str) -> str:
    return {
        "Sales Representative": "Keep the process customer-facing and focused on communication, follow-up, and documentation.",
        "Sales Manager": "Include accountability checkpoints, coaching expectations, and measurable review standards.",
        "Operations Manager": "Include handoffs, documentation standards, quality checks, and escalation paths.",
        "Project Manager": "Focus on readiness, communication, documentation, and completion standards.",
        "Customer Service Representative": "Emphasize response time, notes, issue resolution, and customer experience.",
        "Recruiter / Hiring Manager": "Include review steps, documentation, interview consistency, and next-step ownership.",
        "General Team Member": "Use simple step-by-step instructions that are easy to follow and repeat.",
    }.get(owner_role, "Use simple step-by-step instructions that are easy to follow and repeat.")


def role_quality_standards(owner_role: str) -> list[str]:
    return {
        "Sales Representative": ["Customer contact attempts are documented", "Next step is clear", "Follow-up task is created when needed", "Communication is professional and timely"],
        "Sales Manager": ["Rep activity is reviewed", "Coaching notes are documented", "Accountability expectations are clear", "Performance issue has a next action"],
        "Operations Manager": ["Handoff is complete", "Owner is clear", "System notes are accurate", "Escalations are documented"],
        "Project Manager": ["Job status is accurate", "Customer/internal updates are documented", "Issues are escalated quickly", "Completion standard is verified"],
        "Customer Service Representative": ["Customer concern is documented", "Response is timely", "Resolution or next step is clear", "Escalation happens when needed"],
        "Recruiter / Hiring Manager": ["Status is updated", "Notes are complete", "Next step is documented", "Review criteria are consistent"],
        "General Team Member": ["Steps are completed in order", "Documentation is clear", "Issues are escalated", "Final outcome is reviewed"],
    }.get(owner_role, ["Steps are completed in order", "Documentation is clear", "Issues are escalated", "Final outcome is reviewed"])


def missing_info_check(process: dict) -> list[str]:
    checks = {
        "Process name is missing.": process["process_name"],
        "Process trigger is missing.": process["trigger"],
        "Process goal is missing.": process["goal"],
        "Required inputs/information are missing.": process["inputs"],
        "Tools or systems are missing.": process["tools"],
        "Rough process steps are missing.": process["steps"],
        "Quality standard is missing.": process["quality"],
        "Escalation path is missing.": process["escalation"],
    }
    missing = [message for message, value in checks.items() if not str(value).strip()]
    return missing or ["No major missing information found."]


def process_risk_diagnosis(process: dict, missing_items: list[str]) -> tuple[str, str]:
    real_missing_count = len([item for item in missing_items if item != "No major missing information found."])
    if process["risk"] == "High" and real_missing_count >= 3:
        return "High Documentation Risk", "This process has high business risk and several missing details. Review with a manager before rollout."
    if process["risk"] == "High":
        return "High Operational Risk", "This process has high risk if completed incorrectly. Add quality control, manager review, and escalation steps."
    if real_missing_count >= 4:
        return "Incomplete Process Definition", "Several important details are missing. Complete the SOP before team rollout."
    if process["frequency"] == "Daily" and process["team_size"] in ["4-10 people", "11+ people"]:
        return "Consistency Risk", "This process happens often and is used by multiple people. Clear documentation prevents process drift."
    return "Standard Process Risk", "The process appears suitable for a standard SOP, checklist, and basic manager review."


def readiness_status(complexity: str, missing_items: list[str], risk_label: str) -> tuple[str, str]:
    real_missing = [item for item in missing_items if item != "No major missing information found."]
    if real_missing:
        return "Needs Completion", "Complete missing details before publishing this SOP."
    if risk_label in ["High Documentation Risk", "High Operational Risk"] or complexity == "High Complexity":
        return "Manager Review Recommended", "The SOP is usable, but should be reviewed by a manager before rollout."
    return "Ready for Team Review", "The SOP is ready to review with the team and test in live workflow."


def documentation_readiness_score(process: dict, complexity_score: int, missing_items: list[str], risk_label: str) -> int:
    score = 100
    real_missing_count = len([item for item in missing_items if item != "No major missing information found."])
    score -= real_missing_count * 10
    score -= max(complexity_score - 5, 0) * 3
    if risk_label in ["High Documentation Risk", "High Operational Risk"]:
        score -= 10
    if not process["escalation"].strip():
        score -= 8
    return max(min(score, 100), 0)


def readiness_score_status(score: int) -> str:
    if score >= 85:
        return "Ready for Manager Review"
    if score >= 70:
        return "Needs Light Cleanup"
    return "Needs More Detail"


def improvement_recommendations(complexity: str, risk_level: str, missing_items: list[str]) -> list[str]:
    recs = []
    if [item for item in missing_items if item != "No major missing information found."]:
        recs.append("Complete missing process details before publishing the SOP.")
    if complexity == "High Complexity":
        recs.append("Add manager review checkpoints and require sign-off during initial rollout.")
        recs.append("Use the training plan before allowing independent execution.")
    if risk_level == "High":
        recs.append("Add a clear escalation path and define what should stop the process.")
    recs.append("Review the SOP after the first week of use and update unclear steps.")
    recs.append("Assign one process owner responsible for keeping the SOP current.")
    return recs


def run_sop_workflow(process: dict) -> dict:
    complexity, complexity_note, complexity_score = determine_complexity(process["frequency"], process["risk"], process["team_size"])
    missing_items = missing_info_check(process)
    risk_label, risk_note = process_risk_diagnosis(process, missing_items)
    readiness, readiness_note = readiness_status(complexity, missing_items, risk_label)
    score = documentation_readiness_score(process, complexity_score, missing_items, risk_label)
    role_standards = role_quality_standards(process["owner_role"])
    recommendations = improvement_recommendations(complexity, process["risk"], missing_items)
    return {
        "complexity": complexity,
        "complexity_note": complexity_note,
        "complexity_score": complexity_score,
        "missing_items": missing_items,
        "risk_label": risk_label,
        "risk_note": risk_note,
        "readiness": readiness,
        "readiness_note": readiness_note,
        "score": score,
        "role_standards": role_standards,
        "recommendations": recommendations,
    }
