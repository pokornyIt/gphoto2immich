# Changelog

## [v0.2.1] - 2025-05-25
### Changed
- Project marked as **frozen** due to deprecation of Google Photos API scopes
- Updated `README.md` with a warning and explanation of the issue
- Removed expectation of functional sync using `photoslibrary.*` scopes

### Notes
- Future development may explore integration with Google Takeout exports or other import paths
- No new functionality was added in this release

## [v0.2.0] - 2025-04-21
### Added
- Better logging
- Synchronization strategy
- Testing

## [v0.1.0] - 2025-04-20
### Added
- Initial working version of gphoto2immich
- Fetching metadata from Google Photos using OAuth2
- Matching photos in Immich by original file name
- Updating Immich asset descriptions
- Dry-run mode for safe testing
- Dockerfile and docker-compose setup
- Pre-commit with mypy, ruff, tests
