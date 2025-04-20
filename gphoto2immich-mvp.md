# Project: gphoto2immich

## Project Goal
Synchronize metadata (e.g., descriptions, titles, albums) from Google Photos to the Immich system. The application will:
- Run as a Docker container
- Be written in Python
- Process changes from the last 15 days (or a configurable value)
- Be extendable to include album creation and assignment of photos to albums

## Project Structure

```
gphoto2immich/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── gphotos_client.py
│   ├── immich_client.py
│   ├── sync.py
│   └── utils.py
│
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_gphotos_client.py
│   ├── test_immich_client.py
│   └── test_sync.py
│
├── Dockerfile
├── requirements.txt
├── .env.example
├── main.py
├── compose.yaml
├── README.md
└── pyproject.toml (optional)
```

## MVP Functionality

### 1. Authentication and Configuration
- [x] Load configuration from `.env` or another source
- [x] Google Photos: connect using OAuth 2.0
- [x] Immich API: authenticate using a token or password

### 2. Fetch Photos from Google Photos
- [x] Fetch media items from the last 15 days
- [x] Extract metadata: title, description, creation date

### 3. Match and Update Immich Items
- [x] Identify the corresponding photo in Immich (e.g., by name or checksum)
- [x] Update description/title using Immich API

### 4. Logging and Output
- [x] Summary of processed and updated items

### 5. Testing with `pytest`
- [x] Unit tests for each component
- [x] API mocking for Google and Immich calls
- [ ] Optional CI integration

## Future Extensions
- Map and synchronize albums
- Dry-run mode
- CLI arguments (e.g., `--days-back`)
- Webhook or scheduled cron execution
- Export summary of changes

---

## Configuration: How to obtain `.env` values

### `GOOGLE_CREDENTIALS_PATH`
Path to your Google API credentials file (OAuth 2.0 client ID). To generate:

1. Go to: https://console.cloud.google.com/
2. Create/select a project
3. Enable **Google Photos Library API**
4. Go to **Credentials** > **Create Credentials** > **OAuth client ID**
5. Choose **Desktop App** as application type
6. Download the JSON and save it as `credentials.json` in the project root

In your `.env`:
```
GOOGLE_CREDENTIALS_PATH=credentials.json
```

### `IMMICH_BASE_URL`
Base URL of your Immich instance, e.g.:
```
IMMICH_BASE_URL=http://immich.example.com/api
```

### `IMMICH_API_KEY`
Immich API key – generate it in your Immich user settings (usually in the web UI).
```
IMMICH_API_KEY=your_immich_api_key_here
```

### `DAYS_BACK`
How many days back the sync should look for new or updated photos (default: 15):
```
DAYS_BACK=15
```

---

All values can be set in a `.env` file, which is automatically loaded at runtime.
An example file is provided as `.env.example`.

