# Extra Credit

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-006 |
| CrossReference | [BC-001], [MIL-005] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-12 | Accepted | Jens Tirsvad Nielsen | S02 (AI as stand-in) | Initial version | [5300bd8] |

---

## Purpose

Decide whether the lecture's extra credit is answered: do the 2008 results still hold with newer PayScale data? The lecture says PayScale's site is paywalled now, so the Wayback Machine is the source.

## Deliverable

A scraper for the archived PayScale college salary report that uses only the Python standard library, the parsed result saved as a CSV file in the repository, a comparison with the 2008 data, and a notebook section, a command line step, a screenshot, the README and the wiki in three languages that show what changed.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | The Business Case amendment has a `Go` review and is `Accepted` | Yes | No-Go open |
| 2 | The scraper parses the archived report into a CSV with major, early career pay, mid-career pay and the snapshot date, and its tests run offline on sample markup | Passes | Fails |
| 3 | The CSV holds at least 100 majors and the run needs no new runtime dependency | Yes | No |
| 4 | The comparison names the majors present in both data sets and shows early and mid-career pay then and now | Present | Missing |
| 5 | The notebook, command line, README and the wiki (en, da, ms) show the comparison with a screenshot | Present | Any missing |
| 6 | Code review of the changes has a `Go`; opengrep reports no open finding | Go, 0 findings | No-Go or any finding |

## Dependencies

| Depends on | Reason |
| --- | --- |
| [MIL-005] | Builds on the final notebook and answers |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| Objective 8 | [BC-001] |

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
| 1 | Business Case amendment | Move the extra credit into scope in the Business Case (new objective, scope item, risk and constraint), review it and accept it before any code is written. | No | |
| 2 | Wayback scraper | Fetch an archived PayScale college salary report from the Wayback Machine with the standard library only (one polite request, generic client name) and parse its table into rows of major, degree type, early career pay and mid-career pay. Tests run offline on sample markup. | No | |
| 3 | Newer data set | Run the scraper once and save the result as a CSV file in the package data with the source URL and snapshot date, so nobody needs the network to use the project. | No | |
| 4 | Comparison with 2008 | Join the 2008 and newer data by major and add functions that show the change in early and mid-career pay and in rank, for example where Finance stands now. Add tests. | No | |
| 5 | Notebook and command line | Add the extra credit section to the notebook (also summarised at the top) and a command line step, and extend the notebook test. | No | |
| 6 | Screenshot, README and wiki | Generate the screenshot, update the README and the wiki in English, Danish and Bahasa Malaysia, then run the code review and opengrep. | No | |

---

[BC-001]: ../business-case.md
[MIL-005]: ./mil-005-answers-on-top.md
[5300bd8]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/commit/5300bd8071e1dc27c4689348b5989bde1a698582
