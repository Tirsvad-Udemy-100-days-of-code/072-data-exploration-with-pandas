"""Reads the salary table from a CSV file."""

from __future__ import annotations

from importlib import resources
from pathlib import Path

import pandas as pd

DATA_FILE = "salaries_by_college_major.csv"


def default_path() -> Path:
    """Return the path of the CSV file that ships with the package."""
    return Path(str(resources.files("college_majors") / "data" / DATA_FILE))


def read_data(path: Path | str | None = None) -> pd.DataFrame:
    """Read the salary table; use the packaged file when no path is given."""
    return pd.read_csv(path if path is not None else default_path())
