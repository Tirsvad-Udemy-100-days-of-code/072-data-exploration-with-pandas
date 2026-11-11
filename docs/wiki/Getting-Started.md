**English** · [Dansk](Getting-Started-da) · [Bahasa Melayu](Getting-Started-ms)

# Getting started

You need Python 3.13 or newer. The only runtime dependency is pandas; JupyterLab and pytest are optional extras.

## Create the environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev,notebook]"
```

On Linux and macOS use `source .venv/bin/activate` instead of the activation line.

## Run

```bash
python -m jupyter lab notebooks/day_72_data_exploration.ipynb
python -m college_majors
```

The first command opens the notebook. The second prints every lecture step in the terminal.

## Test

```bash
python -m pytest --cov=college_majors
```

The tests run offline and execute the notebook end to end.
