# Project Structure

```text
.
├── app.py                  # Streamlit application entrypoint
├── README.md               # Project overview, case study, and test flow
├── ARCHITECTURE.md         # Architecture and design decisions
├── PROJECT_STRUCTURE.md    # Repository structure reference
├── DEVELOPMENT_NOTES.md    # Implementation notes and future refactor plan
├── requirements.txt        # Python dependencies
└── screenshots/            # README screenshots
```

## Current File Responsibilities

### `app.py`

Contains the deployed Streamlit process documentation app.

Responsibilities:

- Page configuration
- Process sample data
- SOP builder workflow
- Complexity scoring
- Risk diagnosis
- Documentation readiness scoring
- SOP generation
- Checklist generation
- Training plan generation
- Quality control guide generation
- Implementation plan generation
- Markdown package export
- Streamlit UI rendering

## Future Production Structure

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

The current structure prioritizes fast deployment and public portfolio review while documenting a path toward a modular production build.
