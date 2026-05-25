DEPARTMENTS = ["Sales", "Operations", "Customer Service", "Production / Project Management", "Recruiting / HR", "Administration", "Other"]
OWNER_ROLES = ["Sales Representative", "Sales Manager", "Operations Manager", "Project Manager", "Customer Service Representative", "Recruiter / Hiring Manager", "General Team Member"]
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

PRIVACY_NOTE = "Privacy note: Use fictional/sample data for public demos. Do not enter sensitive, confidential, regulated, or unnecessary business information. If AI is enabled, entered text may be processed by the configured AI provider for output enhancement."
