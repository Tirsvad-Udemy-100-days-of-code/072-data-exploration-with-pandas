"""Shared fixtures."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from college_majors.domain import salaries as cols
from college_majors.infrastructure.csv_repository import read_data

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = PROJECT_ROOT / "notebooks" / "day_72_data_exploration.ipynb"


@pytest.fixture(scope="session")
def _session_raw_frame() -> pd.DataFrame:
    return read_data()


@pytest.fixture
def raw_frame(_session_raw_frame: pd.DataFrame) -> pd.DataFrame:
    """A fresh copy of the real data as shipped, including the junk row."""
    return _session_raw_frame.copy()


@pytest.fixture
def small_frame() -> pd.DataFrame:
    """Six majors in three groups plus one junk row with missing values."""
    rows = [
        ("Alpha", 40000.0, 70000.0, 30000.0, 100000.0, "Business"),
        ("Beta", 50000.0, 90000.0, 60000.0, 110000.0, "STEM"),
        ("Gamma", 30000.0, 50000.0, 40000.0, 60000.0, "HASS"),
        ("Delta", 60000.0, 120000.0, 50000.0, 200000.0, "STEM"),
        ("Epsilon", 35000.0, 60000.0, 25000.0, 90000.0, "Business"),
        ("Zeta", 45000.0, 80000.0, 70000.0, 95000.0, "HASS"),
    ]
    columns = [cols.MAJOR, cols.STARTING, cols.MID_CAREER, cols.P10, cols.P90, cols.GROUP]
    frame = pd.DataFrame(rows, columns=columns)
    nan = float("nan")
    junk = pd.DataFrame([["Source: X", nan, nan, nan, nan, None]], columns=columns)
    return pd.concat([frame, junk], ignore_index=True)


@pytest.fixture
def small_clean(small_frame: pd.DataFrame) -> pd.DataFrame:
    """The synthetic table without the junk row."""
    return small_frame.dropna()


@pytest.fixture
def notebook_path() -> Path:
    """The Day 72 notebook that ships with the project."""
    return NOTEBOOK_PATH
