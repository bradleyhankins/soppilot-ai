import streamlit as st

st.set_page_config(page_title="SOPPilot AI", page_icon="📋", layout="wide")

def determine_complexity(frequency, risk, team_size):
    score = {"Daily": 3, "Weekly": 2, "Monthly": 1, "Rarely / As Needed": 1}.get(frequency, 1)
    score += {"High": 3, "Medium": 2, "Low": 1}.get(risk, 1)
    score += {"1-3 people": 1, "4-10 people": 2, "11+ people": 3}.get(team_size, 1)

    if score >= 8:
        return "High Complexity", "Use a detailed SOP, training checklist, quality checks, manager review, and clear escalation path.", score
    if score >= 5:
        return "Medium Complexity", "Use a clear SOP, checklist, basic quality standards, and routine spot checks.", score
    return "Low Complexity", "A simple SOP and checklist should be enough for this process.", score

def role_guidance(owner_role):
    guidance = {
        "Sales Representative": "Keep the process customer-facing and focused on communication, follow-up, and documentation.",
        "Sales Manager": "Include accountability checkpoints, coaching expectations, and measurable review standards.",
        "Operations Manager": "Include handoffs, documentation standards, quality checks, and escalation paths.",
        "Project Manager": "Focus on readiness, communication, documentation, and completion standards.",
        "Customer Service Representative": "Emphasize response time, notes, issue resolution, and customer experience.",
        "Recruiter / Hiring Manager": "Include screening steps, documentation, interview consistency, and next-step ownership.",
        "General Team Member": "Use simple step-by-step instructions that are easy to follow and repeat."
    }
    return guidance.get(owner_role, guidance["General Team Member"])

def clean_steps(steps):
    cleaned = [s.strip() for s in steps.splitlines() if s.strip()]
    return cleaned or [
        "Confirm the process trigger and required information",
        "Gather the necessary tools, documents, or context",
        "Complete the process according to company standards",
        "Document the completed work in the appropriate system",
        "Review for accuracy and escalate any issues if needed"
    ]

def missing_info_check(process_name, trigger, goal, inputs, tools, steps, quality, escalation):
    missing = []
    if not process_name:
        missing.append("Process name is missing.")
    if not trigger:
        missing.append("Process trigger is missing.")
    if not goal:
        missing.append("Process goal is missing.")
    if not inputs:
        missing.append("Required inputs/information are missing.")
    if not tools:
        missing.append("Tools or systems are missing.")
    if not steps:
        missing.append("Rough process steps are missing.")
    if not quality:
        missing.append("Quality standard is missing.")
    if not escalation:
        missing.append("Escalation path is missing.")

    if not missing:
        return ["No major missing information found."]

    return missing

def process_risk_diagnosis(frequency, risk, team_size, missing_items):
    real_missing_count = len([item for item in missing_items if item != "No major missing information found."])

    if risk == "High" and real_missing_count >= 3:
        return "High Documentation Risk", "This process has high business risk and several missing details. It should be reviewed by a manager before rollout."
    if risk == "High":
        return "High Operational Risk", "This process has high risk if completed incorrectly. Add strong quality control, manager review, and escalation steps."
    if real_missing_count >= 4:
        return "Incomplete Process Definition", "Several important details are missing. The SOP should be reviewed and completed before team rollout."
    if frequency == "Daily" and team_size in ["4-10 people", "11+ people"]:
        return "Consistency Risk", "This process happens often and is used by multiple people. Clear documentation is important to prevent drift."
    return "Standard Process Risk", "The process appears suitable for a standard SOP, checklist, and basic manager review."

def role_quality_standards(owner_role):
    standards = {
        "Sales Representative": [
            "Customer contact attempts are documented",
            "Next step is clear",
            "Follow-up task is created when needed",
            "Communication is professional and timely"
        ],
        "Sales Manager": [
            "Rep activity is reviewed",
            "Coaching notes are documented",
            "Accountability expectations are clear",
            "Performance issue has a next action"
        ],
        "Operations Manager": [
            "Handoff is complete",
            "Owner is clear",
            "System notes are accurate",
            "Escalations are documented"
        ],
        "Project Manager": [
            "Job status is accurate",
            "Customer/internal updates are documented",
            "Issues are escalated quickly",
            "Completion standard is verified"
        ],
        "Customer Service Representative": [
            "Customer concern is documented",
            "Response is timely",
            "Resolution or next step is clear",
            "Escalation happens when needed"
        ],
        "Recruiter / Hiring Manager": [
            "Candidate status is updated",
            "Interview notes are complete",
            "Next step is documented",
            "Decision criteria are consistent"
        ],
        "General Team Member": [
            "Steps are completed in order",
            "Documentation is clear",
            "Issues are escalated",
            "Final outcome is reviewed"
        ]
    }
    return standards.get(owner_role, standards["General Team Member"])

