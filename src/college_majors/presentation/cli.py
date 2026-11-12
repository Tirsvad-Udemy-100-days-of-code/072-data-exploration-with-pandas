"""Command line: prints every lecture step of Day 72 in order."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import TextIO

import pandas as pd

from college_majors.application import comparison as cmp
from college_majors.application import lecture_steps as steps
from college_majors.application.answers import answer_five_questions
from college_majors.infrastructure import wayback_scraper as wayback
from college_majors.infrastructure.csv_repository import read_data, read_payscale_majors

# The day whose captures of the report are scraped.
WAYBACK_DAY = "20200214"


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
    _render_answers(cleaned, out)
    _render_extra_credit(cleaned, read_payscale_majors(), out)


def _render_answers(cleaned: pd.DataFrame, out: TextIO) -> None:
    answers = answer_five_questions(cleaned)
    _section(out, "Step 11: answers to the five questions", "")
    _section(out, "1. Highest starting salaries", answers.highest_starting)
    _section(out, "2a. Lowest starting salaries", answers.lowest_starting)
    _section(out, "2b. Lowest mid-career salaries", answers.lowest_mid_career)
    _section(out, "3. Highest earning potential", answers.highest_potential)
    _section(out, "4. Lowest risk", answers.lowest_risk)
    _section(out, "5. Average salary per group", answers.group_averages)
    out.write(f"Highest mean mid-career salary: {answers.best_group}\n")


def _render_extra_credit(cleaned: pd.DataFrame, newer: pd.DataFrame, out: TextIO) -> None:
    _section(out, "Step 12: extra credit, what changed since 2008", "")
    table = cmp.compare_with_2008(cleaned, newer)
    unmatched = cmp.unmatched_2008_majors(cleaned, newer)
    out.write(f"Newer data: PayScale snapshot {cmp.snapshot_year(newer)}, {len(newer)} majors\n")
    out.write(f"Majors in both data sets: {len(table)} of {len(cleaned)}\n")
    out.write(f"2008 majors without a match: {', '.join(unmatched) or 'none'}\n")
    _section(out, "Biggest gainers (mid-career pay)", cmp.biggest_gainers(table))
    _section(out, "Biggest losers (mid-career pay)", cmp.biggest_losers(table))
    standing = cmp.where_is(table, "Finance")
    if standing is None:
        out.write("\nFinance is not in both data sets\n")
    else:
        out.write(
            f"\nFinance by mid-career pay: rank {standing.rank_then} in 2008, "
            f"rank {standing.rank_now} now\n"
        )


def _scrape_wayback(output: Path, out: TextIO) -> int:
    try:
        result = wayback.scrape(WAYBACK_DAY)
    except wayback.WaybackError as error:
        sys.stderr.write(f"Scrape failed: {error}\n")
        return 1
    wayback.write_csv(result.rows, output, result.snapshot)
    out.write(f"Wrote {len(result.rows)} majors from capture {result.snapshot} to {output}\n")
    out.write(f"Captures used per page: {', '.join(result.page_captures)}\n")
    return 0


def main(argv: Sequence[str] | None = None, out: TextIO | None = None) -> int:
    """Run the command line and return the exit code."""
    parser = argparse.ArgumentParser(description="Day 72: data exploration with pandas")
    parser.add_argument("--csv", type=Path, default=None, help="path to the salaries CSV file")
    parser.add_argument(
        "--scrape-wayback",
        type=Path,
        default=None,
        metavar="OUTPUT_CSV",
        help="fetch the archived PayScale report (slow, uses the network) and save it as CSV",
    )
    args = parser.parse_args(argv)
    stream = out if out is not None else sys.stdout
    if args.scrape_wayback is not None:
        return _scrape_wayback(args.scrape_wayback, stream)
    render(read_data(args.csv), stream)
    return 0
