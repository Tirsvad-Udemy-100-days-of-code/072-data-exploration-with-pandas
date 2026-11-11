from __future__ import annotations

import pandas as pd

from college_majors.application import lecture_steps as steps
from college_majors.domain import salaries as cols


# --- synthetic data -------------------------------------------------------
def test_head_returns_requested_number_of_rows(small_frame: pd.DataFrame) -> None:
    assert len(steps.head(small_frame, 3)) == 3
    assert len(steps.head(small_frame)) == 5


def test_tail_returns_last_rows_including_junk(small_frame: pd.DataFrame) -> None:
    assert steps.tail(small_frame, 2)[cols.MAJOR].tolist() == ["Zeta", "Source: X"]


def test_shape_and_columns_describe_the_frame(small_frame: pd.DataFrame) -> None:
    assert steps.shape(small_frame) == (7, 6)
    assert steps.columns(small_frame)[0] == cols.MAJOR
    assert len(steps.columns(small_frame)) == 6


def test_missing_values_flags_only_junk_row(small_frame: pd.DataFrame) -> None:
    flags = steps.missing_values(small_frame)

    assert flags.iloc[-1, 1:].all()
    assert not flags.iloc[:-1].to_numpy().any()


def test_clean_drops_junk_row(small_frame: pd.DataFrame) -> None:
    assert steps.shape(steps.clean(small_frame)) == (6, 6)
















# --- real data ------------------------------------------------------------
def test_raw_real_data_has_51_rows_and_6_columns(raw_frame: pd.DataFrame) -> None:
    assert steps.shape(raw_frame) == (51, 6)


def test_cleaned_real_data_has_50_rows_and_6_columns(raw_frame: pd.DataFrame) -> None:
    assert steps.shape(steps.clean(raw_frame)) == (50, 6)


def test_real_data_junk_row_is_last_and_removed_by_clean(raw_frame: pd.DataFrame) -> None:
    assert steps.tail(raw_frame, 1)[cols.MAJOR].iloc[0].startswith("Source:")
    assert not steps.clean(raw_frame)[cols.MAJOR].str.startswith("Source:").any()












