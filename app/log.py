"""Logging wrapper for Google Photos 2 Immich."""

import logging
import os
import sys
from datetime import datetime, timezone

LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()


class FixedWidthFormatter(logging.Formatter):
    """ "Formatter that formats log messages with fixed-width fields."""

    def formatTime(self, record: logging.LogRecord, datefmt: str | None = None) -> str:
        """Format the time of the log record.

        :param record: The log record to format.
        :param datefmt: Optional date format string. If None, the default format is used.
        :return: The formatted time string.
        """
        dt: datetime = datetime.fromtimestamp(record.created, tz=timezone.utc).astimezone()
        return dt.strftime("%Y-%m-%dT%H:%M:%S.") + f"{int(record.msecs):03d}" + dt.strftime("%z")

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record.

        :param record: The log record to format.
        :return: The formatted log message.
        """
        record.levelname = f"{record.levelname:<8}"  # Pad level name to 8 chars
        return super().format(record)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name. If no handlers are set, add a StreamHandler with a specific format.

    :param name: The name of the logger.
    :return: A logger instance.
    """
    logger: logging.Logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = FixedWidthFormatter("%(asctime)s - %(levelname)s (%(name)s.%(funcName)s:%(lineno)d) - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(LOG_LEVEL)

    return logger
