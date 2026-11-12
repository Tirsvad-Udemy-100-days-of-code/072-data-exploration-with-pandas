"""Extra credit: compare the 2008 salaries with newer PayScale data, major by major."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from college_majors.domain import salaries as col

STARTING_THEN = "Starting 2008"
EARLY_NOW = "Early Career Now"
MID_THEN = "Mid-Career 2008"
MID_NOW = "Mid-Career Now"
EARLY_CHANGE = "Early Change %"
MID_CHANGE = "Mid-Career Change %"
RANK_THEN = "Rank 2008"
RANK_NOW = "Rank Now"

# 2008 names that the newer PayScale list spells differently (normalised form -> normalised form).
# Only majors that exist in the newer list under another name are listed.
NAME_ALIASES = {
    "math": "mathematics",
    "physician assistant": "physician assistant studies",
}

_KEY = "_match_key"
_SNAPSHOT_YEAR_LENGTH = 4


@dataclass(frozen=True, slots=True)
class MajorStanding:
    """Where a major stands by mid-career pay in each data set (1 is the highest)."""

    major: str
    rank_then: int
    rank_now: int


def _normalise(names: pd.Series) -> pd.Series:
    """Fold case and spaces, drop a trailing "(CS)", read "&" as "and", apply the aliases."""
    plain = names.str.casefold().str.replace(r"\([^)]*\)\s*$", "", regex=True)
    folded = plain.str.replace("&", "and").str.split().str.join(" ")
    return folded.replace(NAME_ALIASES)


def _keyed(frame: pd.DataFrame, pay_column: str, rank_column: str) -> pd.DataFrame:
    """Add the match key and the rank by pay; the first of two equal names is kept."""
    keyed = frame.assign(**{_KEY: _normalise(frame[col.MAJOR])}).drop_duplicates(_KEY)
    keyed[rank_column] = keyed[pay_column].rank(ascending=False, method="min").astype(int)
    return keyed


def _change_percent(then: pd.Series, now: pd.Series) -> pd.Series:
    return (now - then) / then * 100


def snapshot_year(newer: pd.DataFrame) -> int:
    """Return the year of the newer data set, from its Snapshot column."""
    return int(str(newer[col.SNAPSHOT].iloc[0])[:_SNAPSHOT_YEAR_LENGTH])


def compare_with_2008(cleaned_2008: pd.DataFrame, newer: pd.DataFrame) -> pd.DataFrame:
    """Join both data sets by major name; ranks are by mid-career pay within each data set."""
    old = _keyed(cleaned_2008, col.MID_CAREER, RANK_THEN)
    new = _keyed(newer, col.MID_CAREER_NOW, RANK_NOW)
    merged = old.merge(new, on=_KEY, suffixes=("", "_new"))
    result = pd.DataFrame(
        {
            col.MAJOR: merged[col.MAJOR],
            STARTING_THEN: merged[col.STARTING],
            EARLY_NOW: merged[col.EARLY_CAREER],
            MID_THEN: merged[col.MID_CAREER],
            MID_NOW: merged[col.MID_CAREER_NOW],
            RANK_THEN: merged[RANK_THEN],
            RANK_NOW: merged[RANK_NOW],
        }
    )
    result[EARLY_CHANGE] = _change_percent(result[STARTING_THEN], result[EARLY_NOW])
    result[MID_CHANGE] = _change_percent(result[MID_THEN], result[MID_NOW])
    return result.sort_values(RANK_THEN).reset_index(drop=True)


def unmatched_2008_majors(cleaned_2008: pd.DataFrame, newer: pd.DataFrame) -> list[str]:
    """Return the 2008 majors that have no namesake in the newer data."""
    known = set(_normalise(newer[col.MAJOR]))
    missing = ~_normalise(cleaned_2008[col.MAJOR]).isin(known)
    return [str(name) for name in cleaned_2008.loc[missing, col.MAJOR]]


def _by_change(comparison: pd.DataFrame, count: int, *, ascending: bool) -> pd.DataFrame:
    ranked = comparison.sort_values(MID_CHANGE, ascending=ascending)
    return ranked[[col.MAJOR, MID_THEN, MID_NOW, MID_CHANGE]].head(count).reset_index(drop=True)


def biggest_gainers(comparison: pd.DataFrame, count: int = 5) -> pd.DataFrame:
    """Return the majors whose mid-career pay rose the most, in percent."""
    return _by_change(comparison, count, ascending=False)


def biggest_losers(comparison: pd.DataFrame, count: int = 5) -> pd.DataFrame:
    """Return the majors whose mid-career pay rose the least or fell, in percent."""
    return _by_change(comparison, count, ascending=True)


def where_is(comparison: pd.DataFrame, major: str) -> MajorStanding | None:
    """Return the rank of a major then and now, or None when it is not in both data sets."""
    wanted = " ".join(major.casefold().split())
    rows = comparison[_normalise(comparison[col.MAJOR]) == wanted]
    if rows.empty:
        return None
    row = rows.iloc[0]
    return MajorStanding(str(row[col.MAJOR]), int(row[RANK_THEN]), int(row[RANK_NOW]))
