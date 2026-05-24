# Development Notes

## Build Philosophy

SOPPilot AI is designed as a practical process documentation workflow assistant.

The app focuses on turning rough process knowledge into usable SOPs, checklists, training plans, and quality-control guides.

## Engineering Priorities

1. Clear SOP builder workflow
2. Transparent readiness and risk logic
3. Manager-ready documentation output
4. Public-safe sample process scenarios
5. Downloadable Markdown packages
6. Simple deployment on Streamlit Community Cloud

## Current Tradeoffs

The app currently keeps deployment logic in `app.py` for simplicity and easy review. A future production version should split analysis logic, document templates, components, and styling into separate modules.

## Future Refactor Plan

A future production-oriented version should split the app into:

```text
src/config.py
src/process_analysis.py
src/document_templates.py
src/reports.py
src/components.py
src/styles.css
```

## Testing Opportunities

The most valuable future tests would cover:

- Complexity scoring
- Missing information checks
- Risk diagnosis
- Documentation readiness score
- Version control block generation
- SOP template generation
- Markdown package export

## Code Quality Roadmap

Potential future tooling:

- Ruff for linting and formatting
- Pytest for process logic tests
- Pre-commit hooks
- GitHub Actions smoke checks
