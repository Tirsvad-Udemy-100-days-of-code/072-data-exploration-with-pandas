# Foundation

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-001 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-11 | Accepted | Jens Tirsvad Nielsen | S02 (AI as stand-in) | Initial version | pending |

---
## Purpose

Decide whether the project baseline is sound enough to build the analysis on: documents reviewed, a runnable skeleton, and the data loaded and cleaned.

## Deliverable

Accepted Business Case, Stakeholder Analysis, Project Plan and milestones; a Python 3.13+ skeleton with `pyproject.toml`, Python `.gitignore` and `.venv` instructions; the dataset in the repository; a loader and the cleaning step with tests.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | Baseline documents have a `Go` review and are `Accepted` | Yes | Any `No-Go` open |
| 2 | `python -m pytest` passes in a fresh `.venv` | Exit 0 | Any failure |
| 3 | The CSV loads to 51 rows and 6 columns, and 50 rows after cleaning | Matches | Differs |
| 4 | opengrep reports no open finding | 0 findings | Any open finding |

## Dependencies

| Depends on | Reason |
| --- | --- |
| none | First gateway |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| Objectives 3 and 4 | [BC-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S02 |

## Target Date

2026-11-13 — inside the Business Case target of 2026-11-18.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Project skeleton | Create `pyproject.toml` (Python 3.13+, pandas as the only runtime dependency, JupyterLab and nbclient as a `notebook` extra, pytest and coverage as development extras), the Python `.gitignore`, the `src/` and `tests/` layout, the `notebooks/` folder and the venv instructions, including how to start JupyterLab. | No | |
| 2 | Obtain the dataset | Download `salaries_by_college_major.csv` from the link in the assignment, keep it in the repository and record its source. Stop and ask S01 if the link has expired. | No | |
| 3 | Loader and exploration | Implement `read_data` and the exploration helpers for `head`, `tail`, `shape`, `columns` and `isna`, with tests. | No | |
| 4 | Cleaning step | Implement `clean` with `dropna` so the junk last row is removed, leaving 50 majors, with tests. | No | |
| 5 | Local quality gate | Run opengrep (`~/.opengrep/cli/latest/opengrep.exe`) and fix findings before each push. | No | |

---

[BC-001]: ../business-case.md
