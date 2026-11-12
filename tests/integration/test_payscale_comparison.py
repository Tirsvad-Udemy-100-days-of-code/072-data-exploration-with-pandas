from __future__ import annotations

import pandas as pd

from college_majors.application import comparison as cmp
from college_majors.infrastructure.csv_repository import read_payscale_majors


def test_real_data_matches_at_least_20_majors_and_finds_finance(raw_frame: pd.DataFrame) -> None:
    table = cmp.compare_with_2008(raw_frame.dropna(), read_payscale_majors())

    assert len(table) >= 20  # the 2008 table has only 50 majors; many have no namesake
    assert cmp.where_is(table, "Finance") is not None


def test_real_data_matches_the_renamed_majors_through_the_aliases(raw_frame: pd.DataFrame) -> None:
    unmatched = cmp.unmatched_2008_majors(raw_frame.dropna(), read_payscale_majors())

    assert "Math" not in unmatched
    assert "Physician Assistant" not in unmatched
