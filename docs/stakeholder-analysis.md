# Stakeholder Analysis

## Metadata
| Key | Value |
| --- | --- |
| ID | SA-001 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-11 | Accepted | Jens Tirsvad Nielsen | S02 (AI as stand-in) | Initial version | [b409b30] |

---
## Purpose

This analysis identifies who is affected by the Day 72 pandas project and what each group needs, so that the requirements, reviews and documentation serve them. It uses a power/interest grid and maps concerns to FURPS+.

## Stakeholder Summary Table

| ID | Name | Role/Title | Organization | Power Level | Interest Level | Quadrant | Primary Concern (Business Language) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | Jens Tirsvad Nielsen | Course participant, Product Owner, developer and reviewer | Tirsvad | HIGH | HIGH | Manage Closely | A correct, tested solution of the assignment that follows the framework |
| S02 | Udemy coursists | Fellow course participants | Udemy community | LOW | HIGH | Keep Informed | Readable, runnable code with the assignment function names, and run instructions |
| S03 | GitHub viewers | Repository visitors | Public | LOW | MEDIUM | Keep Informed | A clear description, topics and README, and no runtime dependencies beyond what is needed |

## Power/Interest Classification Rationale

- **Manage Closely (S01):** decides scope, writes, reviews and accepts every artifact.
- **Keep Informed (S02, S03):** cannot change the scope, but their needs shape the README, the function names and the wiki. S02 is the main audience; S03 is a lighter, browsing audience.

## Primary Concerns and FURPS+ Mapping

| Concern ID | Stakeholder | Concern | FURPS+ attribute |
| --- | --- | --- | --- |
| CN-001 | S01 | The five questions of the assignment are answered correctly from the data | Functionality |
| CN-002 | S01 | Every function is covered by tests that run offline | Reliability |
| CN-003 | S02 | Function names match the assignment so solutions can be compared | Usability |
| CN-004 | S02 | Clear instructions to create `.venv`, install and run | Usability |
| CN-005 | S02 | The wiki explains what each lecture step taught, in their language | Usability |
| CN-006 | S03 | A clear repository description, topics and README | Usability |
| CN-007 | S03 | No runtime dependencies beyond pandas; Jupyter only as an optional extra | Implementation |

## Communication Requirements

| ID | Channel | Frequency | Deliverable | Phase / Milestone |
| --- | --- | --- | --- | --- |
| CR-001 | Chat with S01 | Per request | Plan for acceptance, then a run summary | All milestones |
| CR-002 | Pull request | One per milestone | Change set with closing issue lines | MIL-001, MIL-002, MIL-003 |
| CR-003 | README and wiki | On release | Run instructions, screenshots, lecture explanations | MIL-003 |

## Conflicting Interests and Mitigations

| Conflict | Stakeholders | Mitigation |
| --- | --- | --- |
| S03 wants no runtime dependencies; the assignment is about pandas and Jupyter | S03, S01 | pandas is the only runtime dependency; JupyterLab and test tools are optional extras, stated in the README |
| S02 wants the assignment names; clean code prefers descriptive Python names | S02, S01 | Keep the assignment names for the public functions and document the mapping |

## Traceability Analysis

### Business Goal Alignment

| Stakeholder | Concern | Business Case objective |
| --- | --- | --- |
| S01 | CN-001, CN-002 | [BC-001] objectives 2 and 3 |
| S02 | CN-003, CN-004, CN-005 | [BC-001] objectives 1, 4 and 6 |
| S03 | CN-006, CN-007 | [BC-001] objectives 4, 5 and 7 |

## Sign-Off

Pending the review record of this document; the Product Owner (S01) accepts the plan in chat.

---

[BC-001]: ./business-case.md
[b409b30]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/commit/b409b30d933875a01860e78a6a26ccda86d6a9b3
