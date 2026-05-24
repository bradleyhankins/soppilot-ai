import streamlit as st

# -----------------------------------------------------------------------------
# Page configuration
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="SOPPilot AI",
    page_icon="📋",
    layout="wide",
)

# -----------------------------------------------------------------------------
# App configuration
# -----------------------------------------------------------------------------

DEPARTMENTS = [
    "Sales",
    "Operations",
    "Customer Service",
    "Production / Project Management",
    "Recruiting / HR",
    "Administration",
    "Other",
]

OWNER_ROLES = [
    "Sales Representative",
    "Sales Manager",
    "Operations Manager",
    "Project Manager",
    "Customer Service Representative",
    "Recruiter / Hiring Manager",
    "General Team Member",
]

FREQUENCIES = ["Daily", "Weekly", "Monthly", "Rarely / As Needed"]
RISK_LEVELS = ["Low", "Medium", "High"]
TEAM_SIZES = ["1-3 people", "4-10 people", "11+ people"]

SAMPLE_PROCESSES = {
    "Blank / Custom": {},
    "New Lead Follow-Up": {
        "process_name": "New Lead Follow-Up Process",
        "department": "Sales",
        "owner_role": "Sales Representative",
        "frequency": "Daily",
        "risk": "High",
        "team_size": "4-10 people",
        "trigger": "A new lead is assigned to a sales representative.",
        "goal": "Contact the lead quickly, document the outcome, and schedule the next step.",
        "inputs": "Customer name, phone number, project type, lead source, appointment availability, and notes from intake.",
        "tools": "CRM, phone, text messaging, email, calendar, and manager dashboard.",
        "steps": "Review the new lead information\nCall the customer within 5 minutes\nSend a follow-up text if there is no answer\nDocument the contact attempt in the CRM\nSchedule an appointment or set a follow-up task\nNotify the manager if the lead cannot be reached after required attempts",
        "quality": "Every lead should have a documented contact attempt, clear next step, and follow-up task if not reached.",
        "escalation": "Escalate to the sales manager if the lead cannot be reached after 3 attempts or if the customer has an urgent issue.",
    },
    "Job Handoff": {
        "process_name": "Sold Job Handoff Process",
        "department": "Production / Project Management",
        "owner_role": "Project Manager",
        "frequency": "Weekly",
        "risk": "High",
        "team_size": "4-10 people",
        "trigger": "A project is sold and needs to move from sales to production.",
        "goal": "Make sure production has complete project details, customer expectations, and required documents before scheduling work.",
        "inputs": "Signed agreement, scope of work, photos, measurements, product selections, payment details, customer notes, and scheduling constraints.",
        "tools": "CRM, project management board, shared files, calendar, email, and customer communication tools.",
        "steps": "Review signed agreement and scope\nConfirm measurements and product selections\nUpload photos and supporting documents\nDocument customer expectations and special notes\nAssign project manager ownership\nSchedule production review\nConfirm handoff completion in CRM",
        "quality": "Production should receive a complete and accurate handoff before any work is scheduled.",
        "escalation": "Escalate to the sales manager or operations manager if scope, pricing, photos, or customer expectations are unclear.",
    },
    "Candidate Follow-Up": {
        "process_name": "Candidate Follow-Up Process",
        "department": "Recruiting / HR",
        "owner_role": "Recruiter / Hiring Manager",
        "frequency": "Weekly",
        "risk": "Medium",
        "team_size": "1-3 people",
        "trigger": "A candidate completes an application, phone screen, or interview.",
        "goal": "Keep candidates informed, document next steps, and avoid losing qualified applicants due to slow communication.",
        "inputs": "Candidate name, role, application source, interview notes, availability, next step, and hiring manager feedback.",
        "tools": "Applicant tracker, email, phone, calendar, and interview notes document.",
        "steps": "Review candidate status\nConfirm next step with hiring manager\nSend candidate follow-up message\nUpdate applicant tracking notes\nSchedule next interview or document pause reason\nSet reminder for next action",
        "quality": "Every candidate should have a clear status, documented next step, and timely communication.",
        "escalation": "Escalate to the hiring manager if feedback is missing or if the candidate is waiting more than 48 hours for next steps.",
    },
}

