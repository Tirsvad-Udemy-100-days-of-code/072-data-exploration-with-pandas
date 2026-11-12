"""Reads the salary table from a CSV file."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA_FILE = "salaries_by_college_major.csv"
PAYSCALE_FILE = "payscale_majors_wayback.csv"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def default_path() -> Path:
    """Return the path of the CSV file that ships with the package."""
    return DATA_DIR / DATA_FILE


def read_data(path: Path | str | None = None) -> pd.DataFrame:
    """Read the salary table; use the packaged file when no path is given."""
    return pd.read_csv(path if path is not None else default_path())


def default_payscale_path() -> Path:
    """Return the path of the newer PayScale CSV file that ships with the package."""
    return DATA_DIR / PAYSCALE_FILE


def read_payscale_majors(path: Path | str | None = None) -> pd.DataFrame:
    """Read the PayScale majors saved by the Wayback scraper; default to the packaged file."""
    return pd.read_csv(path if path is not None else default_payscale_path())
