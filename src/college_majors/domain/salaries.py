"""Column names and pure rules about the salary table."""

from __future__ import annotations

import pandas as pd

MAJOR = "Undergraduate Major"
STARTING = "Starting Median Salary"
MID_CAREER = "Mid-Career Median Salary"
P10 = "Mid-Career 10th Percentile Salary"
P90 = "Mid-Career 90th Percentile Salary"
GROUP = "Group"
SPREAD = "Spread"


def drop_missing(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a copy without the rows that contain a missing value."""
    return frame.dropna()


def add_spread(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with the Spread column (90th minus 10th percentile) as the second column."""
    spread = frame[P90] - frame[P10]
    result = frame.copy()
    result.insert(1, SPREAD, spread)
    return result
