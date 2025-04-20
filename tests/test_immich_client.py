"""Test cases for the ImmichClient class."""

import pytest
import requests_mock

from app.immich_client import ImmichClient


@pytest.fixture
def client() -> ImmichClient:
    return ImmichClient(base_url="http://immich.local/api", api_key="test-key")


def test_find_asset_by_filename_found(requests_mock: requests_mock.Mocker, client: ImmichClient) -> None:
    """Test finding an asset by filename.

    :param requests_mock: The requests_mock fixture to mock HTTP requests.
    :param client: The ImmichClient instance to test.
    """
    requests_mock.get(
        "http://immich.local/api/assets",
        json=[
            {"id": "123", "originalFileName": "photo.jpg"},
            {"id": "456", "originalFileName": "video.mp4"},
        ],
    )

    result: str | None = client.find_asset_by_filename("photo.jpg")
    assert result == "123"


def test_find_asset_by_filename_not_found(requests_mock: requests_mock.Mocker, client: ImmichClient) -> None:
    """Test finding an asset by filename when not found.

    :param requests_mock: The requests_mock fixture to mock HTTP requests.
    :param client: The ImmichClient instance to test.
    """
    requests_mock.get(
        "http://immich.local/api/assets",
        json=[
            {"id": "456", "originalFileName": "video.mp4"},
        ],
    )

    result: str | None = client.find_asset_by_filename("photo.jpg")
    assert result is None


def test_update_asset_description_success(requests_mock: requests_mock.Mocker, client: ImmichClient) -> None:
    """Test updating an asset description successfully.

    :param requests_mock: The requests_mock fixture to mock HTTP requests.
    :param client: The ImmichClient instance to test.
    """
    requests_mock.put("http://immich.local/api/assets/123", status_code=200)

    result: bool = client.update_asset_description("123", "A lovely view")
    assert result is True


def test_update_asset_description_failure(requests_mock: requests_mock.Mocker, client: ImmichClient) -> None:
    """Test updating an asset description when the request fails.

    :param requests_mock: The requests_mock fixture to mock HTTP requests.
    :param client: The ImmichClient instance to test.
    """
    requests_mock.put("http://immich.local/api/assets/123", status_code=400)

    result: bool = client.update_asset_description("123", "A lovely view")
    assert result is False
