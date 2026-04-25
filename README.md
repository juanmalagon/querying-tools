# Querying Tools

Querying and bias-assessment utilities for Scopus-based literature review workflows.

This repository accompanies the paper:

Malagon J, Haelermans C. _Biases and reproducibility challenges in literature reviews - The case of efficiency of education reviews. 2023_

## Quick start

For a person who just cloned the repository:

1. Use Python 3.12.
2. Install development dependencies:

   `pip install -r requirements-dev.txt`

3. Run the basic checks:

   - `ruff check .`
   - `pytest`

4. Start the app:

   `streamlit run unbiased_requester.py`

5. Open:

   `http://localhost:8501`

At this point, the app should start even without Scopus credentials. Without a key, it should show a warning and the live retrieval features will not work.

## Application status

The project includes minimum deployment-oriented features:

- environment-based configuration
- slim production dependencies
- Docker support
- CI checks
- basic automated tests

This is a deployable baseline, not yet a fully hardened production service.

## Local run

### 1. Install dependencies

Runtime only:

`pip install -r requirements.txt`

Development checks:

`pip install -r requirements-dev.txt`

Notebook and exploratory work:

`pip install -r requirements-research.txt`

### 2. Configure Scopus credentials

Choose one of these options.

#### Option A: environment variable

PowerShell:

`$env:SCOPUS_API_KEY="your_api_key_here"`

Command Prompt:

`set SCOPUS_API_KEY=your_api_key_here`

#### Option B: config file

Create `scopus/config.json` with:

```json
{
  "apikey": "your_api_key_goes_here"
}
```

### 3. Start the application

`streamlit run unbiased_requester.py`

Open `http://localhost:8501` in your browser.

### 4. Manual test flow

Without credentials:

- confirm the app opens
- confirm it shows a Scopus credentials warning

With valid credentials:

- load the example query
- retrieve original query data
- run the language-bias tool
- run the publication-bias tool
- run the localization-bias tool
- run the availability-bias tool

## Environment variables

Copy [.env.example](.env.example) and configure these values in your host or container environment:

- `SCOPUS_API_KEY`
- `SCOPUS_CONFIG_FILE` optional fallback path
- `SCOPUS_DATA_DIR` optional export directory
- `SAVE_TO_CSV` set to `1` or `true` to persist exports
- `LOG_LEVEL`

## Docker

Build the container:

`docker build -t querying-tools .`

Run it:

`docker run -p 8501:8501 -e SCOPUS_API_KEY=your_key_here querying-tools`

## Testing

Automated checks:

- `ruff check .`
- `pytest`

Manual checks:

- app startup without credentials
- live retrieval with valid Scopus credentials

## Documentation

Additional project documentation is available in [docs/README.md](docs/README.md):

- [Setup and local usage](docs/setup.md)
- [Testing and validation](docs/testing.md)
- [Deployment notes](docs/deployment.md)

## Deployment notes

- Keep the Scopus API key server-side only.
- Prefer container deployment for first release.

## Troubleshooting

- On Windows, if you hit encoding issues during installation, run `set PYTHONUTF8=1` before installing packages.
- If the app starts but retrieval fails, verify that `SCOPUS_API_KEY` is set or that `scopus/config.json` exists and contains valid JSON.