"""test_sync.py"""

from typing import Any

from pytest import LogCaptureFixture, MonkeyPatch

from app.config import Config
from app.sync import SyncService
from tests.mocks.dummy_gphoto_client import DummyGooglePhotosClient
from tests.mocks.dummy_immich_client import DummyImmichClient, DummyImmichClientWithDescription


def test_sync_run(monkeypatch: MonkeyPatch, caplog: Any) -> None:
    """Test the SyncService run method.

    :param monkeypatch: The pytest monkeypatch fixture to patch classes.
    :param capsys: The pytest capsys fixture to capture output.
    """
    config = Config(
        google_credentials_path="dummy", immich_base_url="http://dummy", immich_api_key="dummy", days_back=15
    )

    # Patch real clients with dummy ones
    monkeypatch.setattr("app.sync.GooglePhotosClient", DummyGooglePhotosClient)
    monkeypatch.setattr("app.sync.ImmichClient", DummyImmichClient)

    sync = SyncService(config)
    with caplog.at_level("INFO"):
        sync.run()

    assert "Found 2 items." in caplog.text
    assert "Updated: test1.jpg" in caplog.text
    assert "Not found in Immich: test2.jpg" not in caplog.text
    assert "Updated 1 items." in caplog.text


def test_sync_dry_run(monkeypatch: MonkeyPatch, caplog: LogCaptureFixture) -> None:
    """Test the SyncService run method in dry run mode.

    :param monkeypatch: The pytest monkeypatch fixture to patch classes.
    :param caplog: The pytest caplog fixture to capture log output.
    """
    config = Config(
        google_credentials_path="dummy",
        immich_base_url="http://dummy",
        immich_api_key="dummy",
        days_back=15,
        dry_run=True,
        sync_strategy="overwrite",
    )

    monkeypatch.setattr("app.sync.GooglePhotosClient", DummyGooglePhotosClient)
    monkeypatch.setattr("app.sync.ImmichClient", DummyImmichClient)

    sync = SyncService(config)
    with caplog.at_level("INFO"):
        sync.run()

    assert "[DRY-RUN] Would update: test1.jpg" in caplog.text


def test_sync_overwrite(monkeypatch: MonkeyPatch, caplog: LogCaptureFixture) -> None:
    """Test the SyncService run method with overwrite strategy.

    :param monkeypatch: The pytest monkeypatch fixture to patch classes.
    :param caplog: The pytest caplog fixture to capture log output.
    """
    config = Config(
        google_credentials_path="dummy",
        immich_base_url="http://dummy",
        immich_api_key="dummy",
        days_back=15,
        dry_run=False,
        sync_strategy="overwrite",
    )

    monkeypatch.setattr("app.sync.GooglePhotosClient", DummyGooglePhotosClient)
    monkeypatch.setattr("app.sync.ImmichClient", DummyImmichClient)

    sync = SyncService(config)
    with caplog.at_level("INFO"):
        sync.run()

    assert "Updated: test1.jpg" in caplog.text


def test_sync_skip_if_present(monkeypatch: MonkeyPatch, caplog: LogCaptureFixture) -> None:
    """Test the SyncService run method with skip_if_present strategy.

    :param monkeypatch: The pytest monkeypatch fixture to patch classes.
    :param caplog: The pytest caplog fixture to capture log output.
    """
    config = Config(
        google_credentials_path="dummy",
        immich_base_url="http://dummy",
        immich_api_key="dummy",
        days_back=15,
        dry_run=False,
        sync_strategy="skip_if_present",
    )

    monkeypatch.setattr("app.sync.GooglePhotosClient", DummyGooglePhotosClient)
    monkeypatch.setattr("app.sync.ImmichClient", DummyImmichClientWithDescription)

    sync = SyncService(config)
    with caplog.at_level("INFO"):
        sync.run()

    assert "Skipping test1.jpg - already has description in Immich" in caplog.text