# -----------------------------------------------------------------------------
# Styling
# -----------------------------------------------------------------------------

CUSTOM_CSS = """
<style>
.block-container {
    max-width: 1180px;
    padding-top: 1.35rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #111827;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] ul,
[data-testid="stSidebar"] ol {
    color: #f9fafb !important;
}

[data-testid="stSidebar"] li::marker {
    color: #93c5fd !important;
}

.hero {
    padding: 1.9rem 2rem;
    border-radius: 20px;
    background: linear-gradient(135deg, #111827 0%, #1f2937 52%, #334155 100%);
    color: #ffffff;
    box-shadow: 0 18px 36px rgba(17, 24, 39, .18);
    margin-bottom: 1rem;
}

.eyebrow {
    text-transform: uppercase;
    letter-spacing: .13em;
    font-size: .75rem;
    font-weight: 800;
    color: #93c5fd;
    margin-bottom: .65rem;
}

.hero-title {
    font-size: 2.25rem;
    line-height: 1.08;
    font-weight: 850;
    margin-bottom: .65rem;
}

.hero-subtitle {
    font-size: 1.02rem;
    line-height: 1.62;
    color: #e5e7eb;
    max-width: 900px;
}

.hero-pills span {
    display: inline-block;
    padding: .35rem .65rem;
    margin: .75rem .28rem 0 0;
    border-radius: 999px;
    background: rgba(255, 255, 255, .10);
    border: 1px solid rgba(255, 255, 255, .16);
    font-weight: 700;
    font-size: .78rem;
    color: #f8fafc;
}

.section-title {
    margin-top: 1.25rem;
    margin-bottom: .55rem;
    font-size: 1.4rem;
    font-weight: 850;
    color: #111827;
}

.section-lede {
    color: #4b5563;
    line-height: 1.6;
    margin-bottom: 1rem;
    max-width: 950px;
}

.form-group-title {
    font-size: .9rem;
    font-weight: 850;
    text-transform: uppercase;
    letter-spacing: .06em;
    color: #64748b;
    margin: .35rem 0 .15rem 0;
}

.metric-card,
.output-card,
.success-card,
.warning-card,
.workflow-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    box-shadow: 0 8px 20px rgba(15, 23, 42, .055);
}

.metric-card {
    height: 138px;
    padding: 1rem;
    margin-bottom: .75rem;
}

.metric-label {
    color: #6b7280;
    font-size: .78rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .05em;
    margin-bottom: .5rem;
}

.metric-value {
    color: #111827;
    font-size: 1.35rem;
    line-height: 1.18;
    font-weight: 900;
    overflow-wrap: break-word;
}

.metric-note {
    color: #64748b;
    font-size: .85rem;
    margin-top: .55rem;
}

.output-card,
.success-card,
.warning-card,
.workflow-card {
    padding: 1.15rem;
    margin-bottom: .8rem;
}

.output-card { border-left: 5px solid #111827; }
.success-card { border-left: 5px solid #059669; }
.warning-card { border-left: 5px solid #f59e0b; }
.workflow-card { border-left: 5px solid #1d4ed8; }

.output-card h3,
.success-card h3,
.warning-card h3,
.workflow-card h3 {
    font-size: 1.05rem;
    font-weight: 850;
    color: #111827;
    margin-bottom: .4rem;
}

.output-card p,
.success-card p,
.warning-card p,
.workflow-card p,
.output-card li,
.success-card li,
.warning-card li,
.workflow-card li {
    color: #4b5563;
    line-height: 1.52;
    font-size: .93rem;
}

.note-box {
    padding: .9rem 1rem;
    border-radius: 14px;
    background: #f8fafc;
    color: #334155;
    border: 1px solid #e2e8f0;
    font-weight: 650;
    margin: .9rem 0;
    font-size: .92rem;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# UI helpers
# -----------------------------------------------------------------------------


def section_title(title: str, lede: str | None = None) -> None:
    """Render a consistent section title."""
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if lede:
        st.markdown(f'<div class="section-lede">{lede}</div>', unsafe_allow_html=True)


def form_group(title: str) -> None:
    """Render a form section label."""
    st.markdown(f'<div class="form-group-title">{title}</div>', unsafe_allow_html=True)


def metric_card(label: str, value: str, note: str | None = None) -> None:
    """Render a metric card."""
    note_html = f'<div class="metric-note">{note}</div>' if note else ""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {note_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def html_card(title: str, body: str, css_class: str = "output-card") -> None:
    """Render a reusable content card."""
    st.markdown(
        f"""
        <div class="{css_class}">
            <h3>{title}</h3>
            {body}
        </div>
        """,
        unsafe_allow_html=True,
    )


def html_list(items: list[str], empty_message: str) -> str:
    """Render a list with a fallback item."""
    visible_items = items or [empty_message]
    return "<ul>" + "".join(f"<li>{item}</li>" for item in visible_items) + "</ul>"

# -----------------------------------------------------------------------------
# SOP logic
# -----------------------------------------------------------------------------


def clean_steps(steps: str) -> list[str]:
    """Split rough process notes into clean step lines."""
    cleaned = [step.strip(" -•\t") for step in steps.splitlines() if step.strip()]
    return cleaned or [
        "Confirm the process trigger and required information",
        "Gather the necessary tools, documents, or context",
        "Complete the process according to company standards",
        "Document the completed work in the appropriate system",
        "Review for accuracy and escalate any issues if needed",
    ]


def determine_complexity(frequency: str, risk: str, team_size: str) -> tuple[str, str, int]:
    """Determine process complexity from usage, risk, and team size."""
    score = {"Daily": 3, "Weekly": 2, "Monthly": 1, "Rarely / As Needed": 1}.get(frequency, 1)
    score += {"High": 3, "Medium": 2, "Low": 1}.get(risk, 1)
    score += {"1-3 people": 1, "4-10 people": 2, "11+ people": 3}.get(team_size, 1)

    if score >= 8:
        return "High Complexity", "Use a detailed SOP, training checklist, quality checks, manager review, and clear escalation path.", score
    if score >= 5:
        return "Medium Complexity", "Use a clear SOP, checklist, basic quality standards, and routine spot checks.", score
    return "Low Complexity", "A simple SOP and checklist should be enough for this process.", score


def role_guidance(owner_role: str) -> str:
    """Return role-specific process guidance."""
    guidance = {
        "Sales Representative": "Keep the process customer-facing and focused on communication, follow-up, and documentation.",
        "Sales Manager": "Include accountability checkpoints, coaching expectations, and measurable review standards.",
        "Operations Manager": "Include handoffs, documentation standards, quality checks, and escalation paths.",
        "Project Manager": "Focus on readiness, communication, documentation, and completion standards.",
        "Customer Service Representative": "Emphasize response time, notes, issue resolution, and customer experience.",
        "Recruiter / Hiring Manager": "Include review steps, documentation, interview consistency, and next-step ownership.",
        "General Team Member": "Use simple step-by-step instructions that are easy to follow and repeat.",
    }
    return guidance.get(owner_role, guidance["General Team Member"])


def role_quality_standards(owner_role: str) -> list[str]:
    """Return role-specific quality standards."""
    standards = {
        "Sales Representative": [
            "Customer contact attempts are documented",
            "Next step is clear",
            "Follow-up task is created when needed",
            "Communication is professional and timely",
        ],
        "Sales Manager": [
            "Rep activity is reviewed",
            "Coaching notes are documented",
            "Accountability expectations are clear",
            "Performance issue has a next action",
        ],
        "Operations Manager": [
            "Handoff is complete",
            "Owner is clear",
            "System notes are accurate",
            "Escalations are documented",
        ],
        "Project Manager": [
            "Job status is accurate",
            "Customer/internal updates are documented",
            "Issues are escalated quickly",
            "Completion standard is verified",
        ],
        "Customer Service Representative": [
            "Customer concern is documented",
            "Response is timely",
            "Resolution or next step is clear",
            "Escalation happens when needed",
        ],
        "Recruiter / Hiring Manager": [
            "Status is updated",
            "Notes are complete",
            "Next step is documented",
            "Review criteria are consistent",
        ],
        "General Team Member": [
            "Steps are completed in order",
            "Documentation is clear",
            "Issues are escalated",
            "Final outcome is reviewed",
        ],
    }
    return standards.get(owner_role, standards["General Team Member"])


def missing_info_check(process: dict) -> list[str]:
    """Identify missing process details."""
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
    """Diagnose process documentation risk."""
    real_missing_count = len([item for item in missing_items if item != "No major missing information found."])

    if process["risk"] == "High" and real_missing_count >= 3:
        return "High Documentation Risk", "This process has high business risk and several missing details. Review with a manager before rollout."
    if process["risk"] == "High":
        return "High Operational Risk", "This process has high risk if completed incorrectly. Add quality control, manager review, and escalation steps."
    if real_missing_count >= 4:
        return "Incomplete Process Definition", "Several important details are missing. Complete the SOP before team rollout."
    if process["frequency"] == "Daily" and process["team_size"] in ["4-10 people", "11+ people"]:
        return "Consistency Risk", "This process happens often and is used by multiple people. Clear documentation is important to prevent process drift."
    return "Standard Process Risk", "The process appears suitable for a standard SOP, checklist, and basic manager review."


def readiness_status(complexity: str, missing_items: list[str], risk_label: str) -> tuple[str, str]:
    """Determine rollout readiness."""
    real_missing = [item for item in missing_items if item != "No major missing information found."]
    if real_missing:
        return "Needs Completion", "Complete missing details before publishing this SOP."
    if risk_label in ["High Documentation Risk", "High Operational Risk"] or complexity == "High Complexity":
        return "Manager Review Recommended", "The SOP is usable, but should be reviewed by a manager before rollout."
    return "Ready for Team Review", "The SOP is ready to review with the team and test in live workflow."


def improvement_recommendations(complexity: str, risk_level: str, missing_items: list[str]) -> list[str]:
    """Generate improvement recommendations."""
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

# -----------------------------------------------------------------------------
# Document generation
# -----------------------------------------------------------------------------


def generate_sop(process: dict, role_standards: list[str]) -> str:
    """Generate the SOP document."""
    step_lines = "\n".join(
        f"{index}. {step}"
        for index, step in enumerate(clean_steps(process["steps"]), start=1)
    )
    standard_lines = "\n".join(f"- {standard}" for standard in role_standards)

    return f"""# {process['process_name']} SOP

