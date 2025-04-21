"""Dummy gphoto client for testing purposes."""

from typing import Any


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
