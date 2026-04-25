# Setup and local usage

## Prerequisites

- Python 3.12
- A Scopus API key if you want to test live data retrieval
- Optional: Docker for container-based testing

## Fresh clone setup

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install runtime dependencies:

   `pip install -r requirements.txt`

4. For development checks, install:

   `pip install -r requirements-dev.txt`

## Configure credentials

### Requesting Your Elsevier API Key

To get started with Elsevier APIs, you’ll first need to request your personal API key:
**[Request your Elsevier API key](https://dev.elsevier.com/apikey/manage)**

### Helpful Documentation

If you need more context or run into issues, these official resources can guide you:

* **[API Authentication Guide](https://dev.elsevier.com/tecdoc_api_authentication.html)**
  Learn how authentication works and how to securely use your API key.

* **[Authentication API Specification](https://dev.elsevier.com/documentation/AuthenticationAPI)**
  Detailed technical documentation for implementing authentication in your applications.

These resources should give you everything you need to get up and running smoothly.

### Use your API Key

Afterwards, choose one option.

#### Option A: environment variable

PowerShell:

`$env:SCOPUS_API_KEY="your_api_key_here"`

Command Prompt:

`set SCOPUS_API_KEY=your_api_key_here`

#### Option B: config file

Create `scopus/config.json` with:

```json
{
  "apikey": "your_api_key_here"
}
```

## Run the app

Start Streamlit:

`streamlit run unbiased_requester.py`

Then open:

`http://localhost:8501`

## First-run expectations

- Without Scopus credentials, the app should start and show a warning.
- With valid Scopus credentials, the example query should retrieve live results.