## Department
{process['department']}

## Process Owner
{process['owner_role']}

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
{standard_lines}

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
    """Generate the checklist document."""
    step_items = "\n".join(f"- [ ] {item}" for item in clean_steps(process["steps"]))
    standards = "\n".join(f"- [ ] {standard}" for standard in role_standards)

    return f"""# {process['process_name']} Checklist

## Process Steps
{step_items}

## Role-Specific Quality Checks
{standards}

## Final Quality Check
- [ ] Information is complete
- [ ] Notes are clear
- [ ] Required communication is complete
- [ ] Process outcome matches expected standard
- [ ] Issues were escalated if needed

Quality Standard:
{process['quality'] or 'Complete, accurate, documented, and ready for review.'}
"""


def generate_training_plan(process: dict, complexity: str) -> str:
    """Generate the training plan."""
    practice_items = "\n".join(f"- {item}" for item in clean_steps(process["steps"])[:5])
    certification_count = "3 times" if complexity == "High Complexity" else "2 times"

    return f"""# {process['process_name']} Training Plan

## Target Role
{process['owner_role']}

## Training Goal
Train the team member to complete **{process['process_name']}** consistently, accurately, and with proper documentation.

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
{practice_items}

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


def generate_quality_control(process: dict) -> str:
    """Generate the quality control guide."""
    review_frequency = {
        "High": "Manager review should happen every time until the process is consistently performed correctly.",
        "Medium": "Manager review should happen weekly or during routine spot checks.",
        "Low": "Manager review can happen periodically or when issues are identified.",
    }.get(process["risk"], "Manager review can happen periodically.")

    return f"""# {process['process_name']} Quality Control Guide

