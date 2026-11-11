"""One function per lecture step of Day 72, named after the assignment."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from college_majors.domain import salaries as col


@dataclass(frozen=True, slots=True)
class MajorSalary:
    """A major together with one salary figure."""

    major: str
    salary: float


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


def _best(frame: pd.DataFrame, column: str, *, highest: bool) -> MajorSalary:
    index = frame[column].idxmax() if highest else frame[column].idxmin()
    return MajorSalary(str(frame[col.MAJOR].loc[index]), float(frame[column].loc[index]))


def highest_starting_salary(frame: pd.DataFrame) -> MajorSalary:
    """Find the major with the highest starting salary (max, idxmax, loc)."""
    return _best(frame, col.STARTING, highest=True)


def highest_mid_career_salary(frame: pd.DataFrame) -> MajorSalary:
    """Find the major with the highest mid-career salary."""
    return _best(frame, col.MID_CAREER, highest=True)


def lowest_starting_salary(frame: pd.DataFrame) -> MajorSalary:
    """Find the major with the lowest starting salary (min, idxmin)."""
    return _best(frame, col.STARTING, highest=False)


def lowest_mid_career_salary(frame: pd.DataFrame) -> MajorSalary:
    """Find the major with the lowest mid-career salary."""
    return _best(frame, col.MID_CAREER, highest=False)


def add_spread(frame: pd.DataFrame) -> pd.DataFrame:
    """Add the Spread column, like df.insert()."""
    return col.add_spread(frame)


def lowest_risk_majors(frame: pd.DataFrame, count: int = 5) -> pd.DataFrame:
    """Return the majors with the smallest spread (sort_values, ascending)."""
    return add_spread(frame).sort_values(col.SPREAD)[[col.MAJOR, col.SPREAD]].head(count)


def highest_potential_majors(frame: pd.DataFrame, count: int = 5) -> pd.DataFrame:
    """Return the majors with the highest 90th percentile mid-career salary."""
    ranked = frame.sort_values(col.P90, ascending=False)
    return ranked[[col.MAJOR, col.P90]].head(count)


def greatest_spread_majors(frame: pd.DataFrame, count: int = 5) -> pd.DataFrame:
    """Return the majors with the largest spread between high and low earners."""
    ranked = add_spread(frame).sort_values(col.SPREAD, ascending=False)
    return ranked[[col.MAJOR, col.SPREAD]].head(count)


def majors_per_group(frame: pd.DataFrame) -> pd.Series:
    """Count the majors in each group (groupby, count)."""
    return frame.groupby(col.GROUP)[col.MAJOR].count()


def average_salary_by_group(frame: pd.DataFrame) -> pd.DataFrame:
    """Return the mean of every numeric column per group (groupby, mean)."""
    return frame.groupby(col.GROUP).mean(numeric_only=True)
