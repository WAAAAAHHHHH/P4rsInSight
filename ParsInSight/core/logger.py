"""
P4rsInSight - Logging configuration
Provides a consistent logger used across all modules.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(level: int = logging.DEBUG) -> logging.Logger:
    """
    Configure application-wide logging.

    Outputs to:
      - Console (INFO and above)
      - Rotating log file at ~/.config/parsinSight/parsinSight.log (DEBUG and above)

    Returns the root 'parsinSight' logger.
    """
    log_dir = Path.home() / ".config" / "parsinSight"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "parsinSight.log"

    logger = logging.getLogger("parsinSight")
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger  # Already configured

    # Console handler — INFO and above
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_fmt = logging.Formatter(
        "[%(levelname)s] %(name)s: %(message)s"
    )
    console_handler.setFormatter(console_fmt)

    # Rotating file handler — DEBUG and above, max 2 MB × 3 backups
    file_handler = RotatingFileHandler(
        log_file, maxBytes=2 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_fmt)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Return a child logger under the 'parsinSight' namespace."""
    return logging.getLogger(f"parsinSight.{name}")