## Review Frequency
{review_frequency}

## Quality Review Questions
- Was the process completed from start to finish?
- Were all required details captured?
- Was the correct tool/system updated?
- Was communication clear and professional?
- Were issues escalated properly?
- Did the final outcome meet the expected standard?

## Quality Standard
{process['quality'] or 'The process should be complete, accurate, documented, and easy for another team member or manager to review.'}

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


def generate_implementation_plan(process: dict, complexity: str, recommendations: list[str]) -> str:
    """Generate the implementation plan."""
    timeline = {
        "High Complexity": "Roll out over 2-3 weeks with training, testing, feedback, and manager review.",
        "Medium Complexity": "Roll out over 1-2 weeks with training and spot checks.",
        "Low Complexity": "Roll out immediately after manager review.",
    }.get(complexity, "Roll out after manager review.")
    recommendation_lines = "\n".join(f"- {recommendation}" for recommendation in recommendations)

    return f"""# {process['process_name']} Implementation Plan

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
{recommendation_lines}

## Success Metrics
- Team members understand the process
- Process is completed more consistently
- Fewer missed steps
- Better documentation
- Faster manager review
- Clearer escalation when issues occur
"""


def generate_manager_summary(process: dict, complexity: str, risk_label: str, readiness: str) -> str:
    """Generate a manager-ready process summary."""
    return f"""{process['process_name']} is owned by {process['owner_role']} in the {process['department']} department.

Complexity: {complexity}
Risk Diagnosis: {risk_label}
Rollout Readiness: {readiness}
Frequency: {process['frequency']}
Team Size: {process['team_size']}

Manager Focus:
Review whether the steps match the real workflow, confirm the escalation path, train the team, and revisit the SOP after the first week of use.
"""


