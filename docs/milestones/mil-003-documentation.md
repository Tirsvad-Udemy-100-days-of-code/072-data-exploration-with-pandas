# Documentation

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-003 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-11 | Accepted | Jens Tirsvad Nielsen | S02 (AI as stand-in) | Initial version | pending |

---
## Purpose

Decide whether the project is documented well enough for coursists and viewers: README, screenshots, a wiki in three languages, and repository metadata.

## Deliverable

A README from the framework template, one screenshot per lecture step in the README and the wiki, a wiki in English, Danish and Bahasa Malaysia explaining what each step taught, and a repository description with topics.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | `check-readme.sh` passes | Exit 0 | Any failure |
| 2 | A screenshot exists for each lecture step in README and wiki | 10 of 10 | Any missing |
| 3 | The wiki has the same page set in `en`, `da` and `ms` | Same set | Any page missing |
| 4 | Repository description and topics are set | Set | Missing |
| 5 | opengrep reports no open finding | 0 findings | Any open finding |

## Dependencies

| Depends on | Reason |
| --- | --- |
| [MIL-002] | The documented output comes from the finished analysis |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| Objectives 4, 5, 6 and 7 | [BC-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S02 |

## Target Date

2026-11-18 — inside the Business Case target of 2026-11-18.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | README | Write `README.md` from the framework template with the venv commands, how to start JupyterLab, `python -m pip install --upgrade pip`, how to run the project and the tests, and the single runtime dependency. | No | |
| 2 | Lecture screenshots | Generate one PNG per lecture step from the executed notebook's cell outputs with a script (no GUI on the host desktop), and embed them in the README. | No | |
| 3 | Wiki in English | Write the wiki pages under `docs/wiki/` explaining what each lecture step taught, with the screenshots. | No | |
| 4 | Wiki in Danish and Bahasa Malaysia | Translate every English page page by page into `-da` and `-ms` files, with the language line and sidebar. | No | |
| 5 | Repository description and topics | Set the description and topics on the git host through its API using the token from `.env`, which is never imported or tested. | No | |

---

[BC-001]: ../business-case.md
[MIL-002]: ./mil-002-analysis.md
