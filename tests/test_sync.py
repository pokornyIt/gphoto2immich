"""test_sync.py"""

from typing import Any, Literal

from pytest import MonkeyPatch

from app.config import Config
from app.sync import SyncService


class DummyGooglePhotosClient:
    """Dummy Google Photos client for testing."""

    def __init__(self, credentials_path: str) -> None:
        """Initialize the dummy client.

        :param credentials_path: Path to the Google API credentials JSON file.
        """
        pass

    def fetch_media_items(self, days_back: int) -> list[dict[str, Any]]:
        """Fetch media items from Google Photos.

        :param days_back: Number of days back to fetch items.
        :return: List of media items.
        """
        return [
            {
                "id": "1",
                "filename": "test1.jpg",
                "description": "Test photo",
                "mediaMetadata": {"creationTime": "2024-04-15T10:00:00Z"},
            },
            {
                "id": "2",
                "filename": "test2.jpg",
                "description": None,  # No description = should be skipped
                "mediaMetadata": {"creationTime": "2024-04-14T10:00:00Z"},
            },
        ]

    def extract_metadata(self, item: dict[str, Any]) -> dict[str, Any]:
        """Extract metadata from a media item.

        :param item: A media item dictionary from Google Photos API.
        :return: A dictionary containing the extracted metadata.
        """
        return {
            "id": item["id"],
            "filename": item["filename"],
            "description": item["description"],
            "creationTime": item["mediaMetadata"]["creationTime"],
        }


class DummyImmichClient:
    """Dummy Immich client for testing."""

    def __init__(self, base_url: str, api_key: str) -> None:
        """Initialize the dummy client.

        :param base_url: Base URL of the Immich server.
        :param api_key: API key for authentication with the Immich server.
        """
        self.updated: list[Any] = []

    def find_asset_by_filename(self, filename: str) -> str | None:
        """Find an asset by filename.

        :param filename: The filename of the asset to search for.
        :return: The asset ID if found, otherwise None.
        """
        return f"asset-{filename}" if "test1" in filename else None

    def update_asset_description(self, asset_id: str, description: str) -> Literal[True]:
        """Update the description of an asset.

        :param asset_id: The ID of the asset to update.
        :param description: The new description for the asset.
        :return: True if the update was successful, otherwise False.
        """
        self.updated.append((asset_id, description))
        return True


def test_sync_run(monkeypatch: MonkeyPatch, capsys: Any) -> None:
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
    sync.run()

    captured = capsys.readouterr()
    assert "[SYNC] Found 2 items." in captured.out
    assert "[SYNC] Updated: test1.jpg" in captured.out
    assert "[SYNC] Not found in Immich: test2.jpg" not in captured.out
    assert "[SYNC] Updated 1 items." in captured.out
