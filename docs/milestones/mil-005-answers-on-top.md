# Answers on Top

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-005 |
| CrossReference | [BC-001], [MIL-004] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-12 | Accepted | Jens Tirsvad Nielsen | S02 (AI as stand-in) | Initial version | [75d20b0] |

---

## Purpose

Decide whether a reader sees the answers to the five questions at once. Today the answers are in Step 11 at the end of the notebook; the reader should find them at the top, directly under the title.

## Deliverable

A section "The five questions and their answers" at the top of the notebook, right after the title, with each question and its answer in one line, and a test that the stated answers match the computed ones.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | The first cells of the notebook show all five questions, each with its answer | 5 of 5 | Any missing |
| 2 | A test checks that the top section names the same majors and group as the computed answers (Physician Assistant, Spanish, Economics, Nursing, STEM) | Passes | Fails |
| 3 | The notebook is executed in a test, stored with outputs, and the README and wiki still match it | Passes | Fails |
| 4 | Code review of the changes has a `Go`; opengrep reports no open finding | Go, 0 findings | No-Go or any finding |

## Dependencies

| Depends on | Reason |
| --- | --- |
| [MIL-004] | Reuses the answers and the notebook test it added |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| Objectives 1 and 2 | [BC-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S02 |

## Target Date

2026-11-14 — inside the Business Case target of 2026-11-18.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Answers at the top of the notebook | Add a section under the title that lists the five questions with one-line answers, and keep Step 11 as the worked proof with tables. The top section must show the real results, so the answers are written from the computed data. | No | |
| 2 | Test and docs | Extend the notebook test so the top section is checked against the computed answers, update the README and wiki text where they describe the notebook layout, and run the code review and opengrep. | No | |

---

[BC-001]: ../business-case.md
[MIL-004]: ./mil-004-answers.md
[75d20b0]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/commit/75d20b0e5eb0b8e38f0779993c9b94a20eee2dc5
