from __future__ import annotations

import io
import subprocess
import sys
from pathlib import Path

import pytest

from college_majors.presentation.cli import main

HEADINGS = [
    "Step 1: head",
    "Step 2: shape",
    "Step 3: columns",
    "Step 4: tail (junk row)",
    "Step 5: clean (dropna)",
    "Step 6: highest starting salary",
    "Step 7: highest mid-career salary",
    "Step 7: lowest starting salary",
    "Step 7: lowest mid-career salary",
    "Step 8: lowest risk majors",
    "Step 9: highest potential",
    "Step 9: greatest spread",
    "Step 10: majors per group",
    "Step 10: average salary by group",
]


def _run_main(*argv: str) -> tuple[int, str]:
    out = io.StringIO()
    code = main(list(argv), out)
    return code, out.getvalue()


def test_main_prints_every_step_heading_and_physician_assistant() -> None:
    code, text = _run_main()

    assert code == 0
    for heading in HEADINGS:
        assert f"== {heading} ==" in text
    assert "Physician Assistant" in text


def test_main_prints_all_columns_without_truncation() -> None:
    _, text = _run_main()

    assert "..." not in text
    assert "Mid-Career 90th Percentile Salary" in text


def test_main_formats_floats_with_two_decimals_and_keeps_value_object_repr() -> None:
    _, text = _run_main()

    assert "74300.0" in text  # the MajorSalary value object
    assert "53,862.50" in text  # a float table cell, two decimals and thousands separator


def test_main_does_not_change_global_pandas_options() -> None:
    import pandas as pd

    before = pd.get_option("display.max_columns")
    _run_main()

    assert pd.get_option("display.max_columns") == before


def test_main_reads_csv_given_with_option(tmp_path: Path) -> None:
    csv = tmp_path / "x.csv"
    csv.write_text(
        "Undergraduate Major,Starting Median Salary,Mid-Career Median Salary,"
        "Mid-Career 10th Percentile Salary,Mid-Career 90th Percentile Salary,Group\n"
        "Solo Major,1.0,2.0,1.0,3.0,STEM\n",
        encoding="utf-8",
        newline="\n",
    )

    code, text = _run_main("--csv", str(csv))

    assert code == 0
    assert "Solo Major" in text


def test_main_writes_to_stdout_by_default(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([]) == 0

    assert "Physician Assistant" in capsys.readouterr().out


def test_python_dash_m_runs_with_exit_code_zero() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "college_majors"],
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )

    assert result.returncode == 0, result.stderr
    assert "Physician Assistant" in result.stdout


def test_dunder_main_module_exits_with_zero_when_run_as_main(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    import runpy

    monkeypatch.setattr(sys, "argv", ["college_majors"])
    with pytest.raises(SystemExit) as exit_info:
        runpy.run_module("college_majors", run_name="__main__")

    assert exit_info.value.code == 0
    assert "Step 1: head" in capsys.readouterr().out
