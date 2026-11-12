[English](Getting-Started) · [Dansk](Getting-Started-da) · **Bahasa Malaysia**

# Bermula

Keperluan: Python 3.13 atau lebih baharu. Satu-satunya kebergantungan semasa larian ialah `pandas`; JupyterLab dan pytest ialah tambahan pilihan.

Cipta dan gunakan `.venv` tempatan.

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev,notebook]"
```

Linux dan macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev,notebook]"
```

Jalankan buku nota, baris arahan dan ujian:

```bash
python -m jupyter lab notebooks/day_72_data_exploration.ipynb
python -m college_majors
python -m pytest --cov=college_majors
```

**Apa yang anda dapat:** persediaan yang boleh diulang (satu persekitaran maya bagi setiap projek), pakej yang dipasang dalam mod boleh disunting, buku nota yang menjawab lima soalan, dan ujian yang membuktikan setiap jawapan.
