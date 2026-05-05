# Development Guide

Technical documentation for contributors and maintainers of **Querying Tools**.

---

## Project Structure

```
querying-tools/
├── unbiased_requester.py      # Streamlit app — entry point
├── app_config.py              # Settings loading (env vars, config files)
├── pyproject.toml             # Project metadata, tool configuration
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Dev dependencies (testing, linting)
├── requirements-research.txt  # Notebook / exploratory dependencies
├── Dockerfile                 # Container build
├── .env.example               # Environment variable template
├── .editorconfig              # Cross-editor coding style
├── .pre-commit-config.yaml    # Pre-commit hooks (linting, formatting)
│
├── resources/                 # Core logic modules
│   ├── querying_tools.py      # Bias-assessment tool implementations
│   ├── scopus_functions.py    # Scopus API interaction helpers
│   ├── examples.py            # Example queries
│   ├── country_lists.py       # Country/region data for localization
│   └── __init__.py
│
├── tests/                     # Automated tests
│   ├── test_app_config.py     # Configuration loading tests
│   ├── test_querying_tools.py # Bias-assessment tool tests
│   └── test_scopus_functions.py  # Scopus API helper tests
│
├── scopus/                    # Scopus API configuration
│   └── config.example.json    # Example config — copy to config.json and fill in
│
├── experiments/               # Jupyter notebooks
│   ├── unbiased_requester_nb.ipynb
│   └── summarize_localized_data.ipynb
│
└── .github/                   # GitHub-specific configuration
    ├── CODEOWNERS             # Repository ownership
    └── workflows/
        └── ci.yml             # Continuous integration pipeline
```

---

## Detailed Setup

### 1. Python Environment

Requires **Python 3.12**. We recommend using a virtual environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

| File | Use case |
|------|----------|
| `requirements.txt` | Production runtime only |
| `requirements-dev.txt` | Development + testing + linting |
| `requirements-research.txt` | Jupyter notebooks / exploration |

```bash
# Runtime only
pip install -r requirements.txt

# Development (includes runtime)
pip install -r requirements-dev.txt

# Research (includes dev + runtime)
pip install -r requirements-research.txt
```

### 3. EditorConfig

The `.editorconfig` file ensures consistent coding style across editors. Supported editors
(VS Code, PyCharm, etc.) will automatically apply these settings:

- UTF-8 encoding
- LF line endings, trailing newline
- Spaces for indentation (4 spaces for Python, 2 for YAML/JSON/TOML)
- Trailing whitespace trimmed (except in Markdown)

### 4. Configuration

All settings are driven by environment variables. Copy `.env.example` and adjust:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SCOPUS_API_KEY` | Yes* | — | Scopus API key |
| `SCOPUS_CONFIG_FILE` | No | — | Alternative config file path |
| `SCOPUS_DATA_DIR` | No | `./data` | Export directory |
| `SAVE_TO_CSV` | No | `0` | Enable CSV persistence (`1` / `true`) |
| `LOG_LEVEL` | No | `INFO` | Logging verbosity |

*\* Without a Scopus API key, the app starts but live retrieval is disabled.*

Alternatively, place a config file in the `scopus/` directory:

```bash
cp scopus/config.example.json scopus/config.json
# edit scopus/config.json with your real key
```

The config file uses this format:

```json
{
  "apikey": "your_scopus_api_key_here"
}
```

> **⚠️ Never commit `scopus/config.json` or `.env`.** Both are listed in `.gitignore`.

---

## Pre-commit Hooks

The project uses [pre-commit](https://pre-commit.com/) to run Ruff (linting + formatting)
before every commit. Install the hooks:

```bash
pre-commit install
```

After setup, `ruff` and `ruff format` will run automatically on staged files when you
commit. To run manually against all files:

```bash
pre-commit run --all-files
```

---

## Testing & Linting

```bash
# Run linter
ruff check .

# Run formatter check
ruff format --check .

# Run tests
pytest
```

Both commands should pass before committing. The test suite covers:

- Configuration loading and credential resolution (`test_app_config.py`)
- Bias-assessment tools: language, publication, and localization (`test_querying_tools.py`)
- Scopus API helpers: data conversion and transformations (`test_scopus_functions.py`)

The `pyproject.toml` configures:

- **Ruff** — line length 88, Python 3.12 target, excludes `experiments/` directory
- **pytest** — test discovery in `tests/`, adds project root to `PYTHONPATH`

---

## Continuous Integration (CI)

GitHub Actions runs on every push and pull request to `main` (see `.github/workflows/ci.yml`):

| Step | Command |
|------|---------|
| Install dependencies | `pip install -e ".[dev]"` |
| Run tests | `pytest tests/` |
| Lint | `ruff check .` |
| Format check | `ruff format --check .` |

All steps must pass for the workflow to succeed.

---

## Docker

```bash
# Build
docker build -t querying-tools .

# Run with API key
docker run -p 8501:8501 -e SCOPUS_API_KEY=your_key_here querying-tools

# Run without API key (retrieval disabled)
docker run -p 8501:8501 querying-tools
```

The Docker image is based on `python:3.12-slim` and exposes port **8501**.

---

## Application Architecture

### Entry Point — `unbiased_requester.py`

A Streamlit application that:

1. Loads an example query from `resources/examples.py`
2. Calls the Scopus API via `resources/scopus_functions.py` to retrieve data
3. Provides four bias-assessment tools from `resources/querying_tools.py`
4. Displays results interactively in the browser

### Configuration — `app_config.py`

The `AppSettings` class loads and validates configuration from environment variables and config files.
Additionally, `configure_logging()` provides a centralized logging setup used by both the Streamlit
app and the library modules. `AppSettings` exposes:

- `from_env()` — factory method to load settings
- `has_scopus_credentials()` — checks if credentials are available
- `resolve_scopus_api_key()` — resolves the API key from env or file

### Bias-Assessment Tools — `resources/querying_tools.py`

Four tools are available:

| Tool | Purpose |
|------|---------|
| `language_bias_tool` | Analyse language distribution in results |
| `publication_bias_tool` | Examine publication outlet patterns |
| `localization_bias_tool` | Map geographic representation |
| *(availability bias)* | Assess full-text access rates |

---

## Notebooks & Experiments

Notebooks in `experiments/` demonstrate research workflows:

- `unbiased_requester_nb.ipynb` — interactive version of the bias-assessment pipeline
- `summarize_localized_data.ipynb` — analysis of geographically tagged results

Install research dependencies and launch Jupyter:

```bash
pip install -r requirements-research.txt
jupyter notebook
```

---

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Run tests and linting: `ruff format --check . && ruff check . && pytest`.
5. Commit with a clear message.
6. Open a pull request.

---

## License

[Apache License 2.0](LICENSE)