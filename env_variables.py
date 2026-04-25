"""Backward-compatible environment defaults for local research workflows.

Deployment should use real environment variables instead:

- ``SCOPUS_API_KEY``
- ``SCOPUS_CONFIG_FILE``
- ``SCOPUS_DATA_DIR``
- ``SAVE_TO_CSV``
- ``LOG_LEVEL``
"""

from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent

os.environ.setdefault("PROJECT_DIR", str(BASE_DIR))
os.environ.setdefault("SCOPUS_CONFIG_FILE", str(BASE_DIR / "scopus" / "config.json"))
os.environ.setdefault("SCOPUS_DATA_DIR", str(BASE_DIR / "data"))
os.environ.setdefault("SAVE_TO_CSV", "1")
os.environ.setdefault("LOG_LEVEL", "INFO")
