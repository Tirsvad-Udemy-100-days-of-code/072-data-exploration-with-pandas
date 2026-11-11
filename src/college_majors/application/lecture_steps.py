"""One function per lecture step of Day 72, named after the assignment."""

from __future__ import annotations

import pandas as pd

from college_majors.domain import salaries as col


def head(frame: pd.DataFrame, count: int = 5) -> pd.DataFrame:
    """Return the first rows, like df.head()."""
    return frame.head(count)


def tail(frame: pd.DataFrame, count: int = 5) -> pd.DataFrame:
    """Return the last rows, like df.tail()."""
    return frame.tail(count)


def shape(frame: pd.DataFrame) -> tuple[int, int]:
    """Return the number of rows and columns, like df.shape."""
    return frame.shape


def columns(frame: pd.DataFrame) -> list[str]:
    """Return the column names, like df.columns."""
    return [str(name) for name in frame.columns]


def missing_values(frame: pd.DataFrame) -> pd.DataFrame:
    """Return True where a cell is missing, like df.isna()."""
    return frame.isna()


def clean(frame: pd.DataFrame) -> pd.DataFrame:
    """Return the table without the junk row, like df.dropna()."""
    return col.drop_missing(frame)
