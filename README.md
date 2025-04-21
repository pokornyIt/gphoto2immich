# gphoto2immich

Synchronize photo descriptions from Google Photos to [Immich](https://github.com/immich-app/immich).

## 🔧 Features

- Pull metadata (filename, description, creation time) from Google Photos API
- Find matching assets in Immich by filename
- Update asset descriptions in Immich if found
- Dry-run mode for safe testing
- Docker + Compose setup
- Pre-commit checks (mypy, ruff, pytest)
- Logging with level control (DEBUG, INFO, WARNING, ERROR)
- Synchronization strategy control (overwrite / skip_if_present)

## 📦 Installation

```bash
git clone https://github.com/pokornyIt/gphoto2immich.git
cd gphoto2immich
cp .env.example .env
# Fill in .env with your Google credentials and Immich info
```

Or use Docker:

```bash
docker compose run --rm sync
```

## 🔑 How to obtain Google API credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or reuse existing)
3. Enable the **Google Photos Library API**
4. Go to "APIs & Services > Credentials"
5. Click **Create Credentials > OAuth client ID**
6. Choose **Desktop app** as application type
7. Download the resulting `client_secret_XXXX.json`
8. Save it as `google-credentials.json` (or update path in `.env`)

> On first run, a browser window will open to authenticate your Google account and generate a `token.json` file.

## 🛠️ Configuration

Edit `.env` file:

```dotenv
GOOGLE_CREDENTIALS_PATH=./google-credentials.json
IMMICH_BASE_URL=https://immich.example.com/api
IMMICH_API_KEY=your_api_key
DAYS_BACK=14
DRY_RUN=true
LOG_LEVEL=INFO
SYNC_STRATEGY=overwrite  # or skip_if_present
```

## ▶️ Running manually

```bash
python main.py
```

## 🧪 Testing

```bash
pytest
```

## 🔄 Synchronization strategies

Use `SYNC_STRATEGY` to control how the tool behaves when Immich already has a description:

- `overwrite` – always overwrite existing Immich descriptions
- `skip_if_present` – skip updating if Immich already has a description

## 🧯 Dry-run mode

When `DRY_RUN=true`, updates to Immich are skipped but logged, so you can verify the behavior safely.

## 📃 Logging

Set `LOG_LEVEL=DEBUG` (or INFO/WARNING/ERROR) to control verbosity. Each module uses structured logging.

## 🧭 Roadmap

- Export summary of changes
- Asynchronous sync engine
- Album sync support
- CLI interface
- Docker image publishing

See `issues.md` for detailed ideas.

---

Project licensed under MIT.
