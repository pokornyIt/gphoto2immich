"""Sync Service"""

from typing import Any

from app.config import Config
from app.gphotos_client import GooglePhotosClient
from app.immich_client import ImmichClient


class SyncService:
    """Service for syncing Google Photos items to Immich."""

    config: Config
    gphotos: GooglePhotosClient
    immich: ImmichClient

    def __init__(self, config: Config) -> None:
        self.config: Config = config
        self.gphotos = GooglePhotosClient(config.google_credentials_path)
        self.immich = ImmichClient(config.immich_base_url, config.immich_api_key)

    def run(self) -> None:
        print(f"[SYNC] Fetching Google Photos items from last {self.config.days_back} days...")
        items: list[dict[Any, Any]] = self.gphotos.fetch_media_items(self.config.days_back)
        print(f"[SYNC] Found {len(items)} items.")

        updated = 0
        for item in items:
            metadata: dict[str, str | None] = self.gphotos.extract_metadata(item)
            filename: str = metadata["filename"] or ""
            description: str | None = metadata["description"]

            if not description:
                continue  # Skip items without description

            asset_id: str | None = self.immich.find_asset_by_filename(filename)
            if asset_id:
                if self.config.dry_run:
                    print(f'[DRY-RUN] Would update: {filename} → "{description}"')
                    updated += 1
                else:
                    success: bool = self.immich.update_asset_description(asset_id, description)
                    if success:
                        print(f"[SYNC] Updated: {filename}")
                        updated += 1
                    else:
                        print(f"[SYNC] Failed to update: {filename}")
            else:
                print(f"[SYNC] Not found in Immich: {filename}")

        print(f"[SYNC] Updated {updated} items.")
