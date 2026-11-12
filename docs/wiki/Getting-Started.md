**English** · [Dansk](Getting-Started-da) · [Bahasa Malaysia](Getting-Started-ms)

# Getting started

Requirements: Python 3.13 or newer. The only runtime dependency is `pandas`; JupyterLab and pytest are optional extras.

Create and use a local `.venv`.

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

Run the notebook, the command line and the tests:

```bash
python -m jupyter lab notebooks/day_72_data_exploration.ipynb
python -m college_majors
python -m pytest --cov=college_majors
```

**What you gain:** a repeatable set-up (a virtual environment per project), a package you install in editable mode, a notebook that answers the five questions, and tests that prove each answer.
