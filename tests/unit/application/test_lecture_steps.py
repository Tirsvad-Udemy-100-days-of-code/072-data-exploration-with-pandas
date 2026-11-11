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


def test_salary_lookups_on_synthetic_data(small_clean: pd.DataFrame) -> None:
    assert steps.highest_starting_salary(small_clean) == steps.MajorSalary("Delta", 60000.0)
    assert steps.highest_mid_career_salary(small_clean) == steps.MajorSalary("Delta", 120000.0)
    assert steps.lowest_starting_salary(small_clean) == steps.MajorSalary("Gamma", 30000.0)
    assert steps.lowest_mid_career_salary(small_clean) == steps.MajorSalary("Gamma", 50000.0)


def test_lowest_risk_majors_sorted_ascending_by_spread(small_clean: pd.DataFrame) -> None:
    result = steps.lowest_risk_majors(small_clean, 3)

    assert result[cols.MAJOR].tolist() == ["Gamma", "Zeta", "Beta"]
    assert result[cols.SPREAD].is_monotonic_increasing


def test_greatest_spread_majors_sorted_descending_by_spread(small_clean: pd.DataFrame) -> None:
    result = steps.greatest_spread_majors(small_clean, 2)

    assert result[cols.MAJOR].tolist() == ["Delta", "Alpha"]
    assert result[cols.SPREAD].is_monotonic_decreasing


def test_highest_potential_majors_sorted_descending_by_p90(small_clean: pd.DataFrame) -> None:
    result = steps.highest_potential_majors(small_clean, 2)

    assert result[cols.MAJOR].tolist() == ["Delta", "Beta"]


def test_majors_per_group_counts_each_group(small_clean: pd.DataFrame) -> None:
    counts = steps.majors_per_group(small_clean)

    assert counts.to_dict() == {"Business": 2, "HASS": 2, "STEM": 2}


def test_average_salary_by_group_is_mean_per_group(small_clean: pd.DataFrame) -> None:
    means = steps.average_salary_by_group(small_clean)

    assert means.loc["STEM", cols.STARTING] == 55000.0
    assert cols.MAJOR not in means.columns


def test_add_spread_step_does_not_mutate(small_clean: pd.DataFrame) -> None:
    result = steps.add_spread(small_clean)

    assert result.columns[1] == cols.SPREAD
    assert cols.SPREAD not in small_clean.columns


# --- real data ------------------------------------------------------------
def test_raw_real_data_has_51_rows_and_6_columns(raw_frame: pd.DataFrame) -> None:
    assert steps.shape(raw_frame) == (51, 6)


def test_cleaned_real_data_has_50_rows_and_6_columns(raw_frame: pd.DataFrame) -> None:
    assert steps.shape(steps.clean(raw_frame)) == (50, 6)


def test_real_data_junk_row_is_last_and_removed_by_clean(raw_frame: pd.DataFrame) -> None:
    assert steps.tail(raw_frame, 1)[cols.MAJOR].iloc[0].startswith("Source:")
    assert not steps.clean(raw_frame)[cols.MAJOR].str.startswith("Source:").any()


def test_real_highest_starting_salary_is_physician_assistant(raw_frame: pd.DataFrame) -> None:
    result = steps.highest_starting_salary(steps.clean(raw_frame))

    assert result == steps.MajorSalary("Physician Assistant", 74300.0)


def test_real_salary_lookups_match_column_extremes(raw_frame: pd.DataFrame) -> None:
    cleaned = steps.clean(raw_frame)
    lookups = {
        cols.STARTING: (steps.lowest_starting_salary, steps.highest_starting_salary),
        cols.MID_CAREER: (steps.lowest_mid_career_salary, steps.highest_mid_career_salary),
    }

    for column, (lowest, highest) in lookups.items():
        low, high = lowest(cleaned), highest(cleaned)
        assert low.salary == cleaned[column].min()
        assert high.salary == cleaned[column].max()
        assert cleaned.loc[cleaned[cols.MAJOR] == low.major, column].iloc[0] == low.salary
        assert cleaned.loc[cleaned[cols.MAJOR] == high.major, column].iloc[0] == high.salary
        assert low.salary < high.salary


def test_real_ranking_functions_return_five_rows(raw_frame: pd.DataFrame) -> None:
    cleaned = steps.clean(raw_frame)

    for ranking in (
        steps.lowest_risk_majors,
        steps.highest_potential_majors,
        steps.greatest_spread_majors,
    ):
        assert len(ranking(cleaned)) == 5


def test_real_rankings_are_ordered(raw_frame: pd.DataFrame) -> None:
    cleaned = steps.clean(raw_frame)

    assert steps.lowest_risk_majors(cleaned)[cols.SPREAD].is_monotonic_increasing
    assert steps.greatest_spread_majors(cleaned)[cols.SPREAD].is_monotonic_decreasing
    assert steps.highest_potential_majors(cleaned)[cols.P90].is_monotonic_decreasing


def test_real_data_has_three_groups_covering_all_majors(raw_frame: pd.DataFrame) -> None:
    counts = steps.majors_per_group(steps.clean(raw_frame))

    assert len(counts) == 3
    assert counts.sum() == 50


def test_real_data_spread_column_at_position_one(raw_frame: pd.DataFrame) -> None:
    result = steps.add_spread(steps.clean(raw_frame))

    assert result.columns[1] == cols.SPREAD
