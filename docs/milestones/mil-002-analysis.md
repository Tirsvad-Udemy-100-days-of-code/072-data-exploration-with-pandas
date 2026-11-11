# Analysis

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-002 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-11 | Accepted | Jens Tirsvad Nielsen | S02 (AI as stand-in) | Initial version | pending |

---
## Purpose

Decide whether the analysis answers the five questions of the assignment correctly and is covered by tests.

## Deliverable

One function per remaining lecture step and challenge, a Jupyter notebook and a command line that print every answer, and tests with at least 90 percent coverage of `src/`.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | Highest starting salary is 74,300 for Physician Assistant | Matches | Differs |
| 2 | Highest mid-career salary, lowest starting and lowest mid-career majors are reported | All present | Any missing |
| 3 | Lowest-risk, highest-potential and greatest-spread rankings are reported | All present | Any missing |
| 4 | Group averages for Business, HASS and STEM are reported | All present | Any missing |
| 5 | Notebook executes without error in the tests and is stored with outputs | Passes | Fails |
| 6 | Code reviewed against `qc-programming-python` with a `Go` | Go | No-Go |
| 7 | Coverage of `src/` | At least 90 percent | Below 90 percent |

## Dependencies

| Depends on | Reason |
| --- | --- |
| [MIL-001] | Needs the loader, cleaned data and skeleton |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| Objectives 1, 2 and 3 | [BC-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S02 |

## Target Date

2026-11-16 — inside the Business Case target of 2026-11-18.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Highest and lowest earners | Implement the `max`, `idxmax` and `loc` lookups for the highest starting salary, the highest mid-career salary, and the lowest starting and mid-career salaries, returning the major names. | No | |
| 2 | Spread and low-risk majors | Add the `Spread` column with `insert` (90th minus 10th percentile) and rank the lowest-risk majors with `sort_values`. | No | |
| 3 | Highest potential and greatest spread | Rank the top five by 90th percentile mid-career salary and by spread, using `sort_values` descending. | No | |
| 4 | Group by category | Count majors per `Group` and compute the mean salary per group with `groupby`, formatted with two decimals. | No | |
| 5 | Jupyter notebook | Create `notebooks/day_72_data_exploration.ipynb` that follows the lecture steps in order with explanatory markdown, calls the `src/` functions, and keeps its outputs; a test executes it end to end with nbclient. | No | |
| 6 | Command line | Add a `python -m` entry point that prints each lecture step in order, so a coursist can run the whole assignment. | No | |
| 7 | Code review | Review `src/` and `tests/` against `qc-programming-python` and record the `RC-*` before the pull request. | No | |

---

[BC-001]: ../business-case.md
[MIL-001]: ./mil-001-foundation.md
