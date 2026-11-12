[English](Learning-Points) · [Dansk](Learning-Points-da) · **Bahasa Malaysia**

# Perkara yang dipelajari

| Alat | Fungsi |
| --- | --- |
| `head()`, `tail()`, `shape`, `columns` | Meneroka DataFrame: baris pertama dan terakhir, saiz dan nama lajur |
| `isna()`, `dropna()` | Mencari nilai NaN dan membuang baris yang tiada data |
| `df['column']`, `df[['a', 'b']]` | Memilih satu atau beberapa lajur |
| `.loc[index]` | Membaca satu baris atau satu sel |
| `max()`, `min()`, `idxmax()`, `idxmin()` | Mencari nilai terbesar dan terkecil serta kedudukannya |
| `sort_values()`, `insert()` | Menyusun jadual dan menambah lajur yang dikira |
| `groupby()` | Mengumpulkan baris mengikut kategori, seperti jadual pangsi Excel |

## Apa yang data beritahu kita

- Education dan Spanish berpendapatan paling rendah; Physician Assistant bermula paling tinggi.
- Nursing ialah jurusan paling rendah risikonya; Economics dan Finance mempunyai sebaran terbesar.
- Secara purata STEM berpendapatan paling tinggi, kemudian Business, kemudian HASS.

Data ini dari tahun 2008 dan melihat sepuluh tahun sebelumnya, jadi kedudukan tinggi Finance mungkin telah berubah sejak krisis kewangan.

Kemas kini: data PayScale yang lebih baharu (syot kilat 2020, lihat langkah 12) menunjukkan kedudukan sebahagian besarnya kekal, dan Finance jatuh dari kedudukan 14 daripada 50 ke 169 daripada 350.
