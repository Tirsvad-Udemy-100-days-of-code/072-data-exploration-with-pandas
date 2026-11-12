# Answers

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-004 |
| CrossReference | [BC-001], [MIL-002] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-12 | Accepted | Jens Tirsvad Nielsen | S02 (AI as stand-in) | Initial version | [266ba91] |

---

## Purpose

Decide whether the notebook states a clear answer to each of the five questions of the assignment. Business Case objective 2 asks the project to answer them; the delivered notebook shows the steps but does not state the answers.

## Deliverable

A section "Answers to the five questions" in the notebook, one answer per question, computed by tested functions in `src/` and repeated in the command line, the README and the wiki in three languages with a new screenshot.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | The notebook has one answer for each of the five questions, backed by a computed table | 5 of 5 | Any missing |
| 2 | A test asserts each answer on the real data (for example Physician Assistant tops the starting salaries, STEM has the highest group average) | 5 of 5 | Any missing |
| 3 | The notebook is executed in a test and stored with outputs | Passes | Fails |
| 4 | README and the wiki (en, da, ms) show the answers with a screenshot | Present | Any missing |
| 5 | Code review of the changes has a `Go`; opengrep reports no open finding | Go, 0 findings | No-Go or any finding |

## Dependencies

| Depends on | Reason |
| --- | --- |
| [MIL-002] | Extends its functions and notebook |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| Objectives 2, 5 and 6 | [BC-001] |

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
| 1 | Ranking functions for questions 1 and 2 | Add functions that return the top majors by starting salary and the lowest-earning majors by starting and mid-career salary, so the plural questions "which degrees" and "which majors" have a table, not only a single name. Add tests. | No | |
| 2 | One answer per question | Add an application function that returns the five answers (top starting salaries, lowest earnings, highest potential, lowest risk, best-earning group) from the cleaned data, with tests on the real data. | No | |
| 3 | Answers section in the notebook | Add a section "Answers to the five questions" with a table and a one-sentence answer for each question, and extend the notebook test to check it. | No | |
| 4 | Command line and screenshot | Print the answers in the command line and generate a screenshot (step 11) for the README and the wiki. | No | |
| 5 | README and wiki in three languages | Show the answers in the README and in the English, Danish and Bahasa Malaysia wiki pages, and run the code review and opengrep. | No | |

---

[BC-001]: ../business-case.md
[MIL-002]: ./mil-002-analysis.md
[266ba91]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/commit/266ba914e205440aa9239b715c548992ead5b34e
