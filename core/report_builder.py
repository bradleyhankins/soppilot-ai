from core.sop_logic import clean_steps, readiness_score_status, role_guidance


def version_control_block(process: dict, score: int) -> str:
    return f"""## Version Control
Version: 1.0
Owner: {process['owner_role']}
Department: {process['department']}
Last Reviewed: Generated Date
Next Review Date: 30 days after rollout
Documentation Readiness Score: {score}%
Status: {readiness_score_status(score)}
"""


def generate_sop(process: dict, role_standards: list[str], score: int) -> str:
    step_lines = "\n".join(f"{i}. {step}" for i, step in enumerate(clean_steps(process["steps"]), start=1))
    standards = "\n".join(f"- {standard}" for standard in role_standards)
    return f"""# {process['process_name']} SOP

{version_control_block(process, score)}
## Purpose
Create a consistent, repeatable process for **{process['process_name']}**.

## Process Goal
{process['goal'] or 'Ensure the process is completed accurately, consistently, and with clear documentation.'}

## When This Process Starts
{process['trigger'] or 'This process begins when the assigned team member identifies that the task needs to be completed.'}

## Inputs / Information Needed
{process['inputs'] or 'Required customer, project, task, or internal information should be gathered before starting.'}

## Tools / Systems Used
{process['tools'] or 'Relevant CRM, spreadsheet, communication platform, document system, or internal tool.'}

## Role-Specific Guidance
{role_guidance(process['owner_role'])}

## Standard Procedure
{step_lines}

## Role-Specific Quality Standards
{standards}

## Quality Standard
{process['quality'] or 'The process should be completed accurately, documented clearly, and reviewed for completeness before being considered finished.'}

## Escalation Path
{process['escalation'] or 'If the team member cannot complete the process or identifies an issue, they should escalate to the appropriate manager or process owner.'}

## Completion Definition
This process is complete when:
- Required steps have been completed
- Required notes or documentation have been entered
- Any customer/internal communication has been completed
- Issues have been escalated if needed
- The process owner can verify completion
"""


def generate_checklist(process: dict, role_standards: list[str]) -> str:
    steps = "\n".join(f"- [ ] {item}" for item in clean_steps(process["steps"]))
    standards = "\n".join(f"- [ ] {standard}" for standard in role_standards)
    return f"# {process['process_name']} Checklist\n\n## Process Steps\n{steps}\n\n## Role-Specific Quality Checks\n{standards}\n\n## Final Quality Check\n- [ ] Information is complete\n- [ ] Notes are clear\n- [ ] Required communication is complete\n- [ ] Process outcome matches expected standard\n- [ ] Issues were escalated if needed\n"


def generate_training_plan(process: dict, complexity: str) -> str:
    practice = "\n".join(f"- {item}" for item in clean_steps(process["steps"])[:5])
    count = "3 times" if complexity == "High Complexity" else "2 times"
    return f"# {process['process_name']} Training Plan\n\n## Target Role\n{process['owner_role']}\n\n## Training Goal\nTrain the team member to complete this process consistently, accurately, and with proper documentation.\n\n## Training Structure\n1. Explain the why\n2. Walk through the SOP\n3. Demonstrate the process\n4. Guided practice\n5. Independent practice\n\n## Practice Items\n{practice}\n\n## Suggested Certification Standard\nFor a **{complexity}** process, the trainee should complete the process correctly at least **{count}** before being considered fully trained.\n"


def generate_quality_control(process: dict) -> str:
    review_frequency = {
        "High": "Manager review should happen every time until the process is consistently performed correctly.",
        "Medium": "Manager review should happen weekly or during routine spot checks.",
        "Low": "Manager review can happen periodically or when issues are identified.",
    }.get(process["risk"], "Manager review can happen periodically.")
    return f"# {process['process_name']} Quality Control Guide\n\n## Review Frequency\n{review_frequency}\n\n## Quality Review Questions\n- Was the process completed from start to finish?\n- Were all required details captured?\n- Was the correct tool/system updated?\n- Was communication clear and professional?\n- Were issues escalated properly?\n- Did the final outcome meet the expected standard?\n\n## Common Failure Points\n- Missing notes or incomplete documentation\n- Skipped steps\n- Unclear ownership\n- Late follow-up\n- Poor handoff communication\n- Failure to escalate issues\n"


