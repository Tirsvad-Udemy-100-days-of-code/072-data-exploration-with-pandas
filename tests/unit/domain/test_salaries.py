from __future__ import annotations

import pandas as pd

from college_majors.domain import salaries as cols


def test_drop_missing_removes_rows_with_missing_values(small_frame: pd.DataFrame) -> None:
    result = cols.drop_missing(small_frame)

    assert len(result) == 6
    assert "Source: X" not in set(result[cols.MAJOR])


def test_drop_missing_leaves_input_unchanged(small_frame: pd.DataFrame) -> None:
    cols.drop_missing(small_frame)

    assert len(small_frame) == 7


def test_add_spread_inserts_spread_as_second_column(small_clean: pd.DataFrame) -> None:
    result = cols.add_spread(small_clean)

    assert list(result.columns)[1] == cols.SPREAD
    assert len(result.columns) == len(small_clean.columns) + 1


def test_add_spread_is_p90_minus_p10(small_clean: pd.DataFrame) -> None:
    result = cols.add_spread(small_clean).set_index(cols.MAJOR)

    assert result.loc["Alpha", cols.SPREAD] == 70000.0
    assert result.loc["Zeta", cols.SPREAD] == 25000.0


def test_add_spread_does_not_mutate_input(small_clean: pd.DataFrame) -> None:
    cols.add_spread(small_clean)

    assert cols.SPREAD not in small_clean.columns


def test_add_spread_on_real_data_has_spread_at_position_one(raw_frame: pd.DataFrame) -> None:
    result = cols.add_spread(cols.drop_missing(raw_frame))

    assert result.columns[1] == cols.SPREAD
    assert result.shape == (50, 7)
