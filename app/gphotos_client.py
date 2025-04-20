"""Google Photos API client for fetching media items and their metadata."""

import datetime
import json
import os
from typing import Any, Optional

import requests
from google.auth.external_account_authorized_user import Credentials as auth_user_credentials
from google.oauth2.credentials import Credentials as oauth2_credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build_from_document

SCOPES: list[str] = ["https://www.googleapis.com/auth/photoslibrary.readonly"]
DISCOVERY_URL: str = "https://photoslibrary.googleapis.com/$discovery/rest?version=v1"
TOKEN_PATH = "token.json"


class GooglePhotosClient:
    """Client for interacting with Google Photos API."""

    service: Any

    def __init__(self, credentials_path: str) -> None:
        """Initialize the Google Photos client.

        :param credentials_path: Path to the Google API credentials JSON file.
        """
        self.service = self._authenticate(credentials_path)

    def _authenticate(self, credentials_path: str) -> Any:
        """Authenticate and create a service object for Google Photos API.

        :param credentials_path: Path to the Google API credentials JSON file.
        :return: Authenticated service object for Google Photos API.
        """
        user_credentials: auth_user_credentials | oauth2_credentials

        if os.path.exists(TOKEN_PATH):
            user_credentials = oauth2_credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

        else:
            flow: InstalledAppFlow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            user_credentials = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token_file:
            token_file.write(user_credentials.to_json())

        discovery_doc: str = requests.get(DISCOVERY_URL).text
        return build_from_document(json.loads(discovery_doc), credentials=user_credentials)

    def fetch_media_items_all(self, days_back: int) -> list[dict]:
        start_date: str = (datetime.datetime.utcnow() - datetime.timedelta(days=days_back)).isoformat("T") + "Z"
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
        media_items: list[Any] = []

        end: datetime.datetime = datetime.datetime.utcnow()
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

        request = self.service.mediaItems().search(body=request_body)
        while request is not None:
            response = request.execute()
            media_items.extend(response.get("mediaItems", []))
            request = self.service.mediaItems().search_next(request, response)

        return media_items

    def extract_metadata(self, media_item: dict) -> dict[str, Optional[str]]:
        """Extract metadata from a media item.

        :param media_item: A media item dictionary from Google Photos API.
        :return: A dictionary containing the extracted metadata.
        """
        return {
            "id": media_item.get("id"),
            "filename": media_item.get("filename"),
            "description": media_item.get("description"),
            "creationTime": media_item.get("mediaMetadata", {}).get("creationTime"),
        }
