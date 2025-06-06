"""Google Photos API client for fetching media items and their metadata."""

import datetime
import json
import os
from logging import Logger
from typing import Any

import requests
from google.auth.exceptions import RefreshError
from google.auth.external_account_authorized_user import Credentials as AuthUserCredentials
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials as OAuth2Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build_from_document

from app.log import get_logger

SCOPES: list[str] = ["https://www.googleapis.com/auth/photoslibrary.readonly"]
DISCOVERY_URL: str = "https://photoslibrary.googleapis.com/$discovery/rest?version=v1"
TOKEN_PATH = "token.json"


class GooglePhotosClient:
    """Client for interacting with Google Photos API."""

    service: Any
    logger: Logger

    def __init__(self, credentials_path: str) -> None:
        """Initialize the Google Photos client.

        :param credentials_path: Path to the Google API credentials JSON file.
        """
        self.logger = get_logger(self.__class__.__name__)
        self.service = self._authenticate(credentials_path)

    def _test_if_token_expired(self) -> bool:
        """Check if the token is expired.

        :return: True if the token is expired, False otherwise.
        """
        if not os.path.exists(TOKEN_PATH):
            self.logger.warning("Token file does not exist: %s", TOKEN_PATH)
            return True

        with open(TOKEN_PATH) as token_file:
            self.logger.debug("Loading token from %s", TOKEN_PATH)
            token_data: dict[str, Any] = json.loads(token_file.read())
            if "expiry" not in token_data:
                self.logger.debug("Token file does not contain a refresh token.")
                return True
            self.logger.debug("Checking if token is expired...")
            # Load the token and check if it is expired
            refresh_date: datetime.datetime = datetime.datetime.fromisoformat(token_data.get("expiry", ""))
            if refresh_date < datetime.datetime.now(datetime.UTC):
                self.logger.info("Token is expired, needs refresh.")
                return True

        return False

    def _authenticate(self, credentials_path: str) -> Any:
        """Authenticate and create a service object for Google Photos API.

        :param credentials_path: Path to the Google API credentials JSON file.
        :return: Authenticated service object for Google Photos API.
        """
        user_credentials: AuthUserCredentials | OAuth2Credentials
        user_credentials_initialized: bool = False

        if os.path.exists(TOKEN_PATH):
            if self._test_if_token_expired():
                self.logger.info("Token is expired, refreshing...")
                try:
                    os.unlink(TOKEN_PATH)
                except OSError as e:
                    self.logger.error("Failed to delete expired token file %s: %s", TOKEN_PATH, e)
                user_credentials_initialized = False
            else:
                user_credentials_initialized = True
                self.logger.debug("Loading existing token from %s", TOKEN_PATH)
                user_credentials = OAuth2Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

        if not user_credentials_initialized or not user_credentials or not user_credentials.valid:
            if (
                user_credentials_initialized
                and user_credentials
                and user_credentials.expired
                and user_credentials.refresh_token
            ):
                self.logger.info("Refreshing expired token...")

                try:
                    user_credentials.refresh(Request())
                except RefreshError as e:
                    self.logger.error("Token refresh failed: %s", e)
                    os.remove(TOKEN_PATH)
                    raise RuntimeError("Token expired and could not be refreshed. Please re-authenticate.")
            else:
                self.logger.info("No valid token found, starting OAuth flow...")
                flow: InstalledAppFlow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                user_credentials = flow.run_local_server(port=0)
            # Save the new token to a file
            self.logger.debug("Saving new token to %s", TOKEN_PATH)
            with open(TOKEN_PATH, "w") as token_file:
                token_file.write(user_credentials.to_json())
                self.logger.info("Saved new token to %s", TOKEN_PATH)

        discovery_doc: str = requests.get(DISCOVERY_URL).text
        return build_from_document(json.loads(discovery_doc), credentials=user_credentials)

    def fetch_media_items_all(self, days_back: int) -> list[dict]:
        """Fetch all media items from Google Photos API.

        :param days_back: Number of days back to fetch media items.
        :return: List of media items from Google Photos API.
        """
        start_date: str = (
            f"{(datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=days_back)).isoformat('T')}Z"
        )
        media_items: list[Any] = []

        request = self.service.mediaItems().list(pageSize=100)
        while request is not None:
            response = request.execute()
            for item in response.get("mediaItems", []):
                metadata = item.get("mediaMetadata", {})
                creation_time = metadata.get("creationTime")
                if creation_time and creation_time >= start_date:
                    media_items.append(item)

            request = self.service.mediaItems().list_next(request, response)

        return media_items

    def fetch_media_items(self, days_back: int) -> list[dict]:
        """Fetch media items from Google Photos API within a specified date range.

        :param days_back: Number of days back to fetch media items.
        :return: List of media items from Google Photos API.
        """
        media_items: list[Any] = []

        end: datetime.datetime = datetime.datetime.now(datetime.UTC)
        start: datetime.datetime = end - datetime.timedelta(days=days_back)

        request_body: dict[str, Any] = {
            "pageSize": 100,
            "filters": {
                "dateFilter": {
                    "ranges": [
                        {
                            "startDate": {"year": start.year, "month": start.month, "day": start.day},
                            "endDate": {"year": end.year, "month": end.month, "day": end.day},
                        }
                    ]
                }
            },
        }

        self.logger.debug("Requesting media items from %s to %s", start.date(), end.date())

        request = self.service.mediaItems().search(body=request_body)
        while request is not None:
            response = request.execute()
            collect_items = response.get("mediaItems", [])
            self.logger.debug("Fetched %d items in this page", len(collect_items))
            media_items.extend(collect_items)
            request = self.service.mediaItems().search_next(request, response)

        self.logger.info("Total media items fetched: %d", len(media_items))
        return media_items

    def extract_metadata(self, media_item: dict) -> dict[str, str | None]:
        """Extract metadata from a media item.

        :param media_item: A media item dictionary from Google Photos API.
        :return: A dictionary containing the extracted metadata.
        """
        metadata: dict[str, Any] = {
            "id": media_item.get("id"),
            "filename": media_item.get("filename"),
            "description": media_item.get("description"),
            "creationTime": media_item.get("mediaMetadata", {}).get("creationTime"),
        }
        self.logger.debug("Extracted metadata: %s", metadata)
        return metadata
