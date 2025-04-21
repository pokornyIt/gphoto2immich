"""Sync Service"""

from logging import Logger
from typing import Any

from app.config import Config
from app.gphotos_client import GooglePhotosClient
from app.immich_client import ImmichClient
from app.log import get_logger


class SyncService:
    """Service for syncing Google Photos items to Immich."""

    config: Config
    gphotos: GooglePhotosClient
    immich: ImmichClient
    logger: Logger

    def __init__(self, config: Config) -> None:
        """Initialize the SyncService.

        :param config: Configuration object containing settings for the sync process.
        """
        self.logger = get_logger("sync")
        self.config: Config = config
        self.gphotos = GooglePhotosClient(config.google_credentials_path)
        self.immich = ImmichClient(config.immich_base_url, config.immich_api_key)
        self.logger.debug(f"Initialized with config: {config}")

    def run(self) -> None:
        self.logger.info("Fetching Google Photos items from last %d days...", self.config.days_back)
        items: list[dict[Any, Any]] = self.gphotos.fetch_media_items(self.config.days_back)
        self.logger.info("Found %d items.", len(items))

        updated = 0
        for item in items:
            metadata: dict[str, str | None] = self.gphotos.extract_metadata(item)
            filename: str = metadata["filename"] or ""
            description: str | None = metadata["description"]

            if not description:
                self.logger.debug("Skipping %s (no description)", filename)
                continue

            asset_id: str | None = self.immich.find_asset_by_filename(filename)
            if asset_id:
                if self.config.sync_strategy == "skip_if_present":
                    existing_description = self.immich.get_asset_description(asset_id)
                    if existing_description:
                        self.logger.info("Skipping %s - already has description in Immich", filename)
                        continue

                if self.config.dry_run:
                    self.logger.info('[DRY-RUN] Would update: %s → "%s"', filename, description)
                    updated += 1
                else:
                    success: bool = self.immich.update_asset_description(asset_id, description)
                    if success:
                        self.logger.info("Updated: %s", filename)
                        updated += 1
                    else:
                        self.logger.error("Failed to update: %s", filename)
            else:
                self.logger.warning("Not found in Immich: %s", filename)

        self.logger.info("Updated %d items.", updated)
