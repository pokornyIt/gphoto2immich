"""Immich Client for Python"""

from typing import Any, Optional

import requests


class ImmichClient:
    """Client for interacting with the Immich API."""

    base_url: str
    headers: dict[str, str]

    def __init__(self, base_url: str, api_key: str) -> None:
        """Initialize the Immich client.

        :param base_url: Base URL of the Immich server (e.g., "https://immich.example.com").
        :param api_key: API key for authentication with the Immich server.
        """
        self.base_url = base_url.rstrip("/")
        self.headers = {"x-api-key": api_key, "Content-Type": "application/json"}

    def find_asset_by_filename(self, filename: str) -> Optional[str]:
        """Find an asset by its filename.

        :param filename: The filename of the asset to search for.
        :return: The asset ID if found, otherwise None.
        """

        # This depends on how the Immich API supports querying – for now we fake it
        response: requests.Response = requests.get(f"{self.base_url}/assets", headers=self.headers)
        response.raise_for_status()
        assets: Any = response.json()

        for asset in assets:
            if asset.get("originalFileName") == filename:
                return str(asset["id"])

        return None

    def update_asset_description(self, asset_id: str, description: str) -> bool:
        """Update the description of an asset.

        :param asset_id: The ID of the asset to update.
        :param description: The new description for the asset.
        """
        response: requests.Response = requests.put(
            f"{self.base_url}/assets/{asset_id}", headers=self.headers, json={"description": description}
        )
        return response.status_code == 200
