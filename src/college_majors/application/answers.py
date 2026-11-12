"""The answers to the five questions of the Day 72 assignment."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from college_majors.application import lecture_steps as steps
from college_majors.domain import salaries as col


@dataclass(frozen=True, slots=True)
class FiveAnswers:
    """One table per question; question 5 also names the best group."""

    highest_starting: pd.DataFrame
    lowest_starting: pd.DataFrame
    lowest_mid_career: pd.DataFrame
    highest_potential: pd.DataFrame
    lowest_risk: pd.DataFrame
    group_averages: pd.DataFrame
    best_group: str


def _group_averages(frame: pd.DataFrame) -> pd.DataFrame:
    means = steps.average_salary_by_group(frame)[[col.STARTING, col.MID_CAREER]]
    return means.sort_values(col.MID_CAREER, ascending=False)


def answer_five_questions(frame: pd.DataFrame) -> FiveAnswers:
    """Answer the five assignment questions from the cleaned table."""
    group_averages = _group_averages(frame)
    return FiveAnswers(
        highest_starting=steps.highest_starting_salary_majors(frame),
        lowest_starting=steps.lowest_starting_salary_majors(frame),
        lowest_mid_career=steps.lowest_mid_career_salary_majors(frame),
        highest_potential=steps.highest_potential_majors(frame),
        lowest_risk=steps.lowest_risk_majors(frame),
        group_averages=group_averages,
        best_group=str(group_averages.index[0]),
    )
