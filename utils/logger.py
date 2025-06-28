"""
logger.py: Centralized logger setup for 022_BREAKFAST_REPORT
- Rotating File Handler for Errors (logs/errors/)
- Rotating File Handler for Debug Logs (logs/debug/)
- Rotating File Handler for Info Logs (logs/info/)
- Graylog Handler (only INFO logs)
- Console Handler (only INFO logs)

Usage:
    from utils.logger import get_logger
    logger = get_logger(__name__)
"""

import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

import settings

# Log directories
LOG_DIR = Path(settings.PATH_TO_LOGS)
ERROR_LOG_DIR = LOG_DIR / "errors"
DEBUG_LOG_DIR = LOG_DIR / "debug"
INFO_LOG_DIR = LOG_DIR / "info"

# Create directories if they don't exist
ERROR_LOG_DIR.mkdir(parents=True, exist_ok=True)
DEBUG_LOG_DIR.mkdir(parents=True, exist_ok=True)
INFO_LOG_DIR.mkdir(parents=True, exist_ok=True)

# Log file names
error_log_file = ERROR_LOG_DIR / f"error_{datetime.now().strftime('%Y%m%d')}.log"
info_log_file = INFO_LOG_DIR / f"info_{datetime.now().strftime('%Y%m%d')}.log"
debug_log_file = DEBUG_LOG_DIR / "debug.log"  # Constant name for debug log

# Detailed formatter for Debug and Error logs
_detailed_formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(message)-60s | "
    "%(filename)s | %(funcName)s | Line %(lineno)d"
)

# Simple formatter for Info logs
_emoji_console_formatter = logging.Formatter("🐍 %(levelname)-8s | %(message)-60s")
_file_formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)-60s")


def get_logger(name: Optional[str] = None) -> logging.Logger:
    logger = logging.getLogger(name if name else "breakfast_report")
    logger.propagate = False

    # Avoid duplicate handlers
    if not getattr(logger, "_is_configured", False):
        # Error Rotating File Handler (5MB, 5 backups)
        error_file_handler = RotatingFileHandler(
            error_log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
        )
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.setFormatter(_detailed_formatter)  # Use detailed formatter
        logger.addHandler(error_file_handler)

        # Debug Rotating File Handler (10MB, 1 file)
        debug_file_handler = RotatingFileHandler(
            debug_log_file, maxBytes=10 * 1024 * 1024, backupCount=1, encoding="utf-8"
        )
        debug_file_handler.setLevel(logging.DEBUG)  # Ensure debug logs are printed
        debug_file_handler.setFormatter(_detailed_formatter)  # Use detailed formatter
        logger.addHandler(debug_file_handler)

        # Info Rotating File Handler (file name as date)
        info_file_handler = RotatingFileHandler(
            info_log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
        )
        info_file_handler.setLevel(logging.INFO)
        info_file_handler.setFormatter(_file_formatter)
        logger.addHandler(info_file_handler)

        # Console handler (only INFO logs)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(_emoji_console_formatter)
        logger.addHandler(console_handler)

        # # Graylog Handler (only INFO logs)
        # try:
        #     gelf_handler = GelfUdpHandler(
        #         host=settings.GRAYLOG_SERVER,
        #         port=settings.GRAYLOG_PORT,
        #         debug=True,
        #         include_extra_fields=True,
        #         _app_name=settings.LOG_APP_NAME,
        #     )
        #     gelf_handler.setLevel(logging.INFO)  # Only send INFO logs to Graylog
        #     logger.addHandler(gelf_handler)
        # except Exception as e:
        #     logger.error(f"⚠️ Could not connect to Graylog: {e}")

        # Set global logger level
        logger.setLevel(settings.LOG_LEVEL)
        logger._is_configured = True  # type: ignore # Custom attr to prevent duplicates

    return logger
