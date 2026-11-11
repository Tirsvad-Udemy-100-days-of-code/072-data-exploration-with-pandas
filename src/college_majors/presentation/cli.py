"""Command line: prints every lecture step of Day 72 in order."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import TextIO

import pandas as pd

from college_majors.application import lecture_steps as steps
from college_majors.infrastructure.csv_repository import read_data


def _format_float(value: float) -> str:
    return f"{value:,.2f}"


# Show every column on one line instead of truncating with "...".
_DISPLAY_OPTIONS = (
    "display.float_format",
    _format_float,
    "display.width",
    None,
    "display.max_columns",
    None,
    "display.max_rows",
    None,
)


def _section(out: TextIO, title: str, body: object) -> None:
    out.write(f"\n== {title} ==\n{body}\n")


def render(frame: pd.DataFrame, out: TextIO) -> None:
    """Write the answer of every lecture step to the stream."""
    with pd.option_context(*_DISPLAY_OPTIONS):
        _render_steps(frame, out)


def _render_steps(frame: pd.DataFrame, out: TextIO) -> None:
    _section(out, "Step 1: head", steps.head(frame))
    _section(out, "Step 2: shape", steps.shape(frame))
    _section(out, "Step 3: columns", steps.columns(frame))
    _section(out, "Step 4: tail (junk row)", steps.tail(frame))
    cleaned = steps.clean(frame)
    _section(out, "Step 5: clean (dropna)", steps.tail(cleaned))
    _section(out, "Step 6: highest starting salary", steps.highest_starting_salary(cleaned))
    _section(out, "Step 7: highest mid-career salary", steps.highest_mid_career_salary(cleaned))
    _section(out, "Step 7: lowest starting salary", steps.lowest_starting_salary(cleaned))
    _section(out, "Step 7: lowest mid-career salary", steps.lowest_mid_career_salary(cleaned))
    _section(out, "Step 8: lowest risk majors", steps.lowest_risk_majors(cleaned))
    _section(out, "Step 9: highest potential", steps.highest_potential_majors(cleaned))
    _section(out, "Step 9: greatest spread", steps.greatest_spread_majors(cleaned))
    _section(out, "Step 10: majors per group", steps.majors_per_group(cleaned))
    _section(out, "Step 10: average salary by group", steps.average_salary_by_group(cleaned))


def main(argv: Sequence[str] | None = None, out: TextIO | None = None) -> int:
    """Run the command line and return the exit code."""
    parser = argparse.ArgumentParser(description="Day 72: data exploration with pandas")
    parser.add_argument("--csv", type=Path, default=None, help="path to the salaries CSV file")
    args = parser.parse_args(argv)
    render(read_data(args.csv), out if out is not None else sys.stdout)
    return 0
