<!-- README built from framework/templates/README-template.md -->

# 🚀 Day 72: Data Exploration with Pandas

A Jupyter notebook and a small, tested Python package that explore the PayScale post-university salary data by college major, from Udemy's *100 Days of Code: The Complete Python Pro Bootcamp*. It is for coursists who want to run and compare solutions, and for visitors who browse for ideas.

## 📚 Table of Contents

- [Overview](#-overview)
- [Requirements](#-requirements)
- [Setup](#-setup)
- [Run](#-run)
- [Tests](#-tests)
- [License](#-license)
- [Links](#-links)
- [Appendix: Project documents](#-appendix-project-documents)

## 🧭 Overview

Do college degrees pay you back? The notebook answers five questions with pandas: which degrees have the highest starting salaries, which majors earn least, which have the highest earning potential, which are the lowest risk, and whether Business, STEM or HASS degrees earn more on average.

| Folder | What it holds |
| --- | --- |
| `notebooks/` | `day_72_data_exploration.ipynb`, the lecture steps in order, with outputs |
| `src/college_majors/` | The tested functions, one per lecture step (clean architecture layers) |
| `src/college_majors/data/` | `salaries_by_college_major.csv` (source: PayScale Inc., via the course) |
| `tests/` | Unit, integration and end-to-end tests; the notebook is executed in a test |
| `docs/` | Project documents and the wiki (English, Danish, Bahasa Malaysia) |

Function names follow the assignment:

| Lecture step | Function |
| --- | --- |
| `df.head()`, `df.tail()` | `head`, `tail` |
| `df.shape`, `df.columns` | `shape`, `columns` |
| `df.isna()` | `missing_values` |
| `df.dropna()` | `clean` |
| `max`, `idxmax`, `loc` | `highest_starting_salary`, `highest_mid_career_salary` |
| `min`, `idxmin` | `lowest_starting_salary`, `lowest_mid_career_salary` |
| `insert` (Spread column) | `add_spread` |
| `sort_values` | `lowest_risk_majors`, `highest_potential_majors`, `greatest_spread_majors` |
| `groupby` | `majors_per_group`, `average_salary_by_group` |

## 📋 Requirements

- Python 3.13 or newer.
- `pandas`, the only runtime dependency.
- Optional, for the notebook: JupyterLab (the `notebook` extra). Optional, for the tests: pytest (the `dev` extra).

## 🛠️ Setup

Create a local virtual environment named `.venv`, upgrade pip, and install the project.

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev,notebook]"
```

Linux and macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev,notebook]"
```

Install only `pip install -e .` if you want the package without Jupyter and pytest.

## ▶️ Run

Open the notebook in JupyterLab:

```bash
python -m jupyter lab notebooks/day_72_data_exploration.ipynb
```

Or print every lecture step in the terminal:

```bash
python -m college_majors
```

## 🧪 Tests

```bash
python -m pytest --cov=college_majors
```

The tests run offline and execute the notebook end to end.

## 📄 License

GNU Affero General Public License v3, see [LICENSE][license].

## 🔗 Links

- [Repository][repository]
- [Documentation][documentation]
- [Issue tracker][issues]

## 📎 Appendix: Project documents

The documents a newcomer needs, in reading order.

| Document | What it tells you |
| --- | --- |
| [Business Case][BC-001] | Why the project exists, its scope and success criteria |
| [Stakeholder Analysis][SA-001] | Who is involved; the stakeholder IDs used for owners and reviewers |
| [Project Plan][PP-001] | The gateways and their schedule |
| [Milestones][milestones] | One document per gateway: Go/No-Go criteria and tasks |
| [Artifact registry][registry] | Where each artifact type lives, the next version, the PO language and domain |
| [Domain dictionary][DICT-001] | The PO terms and the IT terms |
| [Traceability matrix][TM-001] | How the artifacts link and when each was last reviewed |
| [Framework README][framework-readme] | The framework this project uses |
| [Framework changelog][framework-changelog] | What changed in each framework release |

---

[license]: ./LICENSE
[repository]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas
[documentation]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/wiki
[issues]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/issues
[BC-001]: ./docs/business-case.md
[SA-001]: ./docs/stakeholder-analysis.md
[PP-001]: ./docs/project-plan.md
[milestones]: ./docs/milestones/
[registry]: ./docs/artifact-registry.md
[DICT-001]: ./docs/dictionary.md
[TM-001]: ./docs/sqa/traceability-matrix.md
[framework-readme]: ./framework/README.md
[framework-changelog]: ./framework/CHANGELOG.md
