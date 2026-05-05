# Querying Tools

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/python-3.12-blue?logo=python">
  <img alt="License" src="https://img.shields.io/badge/license-Apache%202.0-green">
  <img alt="Streamlit" src="https://img.shields.io/badge/built%20with-Streamlit-red?logo=streamlit">
  <img alt="Paper DOI" src="https://img.shields.io/badge/DOI-10.1111%2Fitor.70207-blue?logo=doi">
</p>

Bias-assessment and querying utilities for Scopus-based literature reviews — a companion tool for the paper:

> **Malagon, J., & Haelermans, C. (2026).** Systematic Flaws: Uncovering Biases and Replicability Challenges in Literature Reviews on Efficiency of Education. *International Transactions in Operational Research*.  
> [DOI: 10.1111/itor.70207](https://doi.org/10.1111/itor.70207)

---

## Features

A Streamlit app that retrieves data from Scopus and runs four bias-assessment tools:

- **🔤 Language bias** — checks for language restrictions in the result set
- **📊 Publication bias** — analyses publication outlet patterns
- **🌍 Localization bias** — maps geographic distribution of results
- **🔓 Availability bias** — assesses full-text accessibility

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/juanmalagon/querying-tools.git
cd querying-tools

# 2. Install development dependencies
pip install -r requirements-dev.txt

# 3. Install pre-commit hooks (optional but recommended)
pre-commit install

# 4. Run basic checks
ruff check .
ruff format --check .
pytest

# 5. Launch the app
streamlit run unbiased_requester.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

> **No Scopus key needed to start.** Without credentials the app opens and shows a warning; live retrieval will be disabled.

---

## Usage

### Scopus Credentials

Choose one of the following (**Option A is recommended for production**):

**Option A — Environment variable (recommended):**

```bash
export SCOPUS_API_KEY="your_api_key_here"
```

You can also copy `.env.example` to `.env` and fill in your key:

```bash
cp .env.example .env
# edit .env with your real key
```

**Option B — Config file (for local development):**

Copy the example and edit it:

```bash
cp scopus/config.example.json scopus/config.json
# edit scopus/config.json with your real key
```

The resulting file should look like:

```json
{
  "apikey": "your_scopus_api_key_here"
}
```

> **⚠️ Never commit `scopus/config.json` or `.env`.** Both are in `.gitignore`.

### Running

```bash
streamlit run unbiased_requester.py
```

Then open `http://localhost:8501`.

### Quick test without credentials

The app opens and shows a Scopus credentials warning — live retrieval is disabled
but the UI and example queries remain accessible.

---

## Development

See **[DEVELOPMENT.md](DEVELOPMENT.md)** for:
- Full project structure and architecture
- EditorConfig, pre-commit hooks, and CI pipeline
- Detailed configuration reference
- Local development setup and contributing guide

---

## Docker

```bash
docker build -t querying-tools .
docker run -p 8501:8501 -e SCOPUS_API_KEY=your_key_here querying-tools
```

---

## Documentation

| Resource | Description |
|----------|-------------|
| **[DEVELOPMENT.md](DEVELOPMENT.md)** | Technical deep-dive: project structure, detailed setup, configuration, testing, and contributing |
| **Unbiased requester** | The app entry point — `unbiased_requester.py` |
| **Configuration** | `.env.example` for environment variables; `app_config.py` for settings loading |

---

## Deployment Notes

- Keep the Scopus API key server-side only.
- Container deployment is recommended for first release.

---

## License

Distributed under the Apache License 2.0. See [LICENSE](LICENSE) for details.
