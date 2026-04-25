import json

from app_config import AppSettings


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
