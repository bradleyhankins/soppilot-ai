import streamlit as st

from ai_helpers import generate_ai_text

st.set_page_config(page_title="SOPPilot AI - AI SOP Writer", page_icon="📋", layout="wide")

st.title("AI SOP Writer")
st.caption("Optional AI enhancement for turning messy process notes into structured SOP drafts.")

st.info(
    "This page is optional. The main SOPPilot workflow still works without AI. "
    "Set OPENAI_TOKEN in the deployment environment to enable AI output."
)

process_name = st.text_input("Process name", placeholder="Example: New Lead Follow-Up Process")
owner = st.text_input("Process owner / role", placeholder="Example: Sales Representative")
rough_notes = st.text_area(
    "Messy process notes",
    height=240,
    placeholder="Paste rough notes, bullet points, or a messy workflow description here.",
)
focus = st.multiselect(
    "What should the AI focus on?",
    ["SOP", "Checklist", "Training Plan", "Quality Control", "Escalation Path", "Process Gaps"],
    default=["SOP", "Checklist", "Process Gaps"],
)

if st.button("Generate AI SOP Draft", use_container_width=True):
    prompt = f"""
You are an operations documentation specialist.
Turn the rough process notes into a clear, practical process document.
Do not invent company-specific policies. If information is missing, list it as a gap.

Process name: {process_name}
Owner or role: {owner}
Focus areas: {', '.join(focus)}

Rough process notes:
{rough_notes}

Return:
1. Clean SOP draft
2. Process checklist
3. Missing information / process gaps
4. Escalation recommendations
5. Training notes for a manager
"""
    with st.spinner("Generating AI SOP draft..."):
        st.markdown(generate_ai_text(prompt))

st.divider()
st.markdown(
    "**AI positioning:** This page adds a natural-language drafting layer on top of SOPPilot's structured, rules-based documentation workflow."
)
