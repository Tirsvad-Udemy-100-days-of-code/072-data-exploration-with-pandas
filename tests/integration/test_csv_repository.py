from __future__ import annotations

import shutil
from pathlib import Path

import nbformat
import pytest
from nbclient import NotebookClient

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
