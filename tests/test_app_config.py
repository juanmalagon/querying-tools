import json
import logging

import pytest

from app_config import AppSettings, configure_logging


def test_settings_defaults_use_base_dir(tmp_path):
    settings = AppSettings.from_env(environ={}, base_dir=tmp_path)

    assert settings.scopus_config_file == tmp_path / "scopus" / "config.json"
    assert settings.scopus_data_dir == tmp_path / "data"
    assert settings.save_to_csv is False


def test_resolve_scopus_api_key_from_env(tmp_path):
    settings = AppSettings.from_env(
        environ={"SCOPUS_API_KEY": "env-key"},
        base_dir=tmp_path,
    )

    assert settings.resolve_scopus_api_key() == "env-key"


def test_resolve_scopus_api_key_from_config_file(tmp_path):
    config_file = tmp_path / "scopus" / "config.json"
    config_file.parent.mkdir(parents=True)
    config_file.write_text(json.dumps({"apikey": "config-key"}), encoding="utf-8")

    settings = AppSettings.from_env(environ={}, base_dir=tmp_path)

    assert settings.resolve_scopus_api_key() == "config-key"


# --- has_scopus_credentials ---

def test_has_scopus_credentials_from_env(tmp_path):
    settings = AppSettings.from_env(
        environ={"SCOPUS_API_KEY": "env-key"},
        base_dir=tmp_path,
    )

    assert settings.has_scopus_credentials() is True


def test_has_scopus_credentials_from_file(tmp_path):
    config_file = tmp_path / "scopus" / "config.json"
    config_file.parent.mkdir(parents=True)
    config_file.write_text(json.dumps({"apikey": "file-key"}), encoding="utf-8")

    settings = AppSettings.from_env(environ={}, base_dir=tmp_path)

    assert settings.has_scopus_credentials() is True


def test_has_scopus_credentials_no_file_and_no_env(tmp_path):
    settings = AppSettings.from_env(environ={}, base_dir=tmp_path)

    assert settings.has_scopus_credentials() is False


def test_has_scopus_credentials_malformed_config_file(tmp_path):
    config_file = tmp_path / "scopus" / "config.json"
    config_file.parent.mkdir(parents=True)
    config_file.write_text("not valid json", encoding="utf-8")

    settings = AppSettings.from_env(environ={}, base_dir=tmp_path)

    assert settings.has_scopus_credentials() is False


# --- resolve_scopus_api_key error paths ---

def test_resolve_scopus_api_key_no_credentials_raises(tmp_path):
    settings = AppSettings.from_env(environ={}, base_dir=tmp_path)

    with pytest.raises(RuntimeError, match="Scopus credentials are not configured"):
        settings.resolve_scopus_api_key()


def test_resolve_scopus_api_key_malformed_file_raises(tmp_path):
    config_file = tmp_path / "scopus" / "config.json"
    config_file.parent.mkdir(parents=True)
    config_file.write_text("bad json", encoding="utf-8")

    settings = AppSettings.from_env(environ={}, base_dir=tmp_path)

    with pytest.raises(RuntimeError, match="Invalid JSON"):
        settings.resolve_scopus_api_key()


# --- configure_logging ---

def test_configure_logging_returns_logger():
    logger = configure_logging("test_logger")

    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_logger"


def test_configure_logging_sets_level():
    logger = configure_logging("test_logger", "DEBUG")

    assert logger.level == logging.DEBUG


def test_configure_logging_prevents_duplicate_handlers():
    logger1 = configure_logging("test_logger_unique")
    handler_count = len(logger1.handlers)

    logger2 = configure_logging("test_logger_unique")
    assert len(logger2.handlers) == handler_count
