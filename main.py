#!/usr/bin/env python3
"""The main entry point for the application."""

from app.config import Config
from app.sync import SyncService


def main() -> None:
    config: Config = Config.load()
    print("Config loaded:")
    print(f"- Google credentials: {config.google_credentials_path}")
    print(f"- Immich URL: {config.immich_base_url}")
    print(f"- Days back: {config.days_back}")
    sync = SyncService(config)
    sync.run()


if __name__ == "__main__":
    main()
