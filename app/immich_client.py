"""Immich Client for Python"""

from logging import Logger
from typing import Any

import requests

from app.constants import HTTP_OK
from app.log import get_logger


class ImmichClient:
    """Client for interacting with the Immich API."""

    base_url: str
    headers: dict[str, str]
    logger: Logger

    def __init__(self, base_url: str, api_key: str) -> None:
        """Initialize the Immich client.

        :param base_url: Base URL of the Immich server (e.g., "https://immich.example.com").
        :param api_key: API key for authentication with the Immich server.
        """
        self.logger = get_logger(self.__class__.__name__)
        self.base_url = base_url.rstrip("/")
        self.headers = {"x-api-key": api_key, "Content-Type": "application/json"}

    def find_asset_by_filename(self, filename: str) -> str | None:
        """Find an asset by its filename.

        :param filename: The filename of the asset to search for.
        :return: The asset ID if found, otherwise None.
        """
        url: str = f"{self.base_url}/search/metadata"
        payload: dict[str, str] = {"originalFileName": filename}
        self.logger.debug("Searching for asset by filename: %s", filename)

        response: requests.Response = requests.post(url, headers=self.headers, json=payload)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self.logger.error("Immich search failed: %s", e)
            return None

        data: Any = response.json()
        assets: Any = data.get("assets", {}).get("items", [])
        if assets:
            asset_id: str = assets[0]["id"]
            self.logger.debug("Found asset ID: %s", asset_id)
            return asset_id

        self.logger.debug("No matching asset found for filename: %s", filename)
        return None

    def update_asset_description(self, asset_id: str, description: str) -> bool:
        """Update the description of an asset.

        :param asset_id: The ID of the asset to update.
        :param description: The new description for the asset.
        """
        url: str = f"{self.base_url}/asset/{asset_id}"
        self.logger.debug("Updating description for asset %s", asset_id)
        response: requests.Response = requests.put(url, headers=self.headers, json={"description": description})
        if response.status_code == HTTP_OK:
            self.logger.debug("Successfully updated asset %s", asset_id)
            return True

        self.logger.error("Failed to update asset %s: HTTP %d", asset_id, response.status_code)
        return False

    def get_asset_description(self, asset_id: str) -> str:
        """Get the description of an asset.

        :param asset_id: The ID of the asset to retrieve the description for.
        :return: The description of the asset, or an empty string if not found.
        """
        url: str = f"{self.base_url}/assets/{asset_id}"
        self.logger.debug("Fetching asset description for ID: %s", asset_id)

        response: requests.Response = requests.get(url, headers=self.headers)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            self.logger.error("Failed to retrieve asset description: %s", e)
            return ""

        description: str = response.json().get("exifInfo", {}).get("description") or ""
        self.logger.debug("Retrieved description for asset %s - %s", asset_id, description)
        return description
