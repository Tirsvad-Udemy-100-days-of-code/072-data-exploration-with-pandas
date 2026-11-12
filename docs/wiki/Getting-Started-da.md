[English](Getting-Started) · **Dansk** · [Bahasa Malaysia](Getting-Started-ms)

# Kom i gang

Krav: Python 3.13 eller nyere. Den eneste afhængighed ved kørsel er `pandas`; JupyterLab og pytest er valgfrie tillæg.

Opret og brug et lokalt `.venv`.

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev,notebook]"
```

Linux og macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev,notebook]"
```

Kør notebooken, kommandolinjen og testene:

```bash
python -m jupyter lab notebooks/day_72_data_exploration.ipynb
python -m college_majors
python -m pytest --cov=college_majors
```

**Det får du:** en gentagelig opsætning (et virtuelt miljø pr. projekt), en pakke installeret i redigerbar tilstand, en notebook der besvarer de fem spørgsmål, og tests der beviser hvert svar.
