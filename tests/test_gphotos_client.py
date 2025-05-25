"""Test Google Photos Client functionality."""

from typing import Any

from app.gphotos_client import GooglePhotosClient
from app.log import get_logger


def test_extract_metadata() -> None:
    """Test extracting metadata from a Google Photos media item."""
    media_item: dict[str, Any] = {
        "id": "abc123",
        "filename": "photo.jpg",
        "description": "Sunset at the beach",
        "mediaMetadata": {"creationTime": "2024-04-10T12:00:00Z"},
    }

    client: GooglePhotosClient = GooglePhotosClient.__new__(GooglePhotosClient)  # Avoid __init__ (no auth)
    client.logger = get_logger("TestClient")  # Use a test logger

    metadata: dict[str, str | None] = client.extract_metadata(media_item)

    assert metadata["id"] == "abc123"
    assert metadata["filename"] == "photo.jpg"
    assert metadata["description"] == "Sunset at the beach"
    assert metadata["creationTime"] == "2024-04-10T12:00:00Z"