def generate_full_package(
    process: dict,
    complexity: str,
    complexity_score: int,
    risk_label: str,
    readiness: str,
    missing_items: list[str],
    recommendations: list[str],
    manager_summary_text: str,
    sop: str,
    checklist: str,
    training: str,
    quality: str,
    implementation: str,
) -> str:
    """Generate the downloadable Markdown SOP package."""
    missing_lines = "\n".join(f"- {item}" for item in missing_items)
    recommendation_lines = "\n".join(f"- {recommendation}" for recommendation in recommendations)

    return f"""# SOPPilot AI Process Documentation Package

## Process Summary
Process Name: {process['process_name']}
Department: {process['department']}
Owner Role: {process['owner_role']}
Complexity: {complexity}
Complexity Score: {complexity_score}
Risk Diagnosis: {risk_label}
Rollout Readiness: {readiness}

## Manager Summary
{manager_summary_text}

## Missing Information Check
{missing_lines}

## Improvement Recommendations
{recommendation_lines}

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

# -----------------------------------------------------------------------------
# Sidebar and hero
# -----------------------------------------------------------------------------

with st.sidebar:
    st.title("SOPPilot AI")
    st.caption("Version 2.0")
    st.markdown("Process documentation and training workflow assistant for small-business teams.")
    st.divider()
    st.markdown("### Outputs")
    st.markdown(
        """
        - Standard Operating Procedure
        - Process checklist
        - Missing-info check
        - Process risk diagnosis
        - Training plan
        - Quality control guide
        - Implementation plan
        - Downloadable SOP package
        """
    )

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Process Documentation Workflow Tool</div>
        <div class="hero-title">SOPPilot AI</div>
        <div class="hero-subtitle">
            Turn rough process notes into SOPs, process checklists, missing-information checks,
            risk diagnoses, training plans, quality control guides, implementation plans, and downloadable documentation packages.
        </div>
        <div class="hero-pills">
            <span>SOPs</span><span>Training</span><span>Quality Control</span><span>Implementation</span><span>Streamlit</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Input workflow
# -----------------------------------------------------------------------------

section_title(
    "SOP builder",
    "Load a fictional sample process or enter your own rough process notes. SOPPilot will organize the process into a complete documentation package.",
)

scenario_name = st.selectbox("Load Sample Process", list(SAMPLE_PROCESSES.keys()))
scenario = SAMPLE_PROCESSES.get(scenario_name, {})

with st.form("sop_form"):
    form_group("Process ownership")
    owner_col1, owner_col2, owner_col3 = st.columns(3)
    with owner_col1:
        process_name = st.text_input(
            "Process Name",
            value=scenario.get("process_name", ""),
            placeholder="Example: New Lead Follow-Up Process",
        )
    with owner_col2:
        department = st.selectbox(
            "Department",
            DEPARTMENTS,
            index=DEPARTMENTS.index(scenario.get("department", "Sales")),
        )
    with owner_col3:
        owner_role = st.selectbox(
            "Process Owner Role",
            OWNER_ROLES,
            index=OWNER_ROLES.index(scenario.get("owner_role", "Sales Representative")),
        )

    form_group("Process risk and usage")
    risk_col1, risk_col2, risk_col3 = st.columns(3)
    with risk_col1:
        frequency = st.selectbox(
            "How Often Does This Process Happen?",
            FREQUENCIES,
            index=FREQUENCIES.index(scenario.get("frequency", "Daily")),
        )
    with risk_col2:
        risk = st.selectbox(
            "Risk Level if Done Incorrectly",
            RISK_LEVELS,
            index=RISK_LEVELS.index(scenario.get("risk", "Medium")),
        )
    with risk_col3:
        team_size = st.selectbox(
            "How Many People Use This Process?",
            TEAM_SIZES,
            index=TEAM_SIZES.index(scenario.get("team_size", "1-3 people")),
        )

    form_group("Process details")
    detail_col1, detail_col2 = st.columns(2)
    with detail_col1:
        trigger = st.text_area(
            "What Triggers This Process?",
            value=scenario.get("trigger", ""),
            height=110,
        )
        inputs = st.text_area(
            "Inputs / Information Needed",
            value=scenario.get("inputs", ""),
            height=110,
        )
    with detail_col2:
        goal = st.text_area(
            "What Is the Goal of This Process?",
            value=scenario.get("goal", ""),
            height=110,
        )
        tools = st.text_area(
            "Tools / Systems Used",
            value=scenario.get("tools", ""),
            height=110,
        )

    form_group("Rough workflow")
    steps = st.text_area(
        "Rough Process Steps",
        value=scenario.get("steps", ""),
        height=190,
        placeholder="Enter one step per line...",
    )

    form_group("Quality and escalation")
    quality_col1, quality_col2 = st.columns(2)
    with quality_col1:
        quality_standard = st.text_area(
            "Quality Standard",
            value=scenario.get("quality", ""),
            height=110,
        )
    with quality_col2:
        escalation_path = st.text_area(
            "Escalation Path",
            value=scenario.get("escalation", ""),
            height=110,
        )

    submitted = st.form_submit_button("Generate SOP Package", use_container_width=True)

if not submitted:
    st.markdown(
        '<div class="note-box">Complete the form or load a sample process, then click Generate SOP Package.</div>',
        unsafe_allow_html=True,
    )
    st.stop()

# -----------------------------------------------------------------------------
# Generate outputs
# -----------------------------------------------------------------------------

process = {
    "process_name": process_name or "Untitled Business Process",
    "department": department,
    "owner_role": owner_role,
    "frequency": frequency,
    "risk": risk,
    "team_size": team_size,
    "trigger": trigger,
    "goal": goal,
    "inputs": inputs,
    "tools": tools,
    "steps": steps,
    "quality": quality_standard,
    "escalation": escalation_path,
}

complexity, complexity_note, complexity_score = determine_complexity(frequency, risk, team_size)
missing_items = missing_info_check(process)
risk_label, risk_note = process_risk_diagnosis(process, missing_items)
readiness, readiness_note = readiness_status(complexity, missing_items, risk_label)
role_standards = role_quality_standards(owner_role)
recommendations = improvement_recommendations(complexity, risk, missing_items)

sop = generate_sop(process, role_standards)
checklist = generate_checklist(process, role_standards)
training = generate_training_plan(process, complexity)
quality = generate_quality_control(process)
implementation = generate_implementation_plan(process, complexity, recommendations)
manager_summary_text = generate_manager_summary(process, complexity, risk_label, readiness)
full_package = generate_full_package(
    process,
    complexity,
    complexity_score,
    risk_label,
    readiness,
    missing_items,
    recommendations,
    manager_summary_text,
    sop,
    checklist,
    training,
    quality,
    implementation,
)

# -----------------------------------------------------------------------------
# Output workflow
# -----------------------------------------------------------------------------

section_title("SOP package snapshot")
snapshot_col1, snapshot_col2, snapshot_col3, snapshot_col4 = st.columns(4)
with snapshot_col1:
    metric_card("Complexity", complexity, f"Score: {complexity_score}")
with snapshot_col2:
    metric_card("Risk Diagnosis", risk_label)
with snapshot_col3:
    metric_card("Readiness", readiness)
with snapshot_col4:
    metric_card("Owner Role", owner_role)

html_card("Complexity Guidance", f"<p>{complexity_note}</p>", "workflow-card")
html_card("Risk Guidance", f"<p>{risk_note}</p>", "warning-card")
html_card("Rollout Readiness", f"<p>{readiness_note}</p>", "success-card")

section_title("Missing information and recommendations")
missing_col, rec_col = st.columns(2)
with missing_col:
    html_card(
        "Missing Information Check",
        html_list(missing_items, "No major missing information found."),
        "warning-card" if missing_items != ["No major missing information found."] else "success-card",
    )
with rec_col:
    html_card(
        "Improvement Recommendations",
        html_list(recommendations, "No major recommendations identified."),
        "workflow-card",
    )

section_title("Manager summary")
st.text_area("Manager-ready process summary", manager_summary_text, height=220)

section_title("Generated documentation")
doc_tabs = st.tabs([
    "SOP",
    "Checklist",
    "Training Plan",
    "Quality Control",
    "Implementation Plan",
])
with doc_tabs[0]:
    st.text_area("Generated SOP", sop, height=420)
with doc_tabs[1]:
    st.text_area("Generated Checklist", checklist, height=360)
with doc_tabs[2]:
    st.text_area("Generated Training Plan", training, height=420)
with doc_tabs[3]:
    st.text_area("Generated Quality Control Guide", quality, height=390)
with doc_tabs[4]:
    st.text_area("Generated Implementation Plan", implementation, height=390)

section_title("Download SOP package")
st.download_button(
    "Download SOP Package",
    data=full_package,
    file_name="soppilot-sop-package.md",
    mime="text/markdown",
    use_container_width=True,
)

st.markdown(
    '<div class="note-box">Privacy note: Information entered into this app is processed during the active session and is not saved by this app.</div>',
    unsafe_allow_html=True,
)
