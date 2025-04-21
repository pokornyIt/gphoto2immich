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
    requests_mock.post(
        "http://immich.local/api/search/metadata",
        json={
            "albums": {"total": 0, "count": 0, "items": [], "facets": []},
            "assets": {
                "total": 0,
                "count": 0,
                "nextPage": None,
                "items": [
                    {"id": "123", "originalFileName": "photo.jpg"},
                    {"id": "456", "originalFileName": "video.mp4"},
                ],
            },
        },
    )

    result: str | None = client.find_asset_by_filename("photo.jpg")
    assert result == "123"


def test_find_asset_by_filename_not_found(requests_mock: requests_mock.Mocker, client: ImmichClient) -> None:
    """Test finding an asset by filename when not found.

    :param requests_mock: The requests_mock fixture to mock HTTP requests.
    :param client: The ImmichClient instance to test.
    """
    requests_mock.post(
        "http://immich.local/api/search/metadata",
        json={
            "albums": {"total": 0, "count": 0, "items": [], "facets": []},
            "assets": {"total": 0, "count": 0, "items": [], "facets": [], "nextPage": None},
        },
    )

    result: str | None = client.find_asset_by_filename("photo.jpg")
    assert result is None


def test_update_asset_description_success(requests_mock: requests_mock.Mocker, client: ImmichClient) -> None:
    """Test updating an asset description successfully.

    :param requests_mock: The requests_mock fixture to mock HTTP requests.
    :param client: The ImmichClient instance to test.
    """
    requests_mock.put("http://immich.local/api/asset/123", status_code=200)

    result: bool = client.update_asset_description("123", "A lovely view")
    assert result is True


def test_update_asset_description_failure(requests_mock: requests_mock.Mocker, client: ImmichClient) -> None:
    """Test updating an asset description when the request fails.

    :param requests_mock: The requests_mock fixture to mock HTTP requests.
    :param client: The ImmichClient instance to test.
    """
    requests_mock.put("http://immich.local/api/asset/123", status_code=400)

    result: bool = client.update_asset_description("123", "A lovely view")
    assert result is False


def test_get_asset_description_success(requests_mock: requests_mock.Mocker, client: ImmichClient) -> None:
    """Test getting an asset description successfully.

    :param requests_mock: The requests_mock fixture to mock HTTP requests.
    :param client: The ImmichClient instance to test.
    """
    asset_id: str = "abc123"
    requests_mock.get(
        f"http://immich.local/api/assets/{asset_id}", json={"exifInfo": {"description": "A mountain view"}}
    )

    desc: str = client.get_asset_description(asset_id)
    assert desc == "A mountain view"


def test_get_asset_description_empty(requests_mock: requests_mock.Mocker, client: ImmichClient) -> None:
    """Test getting an asset description when the response is empty.

    :param requests_mock: The requests_mock fixture to mock HTTP requests.
    :param client: The ImmichClient instance to test.
    """
    asset_id: str = "abc123"
    requests_mock.get(
        f"http://immich.local/api/assets/{asset_id}",
        json={},  # no description
    )

    desc: str = client.get_asset_description(asset_id)
    assert desc == ""


def test_get_asset_description_error(requests_mock: requests_mock.Mocker, client: ImmichClient) -> None:
    """Test getting an asset description when the request fails.

    :param requests_mock: The requests_mock fixture to mock HTTP requests.
    :param client: The ImmichClient instance to test.
    """
    asset_id: str = "abc123"
    requests_mock.get(f"http://immich.local/api/assets/{asset_id}", status_code=404)

    desc: str = client.get_asset_description(asset_id)
    assert desc == ""
