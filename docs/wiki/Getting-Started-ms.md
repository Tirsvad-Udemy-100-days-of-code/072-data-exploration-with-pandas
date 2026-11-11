[English](Getting-Started) · [Dansk](Getting-Started-da) · **Bahasa Malaysia**

# Bermula

Anda memerlukan Python 3.13 atau lebih baharu. Satu-satunya kebergantungan semasa larian ialah pandas; JupyterLab dan pytest ialah tambahan pilihan.

## Cipta persekitaran

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev,notebook]"
```

Pada Linux dan macOS gunakan `source .venv/bin/activate` sebagai ganti baris pengaktifan.

## Jalankan

```bash
python -m jupyter lab notebooks/day_72_data_exploration.ipynb
python -m college_majors
```

Arahan pertama membuka buku nota. Arahan kedua mencetak setiap langkah kuliah dalam terminal.

## Uji

```bash
python -m pytest --cov=college_majors
```

Ujian berjalan tanpa talian dan menjalankan buku nota dari awal hingga akhir.
