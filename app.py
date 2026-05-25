import streamlit as st

from ai_helpers import enhance_text, stable_cache_key
from core.prompts import sop_enhancement_prompt
from core.report_builder import build_documents, version_control_block
from core.sop_logic import readiness_score_status, run_sop_workflow
from data.sample_data import (
    DEPARTMENTS,
    FREQUENCIES,
    OWNER_ROLES,
    PRIVACY_NOTE,
    RISK_LEVELS,
    SAMPLE_PROCESSES,
    TEAM_SIZES,
)
from pdf_helpers import markdown_to_pdf

st.set_page_config(page_title="SOPPilot AI", page_icon="📋", layout="wide")

CSS = """
<style>
.block-container{max-width:1180px;padding-top:1.35rem;padding-bottom:3rem}[data-testid="stSidebar"]{background:#111827}[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3,[data-testid="stSidebar"] p,[data-testid="stSidebar"] span,[data-testid="stSidebar"] label,[data-testid="stSidebar"] li,[data-testid="stSidebar"] ul,[data-testid="stSidebar"] ol{color:#f9fafb!important}[data-testid="stSidebar"] li::marker{color:#93c5fd!important}.hero{padding:1.9rem 2rem;border-radius:20px;background:linear-gradient(135deg,#111827 0%,#1f2937 52%,#334155 100%);color:#fff;box-shadow:0 18px 36px rgba(17,24,39,.18);margin-bottom:1rem}.eyebrow{text-transform:uppercase;letter-spacing:.13em;font-size:.75rem;font-weight:800;color:#93c5fd;margin-bottom:.65rem}.hero-title{font-size:2.25rem;line-height:1.08;font-weight:850;margin-bottom:.65rem}.hero-subtitle{font-size:1.02rem;line-height:1.62;color:#e5e7eb;max-width:900px}.hero-pills span{display:inline-block;padding:.35rem .65rem;margin:.75rem .28rem 0 0;border-radius:999px;background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.16);font-weight:700;font-size:.78rem;color:#f8fafc}.section-title{margin-top:1.25rem;margin-bottom:.55rem;font-size:1.4rem;font-weight:850;color:#111827}.section-lede{color:#4b5563;line-height:1.6;margin-bottom:1rem;max-width:950px}.form-group-title{font-size:.9rem;font-weight:850;text-transform:uppercase;letter-spacing:.06em;color:#64748b;margin:.35rem 0 .15rem 0}.metric-card,.output-card,.success-card,.warning-card,.workflow-card{background:#fff;border:1px solid #e5e7eb;border-radius:18px;box-shadow:0 8px 20px rgba(15,23,42,.055)}.metric-card{height:138px;padding:1rem;margin-bottom:.75rem}.metric-label{color:#6b7280;font-size:.78rem;font-weight:800;text-transform:uppercase;letter-spacing:.05em;margin-bottom:.5rem}.metric-value{color:#111827;font-size:1.35rem;line-height:1.18;font-weight:900;overflow-wrap:break-word}.metric-note{color:#64748b;font-size:.85rem;margin-top:.55rem}.output-card,.success-card,.warning-card,.workflow-card{padding:1.15rem;margin-bottom:.8rem}.output-card{border-left:5px solid #111827}.success-card{border-left:5px solid #059669}.warning-card{border-left:5px solid #f59e0b}.workflow-card{border-left:5px solid #1d4ed8}.output-card h3,.success-card h3,.warning-card h3,.workflow-card h3{font-size:1.05rem;font-weight:850;color:#111827;margin-bottom:.4rem}.output-card p,.success-card p,.warning-card p,.workflow-card p,.output-card li,.success-card li,.warning-card li,.workflow-card li{color:#4b5563;line-height:1.52;font-size:.93rem}.note-box{padding:.9rem 1rem;border-radius:14px;background:#f8fafc;color:#334155;border:1px solid #e2e8f0;font-weight:650;margin:.9rem 0;font-size:.92rem}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def section_title(title: str, lede: str | None = None) -> None:
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if lede:
        st.markdown(f'<div class="section-lede">{lede}</div>', unsafe_allow_html=True)


def form_group(title: str) -> None:
    st.markdown(f'<div class="form-group-title">{title}</div>', unsafe_allow_html=True)


def metric_card(label: str, value: str, note: str | None = None) -> None:
    note_html = f'<div class="metric-note">{note}</div>' if note else ""
    st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div>{note_html}</div>', unsafe_allow_html=True)


def html_card(title: str, body: str, css_class: str = "output-card") -> None:
    st.markdown(f'<div class="{css_class}"><h3>{title}</h3>{body}</div>', unsafe_allow_html=True)


def html_list(items: list[str], empty_message: str) -> str:
    visible_items = items or [empty_message]
    return "<ul>" + "".join(f"<li>{item}</li>" for item in visible_items) + "</ul>"


def render_sidebar() -> None:
    with st.sidebar:
        st.title("SOPPilot AI")
        st.caption("Version 2.4")
        st.markdown("Process documentation and training workflow assistant for small-business teams.")
        st.divider()
        st.markdown("### Outputs")
        st.markdown("- Readiness score\n- Version control block\n- Standard Operating Procedure\n- Process checklist\n- Risk diagnosis\n- Training plan\n- Quality control guide\n- PDF SOP package")


def render_hero() -> None:
    st.markdown(
        '<div class="hero"><div class="eyebrow">Process Documentation Workflow Tool</div><div class="hero-title">SOPPilot AI</div><div class="hero-subtitle">Turn rough process notes into SOPs, process checklists, missing-information checks, risk diagnoses, training plans, quality control guides, implementation plans, and downloadable documentation packages.</div><div class="hero-pills"><span>SOPs</span><span>Training</span><span>Quality Control</span><span>Implementation</span><span>Streamlit</span></div></div>',
        unsafe_allow_html=True,
    )


def build_inputs() -> dict | None:
    scenario_name = st.selectbox("Load Sample Process", list(SAMPLE_PROCESSES.keys()))
    scenario = SAMPLE_PROCESSES.get(scenario_name, {})

    with st.form("sop_form"):
        form_group("Process ownership")
        a, b, c = st.columns(3)
        with a:
            process_name = st.text_input("Process Name", value=scenario.get("process_name", ""), placeholder="Example: New Lead Follow-Up Process")
        with b:
            department = st.selectbox("Department", DEPARTMENTS, index=DEPARTMENTS.index(scenario.get("department", "Sales")))
        with c:
            owner_role = st.selectbox("Process Owner Role", OWNER_ROLES, index=OWNER_ROLES.index(scenario.get("owner_role", "Sales Representative")))

        form_group("Process risk and usage")
        d, e, f = st.columns(3)
        with d:
            frequency = st.selectbox("How Often Does This Process Happen?", FREQUENCIES, index=FREQUENCIES.index(scenario.get("frequency", "Daily")))
        with e:
            risk = st.selectbox("Risk Level if Done Incorrectly", RISK_LEVELS, index=RISK_LEVELS.index(scenario.get("risk", "Medium")))
        with f:
            team_size = st.selectbox("How Many People Use This Process?", TEAM_SIZES, index=TEAM_SIZES.index(scenario.get("team_size", "1-3 people")))

        form_group("Process details")
        g, h = st.columns(2)
        with g:
            trigger = st.text_area("What Triggers This Process?", value=scenario.get("trigger", ""), height=110, max_chars=4000)
            inputs = st.text_area("Inputs / Information Needed", value=scenario.get("inputs", ""), height=110, max_chars=4000)
        with h:
            goal = st.text_area("What Is the Goal of This Process?", value=scenario.get("goal", ""), height=110, max_chars=4000)
            tools = st.text_area("Tools / Systems Used", value=scenario.get("tools", ""), height=110, max_chars=4000)

        form_group("Rough workflow")
        steps = st.text_area("Rough Process Steps", value=scenario.get("steps", ""), height=190, placeholder="Enter one step per line...", max_chars=8000)

        form_group("Quality and escalation")
        i, j = st.columns(2)
        with i:
            quality_standard = st.text_area("Quality Standard", value=scenario.get("quality", ""), height=110, max_chars=4000)
        with j:
            escalation_path = st.text_area("Escalation Path", value=scenario.get("escalation", ""), height=110, max_chars=4000)
        submitted = st.form_submit_button("Generate SOP Package", use_container_width=True)

    if not submitted:
        return None

    return {
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


def enhance_package(process: dict, full_package: str) -> str:
    return enhance_text(
        sop_enhancement_prompt(process, full_package),
        full_package,
        stable_cache_key("soppilot_package", process),
    )


def render_results(process: dict, workflow: dict, documents: dict, enhanced_package: str, pdf_package: bytes) -> None:
    section_title("SOP package snapshot")
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        metric_card("Readiness Score", f"{workflow['score']}%", readiness_score_status(workflow["score"]))
    with s2:
        metric_card("Complexity", workflow["complexity"], f"Score: {workflow['complexity_score']}")
    with s3:
        metric_card("Risk Diagnosis", workflow["risk_label"])
    with s4:
        metric_card("Readiness", workflow["readiness"])

    html_card("Version Control", "<pre>" + version_control_block(process, workflow["score"]).replace("## Version Control\n", "") + "</pre>", "workflow-card")
    html_card("Complexity Guidance", f"<p>{workflow['complexity_note']}</p>", "workflow-card")
    html_card("Risk Guidance", f"<p>{workflow['risk_note']}</p>", "warning-card")
    html_card("Rollout Readiness", f"<p>{workflow['readiness_note']}</p>", "success-card")

    section_title("Missing information and recommendations")
    m1, m2 = st.columns(2)
    with m1:
        html_card(
            "Missing Information Check",
            html_list(workflow["missing_items"], "No major missing information found."),
            "warning-card" if workflow["missing_items"] != ["No major missing information found."] else "success-card",
        )
    with m2:
        html_card("Improvement Recommendations", html_list(workflow["recommendations"], "No major recommendations identified."), "workflow-card")

    section_title("Manager summary")
    st.text_area("Manager-ready process summary", documents["manager_summary"], height=240)

    section_title("Generated documentation")
    tabs = st.tabs(["SOP", "Checklist", "Training Plan", "Quality Control", "Implementation Plan", "Complete Package"])
    with tabs[0]:
        st.text_area("Generated SOP", documents["sop"], height=420)
    with tabs[1]:
        st.text_area("Generated Checklist", documents["checklist"], height=360)
    with tabs[2]:
        st.text_area("Generated Training Plan", documents["training"], height=420)
    with tabs[3]:
        st.text_area("Generated Quality Control Guide", documents["quality"], height=390)
    with tabs[4]:
        st.text_area("Generated Implementation Plan", documents["implementation"], height=390)
    with tabs[5]:
        st.text_area("Complete Documentation Package", enhanced_package, height=520)

    section_title("Download SOP package")
    st.download_button("Download SOP Package PDF", data=pdf_package, file_name="soppilot-sop-package.pdf", mime="application/pdf", use_container_width=True)


def main() -> None:
    render_sidebar()
    render_hero()

    section_title("SOP builder", "Load a fictional sample process or enter your own rough process notes. SOPPilot will organize the process into a complete documentation package.")
    st.markdown(f'<div class="note-box">{PRIVACY_NOTE}</div>', unsafe_allow_html=True)

    process = build_inputs()
    if process is None:
        st.markdown('<div class="note-box">Complete the form or load a sample process, then click Generate SOP Package.</div>', unsafe_allow_html=True)
        return

    workflow = run_sop_workflow(process)
    documents = build_documents(process, workflow)
    enhanced_package = enhance_package(process, documents["full_package"])
    pdf_package = markdown_to_pdf(enhanced_package, title="SOPPilot AI SOP Package")

    render_results(process, workflow, documents, enhanced_package, pdf_package)

    section_title("What this app demonstrates")
    html_card(
        "Portfolio Skills Shown",
        "<ul><li>Modular Streamlit architecture</li><li>AI-enhanced SOP package with rules-based fallback</li><li>Process mapping and documentation logic</li><li>Risk and readiness scoring</li><li>Version-control style business documentation</li><li>User-friendly PDF SOP packages</li></ul>",
        "success-card",
    )
    st.markdown(f'<div class="note-box">{PRIVACY_NOTE}</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
