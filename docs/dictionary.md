# Domain Dictionary (PO and IT terms)

## Metadata
| Key | Value |
| --- | --- |
| ID | DICT-001 |
| CrossReference | [BC-001], [SA-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-11 | Accepted | Jens Tirsvad Nielsen | S02 (AI as stand-in) | Initial version | [b409b30] |

---
## Purpose and Scope

The PO language is English (`en`) and the domain is IT (`it`). The dictionary records the words of the salary data exploration (Product Owner, PO, terms) and the matching names used in code (IT terms).

## Dictionary

| PO term | Language | IT term | Definition | Used as PO term in | Used as IT term in |
| --- | --- | --- | --- | --- | --- |
| Degree group | en | Group column | A category of majors: Business, HASS or STEM. | BC, MIL | source code |
| Low-risk major | en | Smallest-spread row | A major whose salary spread is small, so the earnings are more certain. | BC, MIL | source code |
| Major | en | Row | One undergraduate degree subject with its salary figures. | BC, SA, MIL | source code |
| Mid-career salary | en | Mid-Career Median Salary column | The median salary of graduates with ten or more years of experience. | BC, MIL | source code |
| Missing value | en | NaN | A blank or non-numeric cell that the cleaning step removes. | BC, MIL | source code |
| Salary spread | en | Spread column | The mid-career 90th percentile salary minus the 10th percentile salary. | BC, MIL | source code |
| Starting salary | en | Starting Median Salary column | The median salary of graduates at the start of their career. | BC, MIL | source code |

## Rules

- The PO term is used in the Business Case, Stakeholder Analysis and milestones; the IT term is used in source code and technical artifacts.
- One IT term belongs to one PO term and the reverse.
- Rows are in ascending order of the PO term, case-insensitive.

---

[BC-001]: ./business-case.md
[SA-001]: ./stakeholder-analysis.md
[b409b30]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/commit/b409b30d933875a01860e78a6a26ccda86d6a9b3
