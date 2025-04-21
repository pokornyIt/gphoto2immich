"""Dummy Immich Client for testing purposes."""

from typing import Any, Optional


class DummyImmichClient:
    """Dummy Immich client for testing."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the dummy client."""
        self.updated: list[Any] = []

    def find_asset_by_filename(self, filename: str) -> Optional[str]:
        """Find an asset by filename.

        :param filename: The filename of the asset to search for.
        :return: The asset ID if found, otherwise None.
        """
        if filename == "test1.jpg":
            return "asset123"
        return None

    def update_asset_description(self, asset_id: str, description: str) -> bool:
        """Update the description of an asset.

        :param asset_id: The ID of the asset to update.
        :param description: The new description for the asset.
        :return: True if the update was successful, otherwise False.
        """
        self.updated.append((asset_id, description))
        return True

    def get_asset_description(self, asset_id: str) -> str:
        """Get the description of an asset.

        :param asset_id: The ID of the asset to retrieve the description for.
        :return: The description of the asset, or an empty string if not found.
        """
        return ""


class DummyImmichClientWithDescription(DummyImmichClient):
    """Dummy Immich client that returns a description."""

    def get_asset_description(self, asset_id: str) -> str:
        """Get the description of an asset.

        :param asset_id: The ID of the asset to retrieve the description for.
        :return: The description of the asset, or an empty string if not found.
        """
        return "Existing description"