def improvement_recommendations(complexity, risk_level, missing_items):
    recommendations = []
    real_missing = [item for item in missing_items if item != "No major missing information found."]

    if real_missing:
        recommendations.append("Complete missing process details before publishing the SOP.")
    if complexity == "High Complexity":
        recommendations.append("Add manager review checkpoints and require sign-off during initial rollout.")
        recommendations.append("Use the training plan before allowing independent execution.")
    if risk_level == "High":
        recommendations.append("Add a clear escalation path and define what should stop the process.")
    recommendations.append("Review the SOP after the first week of use and update unclear steps.")
    recommendations.append("Assign one process owner responsible for keeping the SOP current.")

    return recommendations

def generate_sop(process_name, department, owner_role, trigger, goal, inputs, steps, tools, quality, escalation, role_standards):
    step_list = clean_steps(steps)
    step_lines = "\n".join([f"{i}. {step}" for i, step in enumerate(step_list, 1)])
    standards = "\n".join([f"- {standard}" for standard in role_standards])

    return f"""# {process_name} SOP

## Department
{department}

## Process Owner
{owner_role}

## Purpose
Create a consistent, repeatable process for **{process_name}**.

## Process Goal
{goal or "Ensure the process is completed accurately, consistently, and with clear documentation."}

## When This Process Starts
{trigger or "This process begins when the assigned team member identifies that the task needs to be completed."}

## Inputs / Information Needed
{inputs or "Required customer, project, task, or internal information should be gathered before starting."}

## Tools / Systems Used
{tools or "Relevant CRM, spreadsheet, communication platform, document system, or internal tool."}

## Role-Specific Guidance
{role_guidance(owner_role)}

## Standard Procedure
{step_lines}

## Role-Specific Quality Standards
{standards}

## Quality Standard
{quality or "The process should be completed accurately, documented clearly, and reviewed for completeness before being considered finished."}

## Escalation Path
{escalation or "If the team member cannot complete the process or identifies an issue, they should escalate to the appropriate manager or process owner."}

## Completion Definition
This process is complete when:
- Required steps have been completed
- Required notes or documentation have been entered
- Any customer/internal communication has been completed
- Issues have been escalated if needed
- The process owner can verify completion
"""

def generate_checklist(process_name, steps, quality, role_standards):
    items = clean_steps(steps)
    checklist = f"# {process_name} Checklist\n\n"
    checklist += "\n".join([f"- [ ] {item}" for item in items])
    checklist += "\n\n## Role-Specific Quality Checks\n"
    checklist += "\n".join([f"- [ ] {standard}" for standard in role_standards])
    checklist += f"""

## Final Quality Check
- [ ] Information is complete
- [ ] Notes are clear
- [ ] Required communication is complete
- [ ] Process outcome matches expected standard
- [ ] Issues were escalated if needed

Quality Standard:
{quality or "Complete, accurate, documented, and ready for review."}
"""
    return checklist

def generate_training_plan(process_name, owner_role, complexity, steps):
    items = clean_steps(steps)[:5]
    practice = "\n".join([f"- {item}" for item in items])
    certification_count = "3 times" if complexity == "High Complexity" else "2 times"

    return f"""# {process_name} Training Plan

## Target Role
{owner_role}

## Training Goal
Train the team member to complete **{process_name}** consistently, accurately, and with proper documentation.

## Recommended Training Structure

### 1. Explain the Why
Review why the process matters, what problems it prevents, and how it supports the business.

### 2. Walk Through the SOP
Have the trainer walk through the full SOP step-by-step.

### 3. Demonstrate the Process
The trainer completes the process once while the trainee observes.

### 4. Guided Practice
The trainee completes the process with coaching and feedback.

### 5. Independent Practice
The trainee completes the process without help while the trainer reviews the result.

## Practice Items
{practice}

## Manager Review
The manager should confirm:
- The trainee understands the process trigger
- The trainee can complete each step
- The trainee documents the process correctly
- The trainee knows when to escalate
- The trainee meets the quality standard

## Suggested Certification Standard
For a **{complexity}** process, the trainee should complete the process correctly at least **{certification_count}** before being considered fully trained.
"""

