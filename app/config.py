"""Configuration module for the application."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()  # Automatically loads values from .env file


@dataclass
class Config:
    google_credentials_path: str
    immich_base_url: str
    immich_api_key: str
    days_back: int = 15
    dry_run: bool = False
    sync_strategy: str = "overwrite"

    @staticmethod
    def load() -> "Config":
        return Config(
            google_credentials_path=os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json"),
            immich_base_url=os.getenv("IMMICH_BASE_URL") or "",
            immich_api_key=os.getenv("IMMICH_API_KEY") or "",
            days_back=int(os.getenv("DAYS_BACK", "15")),
            dry_run=os.getenv("DRY_RUN", "false").lower() in ("1", "true", "yes"),
            sync_strategy=os.getenv("SYNC_STRATEGY", "overwrite"),
        )
