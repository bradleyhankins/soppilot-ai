# Architecture

SOPPilot AI is a Streamlit process documentation and training workflow assistant for small-business teams.

## Current Architecture

The current version is optimized for simple Streamlit Community Cloud deployment and easy GitHub review.

```text
app.py
README.md
requirements.txt
screenshots/
```

## Application Layers

The app is currently deployed from one Streamlit entrypoint, but the code is organized conceptually into clear layers:

```text
Configuration
- Departments
- Owner roles
- Risk levels
- Process samples

Process Analysis Logic
- Complexity scoring
- Missing information checks
- Risk diagnosis
- Rollout readiness logic
- Documentation readiness scoring

Document Generation
- SOP generation
- Checklist generation
- Training plan generation
- Quality control guide generation
- Implementation plan generation
- Version control block generation
- Downloadable Markdown package

Presentation
- Streamlit builder form
- Snapshot cards
- Documentation tabs
- Download workflow
```

## Design Choices

SOPPilot uses rules-based process logic to keep recommendations transparent and easy to adapt.

Key design goals:

- Reduce tribal knowledge
- Improve process documentation
- Improve training consistency
- Clarify process ownership
- Add version-control thinking to SOP workflows
- Generate manager-ready documentation

## Why Single-File for This Version

The current single-file app keeps deployment simple for a portfolio project. A production version would separate scoring, templates, components, and exports.

## Future Production Layout

```text
app.py
src/
  config.py
  process_analysis.py
  document_templates.py
  reports.py
  components.py
  styles.css
tests/
  test_process_analysis.py
  test_document_templates.py
```

## Future Refactor Plan

1. Move CSS into `styles.css`
2. Move process scoring into `src/process_analysis.py`
3. Move document generation into `src/document_templates.py`
4. Move exports into `src/reports.py`
5. Add tests for readiness score and missing information logic
