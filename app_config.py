from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
from typing import Mapping


_TRUTHY_VALUES = {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class AppSettings:
    base_dir: Path
    scopus_api_key: str | None
    scopus_config_file: Path
    scopus_data_dir: Path
    save_to_csv: bool
    log_level: str

    @classmethod
    def from_env(
        cls,
        environ: Mapping[str, str] | None = None,
        base_dir: Path | None = None,
    ) -> "AppSettings":
        env = os.environ if environ is None else environ
        resolved_base_dir = (base_dir or Path(__file__).resolve().parent).resolve()
        scopus_config_file = Path(
            env.get("SCOPUS_CONFIG_FILE", resolved_base_dir / "scopus" / "config.json")
        )
        scopus_data_dir = Path(
            env.get("SCOPUS_DATA_DIR", resolved_base_dir / "data")
        )

        return cls(
            base_dir=resolved_base_dir,
            scopus_api_key=env.get("SCOPUS_API_KEY"),
            scopus_config_file=scopus_config_file,
            scopus_data_dir=scopus_data_dir,
            save_to_csv=env.get("SAVE_TO_CSV", "0").strip().lower() in _TRUTHY_VALUES,
            log_level=env.get("LOG_LEVEL", "INFO").upper(),
        )

    def has_scopus_credentials(self) -> bool:
        if self.scopus_api_key:
            return True
        if not self.scopus_config_file.exists():
            return False
        try:
            payload = json.loads(self.scopus_config_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return False
        return bool(payload.get("apikey"))

    def resolve_scopus_api_key(self) -> str:
        if self.scopus_api_key:
            return self.scopus_api_key
        if self.scopus_config_file.exists():
            try:
                payload = json.loads(self.scopus_config_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                raise RuntimeError(
                    f"Invalid JSON in Scopus config file: {self.scopus_config_file}"
                ) from exc
            api_key = payload.get("apikey")
            if api_key:
                return api_key
        raise RuntimeError(
            "Scopus credentials are not configured. Set SCOPUS_API_KEY or provide "
            f"a config file at {self.scopus_config_file}."
        )


settings = AppSettings.from_env()
