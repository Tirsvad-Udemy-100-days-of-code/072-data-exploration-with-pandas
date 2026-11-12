from __future__ import annotations

import dataclasses

import pandas as pd
import pytest

from college_majors.application import lecture_steps as steps
from college_majors.application.answers import FiveAnswers, answer_five_questions
from college_majors.domain import salaries as cols


# --- synthetic data -------------------------------------------------------
def test_starting_salary_rankings_on_synthetic_data(small_clean: pd.DataFrame) -> None:
    highest = steps.highest_starting_salary_majors(small_clean, 2)
    lowest = steps.lowest_starting_salary_majors(small_clean, 2)

    assert highest[cols.MAJOR].tolist() == ["Delta", "Beta"]
    assert lowest[cols.MAJOR].tolist() == ["Gamma", "Epsilon"]
    assert list(highest.columns) == [cols.MAJOR, cols.STARTING]


def test_lowest_mid_career_majors_on_synthetic_data(small_clean: pd.DataFrame) -> None:
    result = steps.lowest_mid_career_salary_majors(small_clean, 2)

    assert result[cols.MAJOR].tolist() == ["Gamma", "Epsilon"]
    assert result[cols.MID_CAREER].is_monotonic_increasing


def test_answers_on_synthetic_data(small_clean: pd.DataFrame) -> None:
    answers = answer_five_questions(small_clean)

    assert answers.highest_starting[cols.MAJOR].iloc[0] == "Delta"
    assert answers.lowest_starting[cols.MAJOR].iloc[0] == "Gamma"
    assert answers.lowest_mid_career[cols.MAJOR].iloc[0] == "Gamma"
    assert answers.highest_potential[cols.MAJOR].iloc[0] == "Delta"
    assert answers.lowest_risk[cols.MAJOR].iloc[0] == "Gamma"
    assert answers.best_group == "STEM"
    assert list(answers.group_averages.columns) == [cols.STARTING, cols.MID_CAREER]
    assert answers.group_averages[cols.MID_CAREER].is_monotonic_decreasing


def test_answers_are_immutable(small_clean: pd.DataFrame) -> None:
    answers = answer_five_questions(small_clean)

    with pytest.raises(dataclasses.FrozenInstanceError):
        answers.best_group = "HASS"  # type: ignore[misc]
    assert isinstance(answers, FiveAnswers)


# --- real data ------------------------------------------------------------
def test_real_answers_to_the_five_questions(raw_frame: pd.DataFrame) -> None:
    answers = answer_five_questions(steps.clean(raw_frame))

    assert answers.highest_starting[cols.MAJOR].iloc[0] == "Physician Assistant"
    assert answers.lowest_starting[cols.MAJOR].iloc[0] == "Spanish"
    assert answers.lowest_mid_career[cols.MAJOR].iloc[0] == "Education"
    assert answers.highest_potential[cols.MAJOR].iloc[0] == "Economics"
    assert answers.lowest_risk[cols.MAJOR].iloc[0] == "Nursing"
    assert answers.best_group == "STEM"
    assert len(answers.group_averages) == 3
