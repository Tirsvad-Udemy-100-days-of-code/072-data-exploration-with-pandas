# Traceability Matrix

## Metadata
| Key | Value |
| --- | --- |
| ID | TM-001 |
| CrossReference | [BC-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-11 | Proposed | Jens Tirsvad Nielsen | S02 (AI as stand-in) | Initial version | [b409b30] |

---
## Purpose

Tracks backward and forward links between artifact instances so that the Business Case traceability can be measured. A row is added or updated whenever an artifact instance is created or reviewed.

## Traceability Table

| Artifact Instance | Type | Language | Domain | Upstream (Backward Link) | Downstream (Forward Link) | Last Reviewed (RC-ID) |
| --- | --- | --- | --- | --- | --- | --- |
| [BC-001] | BC | en | it | - | [SA-001], [PP-001] | [RC-001] |
| [SA-001] | SA | en | it | [BC-001] | [PP-001], [DICT-001] | [RC-002] |
| [DICT-001] | DICT | en | it | [BC-001], [SA-001] | - | [RC-003] |
| [PP-001] | PP | en | it | [BC-001], [SA-001] | [MIL-001], [MIL-002], [MIL-003] | [RC-004] |
| [MIL-001] | MIL | en | it | [BC-001], [PP-001] | [MIL-002] | [RC-005] |
| [MIL-002] | MIL | en | it | [MIL-001] | [MIL-003] | [RC-006] |
| [MIL-003] | MIL | en | it | [MIL-002] | - | [RC-007] |
| [WIKI-001] | wiki | en, da, ms | - | [BC-001] | - | [RC-010] |
| [MIL-004] | MIL | en | it | [BC-001], [MIL-002] | - | [RC-011] |
| [PY-001] | PY | - | - | [MIL-001], [MIL-002], [MIL-004] | - | [RC-008], [RC-009], [RC-012] |

## Concern Coverage

| Concern (CN-ID) | Views that answer it | Decisions (ADR) | Quality check (TP) | Status |
| --- | --- | --- | --- | --- |
| CN-001 | none yet (notebook and code come in MIL-002) | - | - | Gap |
| CN-002 | none yet (notebook and code come in MIL-002) | - | - | Gap |
| CN-003 | none yet (notebook and code come in MIL-002) | - | - | Gap |
| CN-004 | none yet (notebook and code come in MIL-002) | - | - | Gap |
| CN-005 | none yet (notebook and code come in MIL-002) | - | - | Gap |
| CN-006 | none yet (notebook and code come in MIL-002) | - | - | Gap |
| CN-007 | none yet (notebook and code come in MIL-002) | - | - | Gap |

## Open Inconsistencies

| # | Views | Inconsistency | Found in (RC-ID) | Status | Resolved in |
| --- | --- | --- | --- | --- | --- |
| 1 | - | none | - | Closed | - |

## Coverage Notes

No architecture views, use cases or test plan exist yet; the concerns are covered by milestone tasks and code. A `-` in Upstream means foundational, in Downstream that nothing is built on it yet.

---

[BC-001]: ../business-case.md
[SA-001]: ../stakeholder-analysis.md
[DICT-001]: ../dictionary.md
[PP-001]: ../project-plan.md
[MIL-001]: ../milestones/mil-001-foundation.md
[MIL-002]: ../milestones/mil-002-analysis.md
[MIL-003]: ../milestones/mil-003-documentation.md
[RC-001]: ./reviews/rc-001-business-case.md
[RC-002]: ./reviews/rc-002-stakeholder-analysis.md
[RC-003]: ./reviews/rc-003-dictionary.md
[RC-004]: ./reviews/rc-004-project-plan.md
[RC-005]: ./reviews/rc-005-mil-001-foundation.md
[RC-006]: ./reviews/rc-006-mil-002-analysis.md
[RC-007]: ./reviews/rc-007-mil-003-documentation.md
[RC-008]: ./reviews/rc-008-python-mil-001.md
[RC-009]: ./reviews/rc-009-python-mil-002.md
[RC-010]: ./reviews/rc-010-wiki.md
[RC-011]: ./reviews/rc-011-mil-004-answers.md
[RC-012]: ./reviews/rc-012-python-mil-004.md
[MIL-004]: ../milestones/mil-004-answers.md
[WIKI-001]: ../wiki/Home.md
[PY-001]: ../../src/college_majors
[b409b30]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/commit/b409b30d933875a01860e78a6a26ccda86d6a9b3