def generate_quality_control(process_name, risk, quality):
    frequency = {
        "High": "Manager review should happen every time until the process is consistently performed correctly.",
        "Medium": "Manager review should happen weekly or during routine spot checks.",
        "Low": "Manager review can happen periodically or when issues are identified."
    }.get(risk, "Manager review can happen periodically.")

    return f"""# {process_name} Quality Control Guide

## Review Frequency
{frequency}

## Quality Review Questions
- Was the process completed from start to finish?
- Were all required details captured?
- Was the correct tool/system updated?
- Was communication clear and professional?
- Were issues escalated properly?
- Did the final outcome meet the expected standard?

## Quality Standard
{quality or "The process should be complete, accurate, documented, and easy for another team member or manager to review."}

## Common Failure Points
- Missing notes or incomplete documentation
- Skipped steps
- Unclear ownership
- Late follow-up
- Poor handoff communication
- Failure to escalate issues

## Manager Coaching Prompt
If this process breaks down, ask:
"What step was missed, what caused the miss, and what should we change so it is easier to do correctly next time?"
"""

def generate_implementation_plan(process_name, complexity, recommendations):
    timeline = {
        "High Complexity": "Roll out over 2-3 weeks with training, testing, feedback, and manager review.",
        "Medium Complexity": "Roll out over 1-2 weeks with training and spot checks.",
        "Low Complexity": "Roll out immediately after manager review."
    }.get(complexity, "Roll out after manager review.")

    rec_lines = "\n".join([f"- {rec}" for rec in recommendations])

    return f"""# {process_name} Implementation Plan

## Rollout Timeline
{timeline}

## Rollout Steps
1. Review the SOP with the process owner.
2. Confirm the steps match the real workflow.
3. Train the team members responsible for the process.
4. Test the process using a sample scenario.
5. Adjust unclear steps based on team feedback.
6. Begin using the SOP in live operations.
7. Review results and improve the SOP as needed.

## Improvement Recommendations
{rec_lines}

## Success Metrics
- Team members understand the process
- Process is completed more consistently
- Fewer missed steps
- Better documentation
- Faster manager review
- Clearer escalation when issues occur
"""

st.title("📋 SOPPilot AI")
st.subheader("AI-assisted SOP, checklist, and training document generator for small-business teams")

st.markdown("""
SOPPilot AI helps managers turn messy process notes into structured SOPs, checklists,
training plans, quality control guides, implementation plans, and rollout recommendations.
""")

st.sidebar.title("SOPPilot AI")
st.sidebar.caption("Version 1.1 MVP")
st.sidebar.markdown("""
**Built by Bradley Hankins**

A practical AI workflow automation tool for process documentation, training, and operational consistency.
""")
st.sidebar.divider()

with st.sidebar.expander("What this app generates"):
    st.markdown("""
    - Standard Operating Procedure
    - Process checklist
    - Missing-info check
    - Process risk diagnosis
    - Training plan
    - Quality control guide
    - Implementation plan
    - Downloadable SOP package
    """)

st.header("SOP Builder")

with st.form("sop_form"):
    col1, col2 = st.columns(2)

    with col1:
        process_name = st.text_input("Process Name", placeholder="Example: New Lead Follow-Up Process")
        department = st.selectbox("Department", ["Sales", "Operations", "Customer Service", "Production / Project Management", "Recruiting / HR", "Administration", "Other"])
        owner_role = st.selectbox("Process Owner Role", ["Sales Representative", "Sales Manager", "Operations Manager", "Project Manager", "Customer Service Representative", "Recruiter / Hiring Manager", "General Team Member"])
        process_frequency = st.selectbox("How Often Does This Process Happen?", ["Daily", "Weekly", "Monthly", "Rarely / As Needed"])
        risk_level = st.selectbox("Risk Level if Done Incorrectly", ["Low", "Medium", "High"])

    with col2:
        team_size = st.selectbox("How Many People Use This Process?", ["1-3 people", "4-10 people", "11+ people"])
        trigger_event = st.text_area("What Triggers This Process?", placeholder="Example: A new lead is assigned to a sales rep.")
        goal = st.text_area("What Is the Goal of This Process?", placeholder="Example: Contact the lead quickly, document the outcome, and schedule the next step.")
        inputs_needed = st.text_area("Inputs / Information Needed", placeholder="Example: Customer name, phone number, project type, lead source, appointment availability.")
        tools_used = st.text_area("Tools / Systems Used", placeholder="Example: CRM, phone, email, calendar, shared spreadsheet.")

    steps = st.text_area("Rough Process Steps", height=220, placeholder="""Example:
Review the new lead information
Call the customer within 5 minutes
Send a follow-up text if no answer
Document the contact attempt in the CRM
Schedule appointment or set follow-up task""")

    quality_standard = st.text_area("Quality Standard", placeholder="Example: Every lead should have a documented contact attempt, clear next step, and follow-up task if not reached.")
    escalation_path = st.text_area("Escalation Path", placeholder="Example: Escalate to the sales manager if the lead cannot be reached after 3 attempts.")
    submitted = st.form_submit_button("Generate SOP Package")

