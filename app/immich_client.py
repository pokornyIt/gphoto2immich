"""Immich Client for Python"""

from typing import Any

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

    def find_asset_by_filename(self, filename: str) -> str | None:
        """Find an asset by its filename.

        :param filename: The filename of the asset to search for.
        :return: The asset ID if found, otherwise None.
        """
        url: str = f"{self.base_url}/search/metadata"
        payload: dict[str, str] = {"originalFileName": filename}

        response: requests.Response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()

        data: Any = response.json()
        assets: Any = data.get("assets", {}).get("items", [])
        if assets:
            print(f"[IMMICH] Found asset ID: {assets[0]['id']} for filename: {filename}")
            return str(assets[0]["id"])
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
