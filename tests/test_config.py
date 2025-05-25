"""Test configuration loading and validation."""

from pytest import MonkeyPatch

from app.config import Config

TEST_DAY_BACK: int = 7

def test_load_config(monkeypatch: MonkeyPatch) -> None:
    """Test loading configuration from environment variables.

    :param monkeypatch: The pytest fixture to modify environment variables.
    """
    monkeypatch.setenv("GOOGLE_CREDENTIALS_PATH", "test_credentials.json")
    monkeypatch.setenv("IMMICH_BASE_URL", "http://localhost:2283/api")
    monkeypatch.setenv("IMMICH_API_KEY", "dummy-api-key")
    monkeypatch.setenv("DAYS_BACK", f"{TEST_DAY_BACK}")

    config: Config = Config.load()

    assert config.google_credentials_path == "test_credentials.json"
    assert config.immich_base_url == "http://localhost:2283/api"
    assert config.immich_api_key == "dummy-api-key"
    assert config.days_back == TEST_DAY_BACK
