# Project Documentation

## Overview

This repository provides a set of tools for querying bibliographic and other data sources, running experiments, and reusable helper modules. It includes scripts for unbiased requester experiments, utilities for query building and handling, example notebooks, and provider-specific helpers (Scopus, EBSCO, ERIC).

## Key repo layout

- `env_variables.py`: environment variable helpers and configuration.
- `requirements.txt`: Python dependencies used by the project.
- `unbiased_requester.py`: main script for performing unbiased requester experiments.
- `resources/`: helper resources and example query sets.
  - `resources/querying_tools.py` and `resources/scopus_functions.py` provide resource-level helpers and examples.
- `utils/`: core utilities used across scripts and notebooks.
  - `utils/query_tools.py`: query-building helpers.
  - `utils/handler.py`: high-level request/response handling.
  - `utils/scopus_functions.py`: Scopus-specific helpers.
- `experiments/` and `wip/`: Jupyter notebooks and experimental work. See notebooks for runnable examples.
- `scopus/`: contains instructions about placing Scopus config files (see `scopus/place_config_file_in_this_folder`).

## Installation

1. Create a Python 3.10+ virtual environment (or your preferred version):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Export or configure any required environment variables referenced in `env_variables.py` (API keys, paths).

## Quickstart

- Run the main requester script (example):

```bash
python unbiased_requester.py --help
python unbiased_requester.py --config path/to/config.yaml
```

- Open example notebooks:
  - [experiments/summarize_localized_data.ipynb](experiments/summarize_localized_data.ipynb)
  - [experiments/unbiased_requester_nb.ipynb](experiments/unbiased_requester_nb.ipynb)

These notebooks demonstrate typical workflows and show how to call the utilities in `utils/` and `resources/`.

## Configuration

- Place provider-specific config (e.g., Scopus credentials) in the `scopus/` folder as instructed by the placeholder `place_config_file_in_this_folder`.
- Review `env_variables.py` to see required environment keys and defaults used across the project.

## Usage patterns & examples

- Programmatic usage: import helpers from `utils/`:

```python
from utils.query_tools import build_query
from utils.handler import RequestHandler

q = build_query(...)
handler = RequestHandler()
res = handler.run(q)
```

- Notebook-driven exploration: use notebooks in `experiments/` which include runnable examples and small datasets.

## Development

- Follow the repository style (PEP8). Use black/flake8 as needed.
- Add tests alongside new modules where possible.
- When adding provider-specific logic, keep provider code under `utils/` or `resources/` to maintain separation from experiments.

## Contributing

- Fork the repo, create a feature branch, and open a pull request with a clear description.
- Update this documentation if your changes affect usage or configuration.

## Troubleshooting

- Missing package errors: ensure the virtual env is active and `pip install -r requirements.txt` succeeded.
- Scopus / provider auth: confirm credentials are placed in `scopus/` and environment vars referenced by `env_variables.py` are set.

## License

See the repository `LICENSE` file for licensing terms.