# Review of Python source (full MIL-002 scope)

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-009 |
| CrossReference | [PY-001], [QC-PY-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-11 | Proposed | Jens Tirsvad Nielsen | AI as stand-in for S02 | Initial version | [2bb83ad] |

---

## Artifact Under Review

- Instance reviewed: [PY-001]
- Checklist used: [QC-PY-001]
- Scope: full review of the final code (all lecture steps, command line, notebook test); delta re-review of [RC-008] scope: no earlier criterion changed
- Language and domain: n/a (technical type)
- Language reviewer: none (the stand-in reads English and knows the IT domain)
- Mode: autonomous, not independent (`AI as stand-in for S02`)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | ruff N rules pass; snake_case, PascalCase and UPPER_SNAKE used. |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | Names state purpose in domain words (highest_starting_salary, drop_missing). |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff format --check` and `ruff check` (E, F, I, B, UP, N, D, ANN, S) pass; config in pyproject.toml. |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | All functions annotated, including -> None; ANN rules pass in src. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | No bare except and no swallowed exceptions (B and E rules pass). |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No mutable defaults; no builtin is shadowed (max, min are not redefined). |
| 7 | Files, locks and connections are managed with context managers | Pass | No files opened by hand; pandas and importlib.resources manage the file. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | Docstrings on every public module, class and function (D rules pass). |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | No logging and no secrets; the CLI writes program output to a TextIO, not to logs. |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | N-A | No Design Class Diagram exists; the tasks are plain technical tasks in the milestone. |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | Tests named for behaviour, offline and order-independent; 41 tests incl. the notebook executed with nbclient and the command line end to end; 100 percent line coverage. |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | N-A | Optional; no type checker is configured. Annotations are complete. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | Dependencies declared in pyproject.toml, none unused; lower bounds, not exact pins (optional criterion). |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | Column names defined once in domain/salaries.py; Spread rule defined once. |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | domain imports nothing from the project; application imports domain; presentation imports both. Deviation: pandas DataFrames are used in domain and application because the assignment is about pandas; recorded here as a justified deviation. |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | Small functions with one reason to change; no type switches; no inheritance. |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | Layers domain, application, infrastructure, presentation under src/college_majors; tests/unit, tests/integration, tests/e2e. |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | File and folder names are English, lowercase, with letters, digits, underscore and dot only. |

## Overall Verdict

Go — no Mandatory criterion fails (full MIL-002 scope); the stand-in review is not independent and stays open to challenge by S01.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| none | - | - |

---

[PY-001]: ../../../src/college_majors
[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
[2bb83ad]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/commit/2bb83adc72257dc905f624715ad925b578e08d8f
