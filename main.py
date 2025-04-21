#!/usr/bin/env python3
"""The main entry point for the application."""

from logging import Logger

from app.config import Config
from app.log import get_logger
from app.sync import SyncService


def main() -> None:
    logger: Logger = get_logger("main")
    try:
        config: Config = Config.load()
        logger.info("Configuration loaded successfully.")
        print("Config loaded:")
        print(f"- Google credentials: {config.google_credentials_path}")
        print(f"- Immich URL: {config.immich_base_url}")
        print(f"- Days back: {config.days_back}")
        print(f"- Sync strategy: {config.sync_strategy}")
        print(f"- Dry run: {config.dry_run}")
        print(f"- Log level: {logger.level}")
        sync = SyncService(config)
        sync.run()
        logger.info("Sync process completed.")
    except Exception as e:
        logger.exception("Unhandled exception occurred: %s", e)


if __name__ == "__main__":
    main()
