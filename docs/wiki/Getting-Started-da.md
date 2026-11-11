[English](Getting-Started) · **Dansk** · [Bahasa Malaysia](Getting-Started-ms)

# Kom i gang

Du skal bruge Python 3.13 eller nyere. Den eneste afhængighed ved kørsel er pandas; JupyterLab og pytest er valgfrie tillæg.

## Opret miljøet

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev,notebook]"
```

På Linux og macOS bruges `source .venv/bin/activate` i stedet for aktiveringslinjen.

## Kør

```bash
python -m jupyter lab notebooks/day_72_data_exploration.ipynb
python -m college_majors
```

Den første kommando åbner notebooken. Den anden udskriver hvert forelæsningstrin i terminalen.

## Test

```bash
python -m pytest --cov=college_majors
```

Testene kører offline og kører notebooken fra start til slut.