def generate_implementation_plan(process: dict, complexity: str, recommendations: list[str]) -> str:
    timeline = {
        "High Complexity": "Roll out over 2-3 weeks with training, testing, feedback, and manager review.",
        "Medium Complexity": "Roll out over 1-2 weeks with training and spot checks.",
        "Low Complexity": "Roll out immediately after manager review.",
    }.get(complexity, "Roll out after manager review.")
    rec_lines = "\n".join(f"- {r}" for r in recommendations)
    return f"# {process['process_name']} Implementation Plan\n\n## Rollout Timeline\n{timeline}\n\n## Rollout Steps\n1. Review the SOP with the process owner.\n2. Confirm the steps match the real workflow.\n3. Train responsible team members.\n4. Test the process using a sample scenario.\n5. Adjust unclear steps.\n6. Begin using the SOP in live operations.\n7. Review and improve after rollout.\n\n## Improvement Recommendations\n{rec_lines}\n"


def generate_manager_summary(process: dict, complexity: str, risk_label: str, readiness: str, score: int) -> str:
    return f"""{process['process_name']} is owned by {process['owner_role']} in the {process['department']} department.

Documentation Readiness Score: {score}%
Documentation Status: {readiness_score_status(score)}
Complexity: {complexity}
Risk Diagnosis: {risk_label}
Rollout Readiness: {readiness}
Frequency: {process['frequency']}
Team Size: {process['team_size']}

Manager Focus:
Review whether the steps match the real workflow, confirm the escalation path, train the team, and revisit the SOP after the first week of use.
"""


def generate_full_package(process: dict, workflow: dict, documents: dict) -> str:
    missing_lines = "\n".join(f"- {item}" for item in workflow["missing_items"])
    rec_lines = "\n".join(f"- {r}" for r in workflow["recommendations"])
    return f"""# SOPPilot AI Process Documentation Package

## Process Summary
Process Name: {process['process_name']}
Department: {process['department']}
Owner Role: {process['owner_role']}
Documentation Readiness Score: {workflow['score']}%
Documentation Status: {readiness_score_status(workflow['score'])}
Complexity: {workflow['complexity']}
Complexity Score: {workflow['complexity_score']}
Risk Diagnosis: {workflow['risk_label']}
Rollout Readiness: {workflow['readiness']}

{version_control_block(process, workflow['score'])}
## Manager Summary
{documents['manager_summary']}

## Missing Information Check
{missing_lines}

## Improvement Recommendations
{rec_lines}

---

{documents['sop']}

---

{documents['checklist']}

---

{documents['training']}

---

{documents['quality']}

---

{documents['implementation']}

---

Generated by SOPPilot AI.
"""


def build_documents(process: dict, workflow: dict) -> dict:
    sop = generate_sop(process, workflow["role_standards"], workflow["score"])
    checklist = generate_checklist(process, workflow["role_standards"])
    training = generate_training_plan(process, workflow["complexity"])
    quality = generate_quality_control(process)
    implementation = generate_implementation_plan(process, workflow["complexity"], workflow["recommendations"])
    manager_summary = generate_manager_summary(process, workflow["complexity"], workflow["risk_label"], workflow["readiness"], workflow["score"])
    documents = {
        "sop": sop,
        "checklist": checklist,
        "training": training,
        "quality": quality,
        "implementation": implementation,
        "manager_summary": manager_summary,
    }
    documents["full_package"] = generate_full_package(process, workflow, documents)
    return documents