if submitted:
    final_process_name = process_name or "Untitled Business Process"
    complexity, complexity_note, complexity_score = determine_complexity(process_frequency, risk_level, team_size)
    missing_items = missing_info_check(process_name, trigger_event, goal, inputs_needed, tools_used, steps, quality_standard, escalation_path)
    risk_label, risk_note = process_risk_diagnosis(process_frequency, risk_level, team_size, missing_items)
    role_standards = role_quality_standards(owner_role)
    recommendations = improvement_recommendations(complexity, risk_level, missing_items)

    sop = generate_sop(final_process_name, department, owner_role, trigger_event, goal, inputs_needed, steps, tools_used, quality_standard, escalation_path, role_standards)
    checklist = generate_checklist(final_process_name, steps, quality_standard, role_standards)
    training = generate_training_plan(final_process_name, owner_role, complexity, steps)
    quality = generate_quality_control(final_process_name, risk_level, quality_standard)
    implementation = generate_implementation_plan(final_process_name, complexity, recommendations)

    st.divider()
    st.header("Generated SOP Package")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Process Complexity", complexity)
    col2.metric("Complexity Score", complexity_score)
    col3.metric("Risk Diagnosis", risk_label)
    col4.metric("Owner Role", owner_role)

    st.info(complexity_note)
    st.warning(risk_note)

    st.subheader("Missing Information Check")
    for item in missing_items:
        if item == "No major missing information found.":
            st.success(item)
        else:
            st.warning(item)

    st.subheader("Improvement Recommendations")
    for rec in recommendations:
        st.markdown(f"- {rec}")

    st.subheader("Standard Operating Procedure")
    st.text_area("Generated SOP", sop, height=420)

    st.subheader("Process Checklist")
    st.text_area("Generated Checklist", checklist, height=300)

    st.subheader("Training Plan")
    st.text_area("Generated Training Plan", training, height=360)

    st.subheader("Quality Control Guide")
    st.text_area("Generated Quality Control Guide", quality, height=340)

    st.subheader("Implementation Plan")
    st.text_area("Generated Implementation Plan", implementation, height=340)

    full_package = f"""# SOPPilot AI Process Documentation Package

## Process Summary
Process Name: {final_process_name}
Department: {department}
Owner Role: {owner_role}
Complexity: {complexity}
Complexity Score: {complexity_score}
Risk Diagnosis: {risk_label}

## Missing Information Check
""" + "\n".join([f"- {item}" for item in missing_items]) + """

## Improvement Recommendations
""" + "\n".join([f"- {rec}" for rec in recommendations]) + f"""

---

{sop}

---

{checklist}

---

{training}

---

{quality}

---

{implementation}

---

Generated by SOPPilot AI.
"""

    st.download_button("Download SOP Package", data=full_package, file_name="soppilot-sop-package.md", mime="text/markdown")
else:
    st.info("Complete the form and click Generate SOP Package to create an SOP, checklist, training plan, quality guide, and implementation plan.")

st.divider()

st.header("Built for Practical AI Process Documentation")
st.markdown("""
SOPPilot AI is a portfolio project demonstrating how AI-assisted workflows can help small businesses
turn informal process knowledge into usable documentation, training materials, quality standards, and rollout plans.

This MVP uses rules-based generation to keep the app free, simple, and easy to deploy. Future versions can include
OpenAI API integration, PDF exports, saved templates, team libraries, and role-based SOP packages.
""")
st.info("Privacy note: Information entered into this app is processed during the active session and is not saved by this app.")
