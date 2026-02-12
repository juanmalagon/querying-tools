# Querying Tools — bias-aware literature review helpers

This repository provides tools, utilities, and example workflows to help researchers build and run literature-review queries with reduced bias and improved reproducibility. The codebase focuses on query construction, provider-specific helpers (e.g., Scopus), and experiment scripts/notebooks that demonstrate more systematic search strategies.

## Quick links

- Documentation: [docs/PROJECT_DOCUMENTATION.md](docs/PROJECT_DOCUMENTATION.md)
- Main requester script: `unbiased_requester.py`
- Utilities: `utils/` and `resources/`
- Example notebooks: [experiments/](experiments/)

## Why this project exists

Systematic literature reviews and meta-analyses depend heavily on search queries. Small, implicit choices in query wording, filters, or provider APIs can introduce selection bias. This project collects tools and best-practice examples to make query design explicit, repeatable, and easier to audit.

## Key features

- Query-building helpers and templates for reproducible searches
- Provider-specific adapters (Scopus helper functions included)
- Notebooks and scripts for running experiments and demonstrations
- Utilities for storing/configuring API credentials and running batch requests

## Installation

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

- Place provider config (e.g., Scopus credentials) in the `scopus/` folder per the placeholder instruction.
- Inspect `env_variables.py` for environment keys and paths used across scripts.

Quickstart

1. Read the full project documentation: [docs/PROJECT_DOCUMENTATION.md](docs/PROJECT_DOCUMENTATION.md)

2. Run the interactive requester (example):

```bash
streamlit run unbiased_requester.py
```

3. Or run programmatically from Python:

```python
from utils.query_tools import build_query
from utils.handler import RequestHandler

q = build_query(...)  # see docs for arguments
handler = RequestHandler()
res = handler.run(q)
```

## Examples and experiments

- Open the notebooks in `experiments/` to see step-by-step examples and small reproducible runs.
- Use `resources/examples.py` and `utils/examples.py` as starting points for adapting queries to your topic.

## Contributing

- Please open issues or pull requests. When changing usage or APIs, update [docs/PROJECT_DOCUMENTATION.md](docs/PROJECT_DOCUMENTATION.md).

## Troubleshooting

- If packages are missing, ensure your virtual environment is active and run `pip install -r requirements.txt`.
- For Scopus/Elsevier API access, request an API key at https://dev.elsevier.com/apikey/manage and follow the authentication guidance in the docs.

## License

See the repository `LICENSE` file for license terms.