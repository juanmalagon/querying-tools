# Testing and validation

## Minimal validation for a fresh clone

Install development dependencies:

`pip install -r requirements-dev.txt`

Run automated checks:

- `ruff check .`
- `pytest`

These checks confirm that:

- configuration helpers load correctly
- core query transformation helpers behave as expected

## Manual application checks

### Check 1: startup without credentials

1. Make sure `SCOPUS_API_KEY` is not set.
2. Run:

   `streamlit run unbiased_requester.py`

3. Confirm the app opens and shows a credentials warning.

### Check 2: live retrieval with credentials

1. Configure `SCOPUS_API_KEY` or `scopus/config.json`.
2. Start the app.
3. Load the example query.
4. Test these actions:
   - retrieve original query data
   - apply language-bias tool
   - apply publication-bias tool
   - apply localization-bias tool
   - apply availability-bias tool

## Current test scope

Automated tests are intentionally light. They do not yet cover:

- end-to-end Streamlit behavior
- live Scopus integration
- deployment smoke tests

Those should be added in a later hardening pass.
