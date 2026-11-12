from __future__ import annotations

import shutil
from pathlib import Path

import nbformat
import pandas as pd
import pytest
from nbclient import NotebookClient

from college_majors.application import lecture_steps as steps
from college_majors.application.answers import answer_five_questions
from college_majors.domain import salaries as cols
from college_majors.infrastructure.csv_repository import default_path, read_data


def test_default_path_points_to_packaged_csv() -> None:
    assert default_path().is_file()
    assert default_path().name == "salaries_by_college_major.csv"


def test_read_data_without_path_reads_packaged_file() -> None:
    assert read_data().shape == (51, 6)


def test_read_data_with_explicit_path_reads_that_file(tmp_path: Path) -> None:
    csv = tmp_path / "small.csv"
    csv.write_text("Undergraduate Major,Group\nA,STEM\nB,HASS\n", encoding="utf-8", newline="\n")

    frame = read_data(csv)

    assert frame.shape == (2, 2)
    assert frame["Undergraduate Major"].tolist() == ["A", "B"]


def test_read_data_accepts_string_path(tmp_path: Path) -> None:
    csv = tmp_path / "one.csv"
    csv.write_text("a,b\n1,2\n", encoding="utf-8", newline="\n")

    assert read_data(str(csv)).shape == (1, 2)


def test_read_data_raises_for_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        read_data(tmp_path / "missing.csv")


def test_notebook_executes_end_to_end_without_error(tmp_path: Path, notebook_path: Path) -> None:
    copy = tmp_path / notebook_path.name
    shutil.copy(notebook_path, copy)
    notebook = nbformat.read(copy, as_version=4)

    client = NotebookClient(
        notebook,
        timeout=120,
        kernel_name="python3",
        resources={"metadata": {"path": str(tmp_path)}},
    )
    client.execute()

    errors = [
        out
        for cell in notebook.cells
        if cell.cell_type == "code"
        for out in cell.outputs
        if out.output_type == "error"
    ]
    assert errors == []
    _assert_five_answers_section(notebook)


def _assert_five_answers_section(notebook: nbformat.NotebookNode) -> None:
    sources = "\n".join(str(cell.source) for cell in notebook.cells)
    assert "Step 11: Answers to the five questions" in sources

    outputs = "\n".join(
        str(out.get("text", "")) + str(out.get("data", {}).get("text/plain", ""))
        for cell in notebook.cells
        if cell.cell_type == "code"
        for out in cell.outputs
    )
    for expected in ("Physician Assistant", "Nursing", "Economics", "Best-earning group: STEM"):
        assert expected in outputs


QUESTIONS = [
    "Which degrees have the highest starting salaries?",
    "Which majors have the lowest earnings after college?",
    "Which degrees have the highest earning potential?",
    "What are the lowest-risk majors from an earnings standpoint?",
    "Do Business, STEM or HASS",
]


def test_notebook_states_the_five_answers_on_top(notebook_path: Path) -> None:
    notebook = nbformat.read(notebook_path, as_version=4)
    cell = notebook.cells[1]

    assert cell.cell_type == "markdown"
    assert cell.source.startswith("## The five questions and their answers")
    assert all(question in cell.source for question in QUESTIONS)
    assert all(other.cell_type != "code" for other in notebook.cells[:2])


def test_notebook_top_answers_match_the_computed_answers(
    notebook_path: Path, raw_frame: pd.DataFrame
) -> None:
    text = nbformat.read(notebook_path, as_version=4).cells[1].source
    answers = answer_five_questions(steps.clean(raw_frame))

    stated = [
        answers.highest_starting,
        answers.lowest_starting,
        answers.lowest_mid_career,
        answers.highest_potential,
        answers.lowest_risk,
    ]
    for table in stated:
        assert table[cols.MAJOR].iloc[0] in text
    assert answers.best_group in text
    for number in ("74,300", "210,000", "50,700"):
        assert number in text
