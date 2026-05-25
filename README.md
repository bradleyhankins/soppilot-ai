# SOPPilot AI

SOPPilot AI is an AI-enhanced process documentation and training workflow assistant for small-business teams. It turns rough process notes into structured SOPs, checklists, missing-information checks, risk diagnoses, training plans, quality control guides, implementation plans, and downloadable documentation packages.

## Live Demo

[Launch SOPPilot AI](https://soppilot-ai.streamlit.app/)

## Current Version: v2.4

SOPPilot AI combines a rules-based process documentation engine with embedded AI-enhanced SOP package generation.

The app works in two layers:

1. **Rules-based core:** creates SOPs, checklists, training plans, quality control guides, implementation plans, readiness scores, risk checks, version-control blocks, and manager summaries.
2. **Embedded AI layer:** when an OpenAI token is available, the app improves the complete SOP package into a cleaner, more manager-ready document.

If the AI call fails or an API key is unavailable, the app falls back to the rules-based SOP package. The user experience stays the same.

## Architecture

SOPPilot has been refactored from a single-file Streamlit prototype into a modular application.

```text
soppilot-ai/
├── app.py
├── ai_helpers.py
├── pdf_helpers.py
├── requirements.txt
├── core/
│   ├── __init__.py
│   ├── prompts.py
│   ├── report_builder.py
│   └── sop_logic.py
├── data/
│   ├── __init__.py
│   └── sample_data.py
└── .github/
    └── workflows/
        └── python-checks.yml
```

### Module Responsibilities

- `app.py` handles Streamlit layout, form inputs, rendering, and orchestration.
- `core/sop_logic.py` contains step cleanup, complexity scoring, role guidance, quality standards, missing-info checks, risk diagnosis, readiness scoring, recommendations, and the main workflow runner.
- `core/report_builder.py` builds the SOP, checklist, training plan, quality control guide, implementation plan, manager summary, and complete documentation package.
- `core/prompts.py` contains the AI enhancement prompt.
- `data/sample_data.py` stores dropdown options, sample process scenarios, and public-demo privacy notes.
- `ai_helpers.py` manages OpenAI access, guardrails, prompt length control, stable cache keys, and fallback behavior.
- `pdf_helpers.py` converts structured report text into a downloadable PDF.

## AI Design Pattern

```text
Rules decide. AI polishes. Guardrails constrain. Fallback protects.
```

The rules-based workflow remains the source of truth for:

- Documentation readiness score
- Complexity label and score
- Risk diagnosis
- Rollout readiness
- Missing-information check
- Improvement recommendations
- Version-control block
- Generated SOP/checklist/training/quality-control package

The AI layer is used only to improve readability, clarity, and structure of the complete SOP package.

## Privacy Note

This public demo is designed for fictional or sample data. Users should not enter sensitive, confidential, or unnecessary business information. When AI enhancement is enabled, entered process notes may be processed by the configured AI provider for output enhancement.

## Why this project exists

Small and mid-sized businesses often rely on tribal knowledge, verbal instructions, scattered notes, and inconsistent training. SOPPilot AI helps convert rough process knowledge into repeatable documentation.

## Workflow Outputs

- Public-safe sample process scenarios
- Process ownership inputs
- Process risk and usage inputs
- Rough workflow input
- Quality and escalation inputs
- Documentation readiness score
- Version-control block
- Process complexity logic
- Risk diagnosis logic
- Rollout readiness guidance
- Missing-information check
- Improvement recommendations
- Manager-ready process summary
- Standard Operating Procedure generator
- Process checklist generator
- Training plan generator
- Quality control guide generator
- Implementation plan generator
- AI-enhanced complete SOP package with rules-based fallback
- Downloadable PDF SOP package

## Export Strategy

Current user-facing export:

- PDF SOP package for a manager/training-ready deliverable

## Suggested Test Flow

1. Launch the live demo.
2. Load the “New Lead Follow-Up” sample process.
3. Generate the SOP package.
4. Review the documentation readiness score, version-control block, complexity, risk diagnosis, and rollout readiness snapshot.
5. Review the missing-information check and improvement recommendations.
6. Review the SOP, checklist, training plan, quality control guide, implementation plan, and AI-enhanced complete package.
7. Download the PDF SOP package.

## Automated Checks

This repo includes a GitHub Actions workflow that runs:

```bash
python -m compileall .
```

This catches syntax and import issues after modular refactors.

## Screenshots

Screenshots will be refreshed after the final UI and PDF polish pass.

## Tech Stack

- Python
- Streamlit
- OpenAI API integration
- Rules-based process documentation logic
- Modular app architecture
- Silent AI fallback pattern
- AI guardrails
- PDF report export
- GitHub Actions syntax checks
- GitHub
- Streamlit Community Cloud

## Run Locally

```bash
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

## Environment Variables

To enable embedded AI output:

```bash
OPENAI_TOKEN=your_api_key_here
```

The app still works without this token by using the rules-based fallback.

## Public Demo Note

All sample data, names, companies, and scenarios used in this project are fictional and created for public portfolio demonstration purposes.

## Case Study

### Problem

Small and mid-sized businesses often rely on scattered notes and inconsistent training. This creates confusion when processes need to be repeated, taught, reviewed, or improved.

### Solution

SOPPilot AI turns rough process details into a complete SOP package with scoring, version control, risk guidance, checklists, training plans, quality control, and implementation planning. The embedded AI layer improves the complete package when available while preserving a reliable rules-based fallback.

### Business Value

SOPPilot AI helps small and mid-sized businesses turn informal knowledge into repeatable process documentation.

## Built By

Bradley Hankins  
Operations & Revenue Leader | AI Workflow Automation | RevOps & Process Improvement
