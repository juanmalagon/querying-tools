# Deployment notes

## Current deployment posture

The project is suitable for a container-based deployment.

Included:

- environment-based configuration
- Dockerfile
- CI workflow
- basic automated tests

Not yet included:

- authentication
- request throttling
- monitoring/alerting
- managed secret integration
- end-to-end smoke tests

## Recommended first deployment

Use any Docker-compatible host

## Required secrets

At minimum, configure:

- `SCOPUS_API_KEY`

Optional:

- `SCOPUS_DATA_DIR`
- `SAVE_TO_CSV`
- `LOG_LEVEL`

## Docker workflow

Build:

`docker build -t querying-tools .`

Run:

`docker run -p 8501:8501 -e SCOPUS_API_KEY=your_key_here querying-tools`

## Pre-release checklist

- run `pytest`
- run `ruff check .`
- verify the app starts locally
- verify the example query works with valid credentials
