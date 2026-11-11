# Business Case: Day 72 Data Exploration with Pandas

## Metadata
| Key | Value |
| --- | --- |
| ID | BC-001 |
| CrossReference | [SA-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-11 | Accepted | Jens Tirsvad Nielsen | S02 (AI as stand-in) | Initial version | [b409b30] |

---

## Executive Summary

College is expensive, and learners ask whether a degree pays back. This project turns Day 72 of Udemy's "100 Days of Code: The Complete Python Pro Bootcamp" into a runnable, tested Python project. It explores the PayScale post-university salary data by undergraduate major with pandas and answers five questions: highest starting salaries, lowest earnings, highest earning potential, lowest-risk majors, and Business versus STEM (science, technology, engineering, mathematics) versus HASS (humanities, arts, social science) averages. The work is done in a Jupyter notebook that calls tested functions from `src/`. Each lecture step has a function, a notebook section, a screenshot, a README entry and a wiki page in English, Danish and Bahasa Malaysia.

## Methodological and Standards Foundation

Work follows the SQA and QC framework mounted at `framework/`: plan first, one reviewed artifact at a time, one pull request per milestone. Quality is judged against ISO/IEC 25010:2023 through the QC checklists. Code follows the `coding-conventions` and `clean-architecture` skills and `qc-programming-python`.

## Problem Statement

The course teaches the analysis in a Google Colab notebook. Such a notebook needs an online runtime, is hard to test, and is hard to browse as a repository. Jupyter is the format the course uses, so it stays, but run locally. Learners who share solutions need readable, runnable code that keeps the assignment's names.

## Business Opportunity

A plain Python package with tests and clear instructions lets coursists run and compare solutions, and lets visitors browse the repository for ideas. It also gives the Product Owner a worked example of the framework.

## Objectives

1. Provide a Jupyter notebook that follows the lecture steps in order, backed by one function per step in `src/`, named as in the assignment (head, shape, columns, dropna, max, idxmax, loc, spread, sort_values, groupby), also runnable from a command line.
2. Answer the five questions of the assignment from the PayScale data.
3. Cover every function with automated tests that pass offline.
4. Document how to create `.venv`, upgrade pip, install and run the project and its tests.
5. Provide a screenshot for each lecture step in the README and in the wiki.
6. Provide a wiki in English, Danish and Bahasa Malaysia that explains what each lecture step taught.
7. Publish a repository description and topics.

## Scope

### In Scope

- A Jupyter notebook in `notebooks/` that runs locally (JupyterLab) and is executed in the tests.
- Python 3.13 or newer package under `src/`, tests under `tests/`, `pyproject.toml`, Python `.gitignore`, venv instructions.
- Loading and cleaning `salaries_by_college_major.csv`, and all lecture steps and challenges of Day 72.
- README from the framework template, screenshots, wiki in three languages, repository description and topics.
- Local static analysis with opengrep before each push.

### Out of Scope

- The extra-credit web scraping of current PayScale data.
- Google Colab hosting.
- Charts, a web interface or any GUI.
- Publishing a package to PyPI.

## Expected Benefits

### Tangible Benefits

- A repository a coursist can clone and run in minutes.
- A tested solution for every lecture step.
- Documentation in three languages.

### Intangible Benefits

- Learners understand data exploration with pandas.
- A reusable example of the plan-first workflow.

## Strategic Alignment

The project supports the Product Owner's goal of completing the 100 Days of Code bootcamp with shareable, quality-checked solutions, and the framework's goal of a reviewed, traceable delivery.

## Success Criteria

| # | Criterion | Target | Measure |
| --- | --- | --- | --- |
| 1 | Lecture steps implemented | 10 of 10 | One function and one test per step |
| 2 | Tests pass | 100 percent, offline | `python -m pytest` exits 0 |
| 3 | Statement coverage of `src/` | at least 90 percent | pytest-cov report |
| 4 | Screenshots | one per lecture step in README and wiki | Count of images |
| 5 | Wiki languages | 3 languages, same page set | File list in `docs/wiki/` |
| 6 | Static analysis | 0 findings left open | opengrep run before push |
| 7 | Reviews | every artifact `Go` | `RC-*` records |

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| The dataset download link has expired | The analysis cannot run on the real data | Try the supplied link; if it fails, stop and ask S01 for the file |
| pandas is a runtime dependency although S03 wants none | A viewer must install one package | pandas is the subject of the assignment; it is the only runtime dependency, and JupyterLab is an optional extra, both stated in the README |
| Translations contain errors | Misleading wiki text | English is authoritative; translations follow page by page; S01 can challenge them |
| A token leaks into the repository | Security defect | `.env` is ignored, never read by project code, never printed |
| Screenshots drift from the code | Outdated documentation | A script regenerates them from the real output |

## Assumptions

- S01 is the Product Owner, developer and reviewer; the AI acts as stand-in reviewer (autonomous mode) and says so in every record.
- The dataset link in the assignment is valid on the day of the work.
- The git host accepts the tokens kept in the local `.env`.

## Constraints

- Python 3.13 or newer, `venv`, configuration in `pyproject.toml`.
- Folders `src/`, `tests/`, `docs/`.
- Jupyter is used for the notebook; runtime dependency is pandas only, Jupyter tools are an optional `notebook` extra.
- Product Owner languages: English and IT domain.
- Tokens come from `.env`, which is personal and never tested, imported or committed.
- Target date: 2026-11-18.

## Cost–Benefit Assessment

The assessment is qualitative on purpose: this is a personal learning project with no revenue, and the cost is the Product Owner's own time, so a monetary return would be invented precision.

| Costs | Benefits |
| --- | --- |
| About two days of AI-assisted effort and reviews | A tested, documented, trilingual example repository |
| Maintaining three wiki languages | Reach for English, Danish and Malay readers |

## Stakeholders

| Stakeholder ID (SA) | Interest in this project |
| --- | --- |
| S01 | Completes the assignment with quality and owns the result |
| S02 | Reads and runs the code and compares solutions |
| S03 | Browses the repository for ideas |

## Recommendation

Proceed — the scope is small, the data is public to course participants and every objective is checkable.

---

[SA-001]: ./stakeholder-analysis.md
[b409b30]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/commit/b409b30d933875a01860e78a6a26ccda86d6a9b3
