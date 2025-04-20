# gphoto2immich

A Python-based Docker tool for syncing metadata (e.g. descriptions, titles, albums) from **Google Photos** into your **Immich** instance.

---

## ✨ Features

- Connects to Google Photos using OAuth 2.0
- Looks back (default 15 days) to fetch newly uploaded or updated media
- Finds matching files in Immich by filename
- Updates metadata (e.g. descriptions) in Immich via its API
- Easily configurable via `.env`
- Fully testable with `pytest`

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourname/gphoto2immich.git
cd gphoto2immich
```

### 2. Setup `.env` file

Create your own `.env` file based on the example:

```bash
cp .env.example .env
```

Then edit the values to match your environment. See [below](#configuration-values) for how to obtain them.

### 3. Build & Run via Docker Compose

```bash
docker compose up --build
```

This will launch the app, authorize access to your Google Photos account, and begin syncing.

---

## ⚙️ Configuration Values

| Variable              | Description                                                  |
|-----------------------|--------------------------------------------------------------|
| `GOOGLE_CREDENTIALS_PATH` | Path to your OAuth2 `credentials.json` downloaded from Google Cloud |
| `IMMICH_BASE_URL`     | Base URL of your Immich instance (e.g., `http://host/api`)   |
| `IMMICH_API_KEY`      | API key for your Immich user (generated in web UI)           |
| `DAYS_BACK`           | Number of days to look back for changed photos (default: 15) |

For a detailed guide on obtaining these values, see the [MVP document](./gphoto2immich-mvp,md).

---

## 🧪 Running Tests

You can run the test suite locally:

```bash
pytest
```

---

## 📦 Project Structure

```
app/
  config.py           # Loads .env config
  gphotos_client.py   # Google Photos API
  immich_client.py    # Immich API wrapper
  sync.py             # Core logic
tests/
  test_*.py           # Unit tests
```

---

## 📋 License

MIT License
