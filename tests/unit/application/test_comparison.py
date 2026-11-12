from __future__ import annotations

import pandas as pd
import pytest

from college_majors.application import comparison as cmp
from college_majors.domain import salaries as col


@pytest.fixture
def old() -> pd.DataFrame:
    return pd.DataFrame(
        {
            col.MAJOR: ["Finance", "Art  History", "Dance", "Physics"],
            col.STARTING: [40000.0, 30000.0, 20000.0, 50000.0],
            col.MID_CAREER: [80000.0, 60000.0, 40000.0, 100000.0],
        }
    )


@pytest.fixture
def newer() -> pd.DataFrame:
    return pd.DataFrame(
        {
            col.MAJOR: ["physics", "FINANCE", "art history", "Finance", "Robotics"],
            col.EARLY_CAREER: [60000, 48000, 33000, 1, 70000],
            col.MID_CAREER_NOW: [110000, 120000, 54000, 1, 130000],
            col.SNAPSHOT: ["2019-02-22"] * 5,
        }
    )


def test_compare_joins_by_normalised_name_and_keeps_the_2008_spelling(
    old: pd.DataFrame, newer: pd.DataFrame
) -> None:
    result = cmp.compare_with_2008(old, newer)

    assert sorted(result[col.MAJOR]) == ["Art  History", "Finance", "Physics"]


def test_compare_computes_change_in_percent_for_early_and_mid_career(
    old: pd.DataFrame, newer: pd.DataFrame
) -> None:
    row = cmp.compare_with_2008(old, newer).set_index(col.MAJOR).loc["Finance"]

    assert row[cmp.EARLY_CHANGE] == pytest.approx(20.0)
    assert row[cmp.MID_CHANGE] == pytest.approx(50.0)
    assert row[cmp.STARTING_THEN] == 40000.0
    assert row[cmp.EARLY_NOW] == 48000


def test_compare_ranks_each_major_by_mid_career_pay_within_its_own_data_set(
    old: pd.DataFrame, newer: pd.DataFrame
) -> None:
    ranks = cmp.compare_with_2008(old, newer).set_index(col.MAJOR)[[cmp.RANK_THEN, cmp.RANK_NOW]]

    assert ranks.loc["Finance"].tolist() == [2, 2]
    assert ranks.loc["Physics"].tolist() == [1, 3]
    assert ranks.loc["Art  History"].tolist() == [3, 4]


def test_unmatched_2008_majors_lists_the_ones_without_a_namesake(
    old: pd.DataFrame, newer: pd.DataFrame
) -> None:
    assert cmp.unmatched_2008_majors(old, newer) == ["Dance"]


def test_biggest_gainers_and_losers_order_by_mid_career_change(
    old: pd.DataFrame, newer: pd.DataFrame
) -> None:
    table = cmp.compare_with_2008(old, newer)

    assert cmp.biggest_gainers(table, 1)[col.MAJOR].tolist() == ["Finance"]
    assert cmp.biggest_losers(table, 2)[col.MAJOR].tolist() == ["Art  History", "Physics"]
    assert len(cmp.biggest_gainers(table)) == 3


def test_where_is_finds_a_major_ignoring_case_and_spacing(
    old: pd.DataFrame, newer: pd.DataFrame
) -> None:
    table = cmp.compare_with_2008(old, newer)

    assert cmp.where_is(table, " finance ") == cmp.MajorStanding("Finance", 2, 2)
    assert cmp.where_is(table, "art history") is not None


def test_where_is_returns_none_for_a_major_missing_from_either_data_set(
    old: pd.DataFrame, newer: pd.DataFrame
) -> None:
    table = cmp.compare_with_2008(old, newer)

    assert cmp.where_is(table, "Dance") is None
    assert cmp.where_is(table, "Robotics") is None


def test_snapshot_year_reads_the_first_four_characters(newer: pd.DataFrame) -> None:
    assert cmp.snapshot_year(newer) == 2019


def test_compare_ignores_a_trailing_abbreviation_and_reads_ampersand_as_and() -> None:
    old = pd.DataFrame(
        {
            col.MAJOR: ["Computer Science", "Arts and Crafts"],
            col.STARTING: [1.0, 1.0],
            col.MID_CAREER: [2.0, 2.0],
        }
    )
    newer = pd.DataFrame(
        {
            col.MAJOR: ["Computer Science (CS)", "Arts & Crafts"],
            col.EARLY_CAREER: [2, 2],
            col.MID_CAREER_NOW: [3, 3],
            col.SNAPSHOT: ["2019-02-22"] * 2,
        }
    )

    assert len(cmp.compare_with_2008(old, newer)) == 2


def test_compare_applies_the_name_aliases_for_majors_renamed_since_2008() -> None:
    old = pd.DataFrame(
        {
            col.MAJOR: ["Math", "Physician Assistant"],
            col.STARTING: [1.0, 1.0],
            col.MID_CAREER: [2.0, 2.0],
        }
    )
    newer = pd.DataFrame(
        {
            col.MAJOR: ["Mathematics", "Physician Assistant Studies"],
            col.EARLY_CAREER: [2, 2],
            col.MID_CAREER_NOW: [3, 3],
            col.SNAPSHOT: ["2020-02-14"] * 2,
        }
    )

    assert len(cmp.compare_with_2008(old, newer)) == 2
    assert cmp.unmatched_2008_majors(old, newer) == []
