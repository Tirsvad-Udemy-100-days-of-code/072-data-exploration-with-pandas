[English](Lecture-Steps) · [Dansk](Lecture-Steps-da) · **Bahasa Malaysia**

# Langkah kuliah

Setiap langkah di bawah sepadan dengan satu bahagian dalam buku nota `notebooks/day_72_data_exploration.ipynb` dan satu fungsi dalam `college_majors.application.lecture_steps`. Imej diambil daripada buku nota yang telah dijalankan.

## Langkah 1: Baca fail .csv dan lihat baris pertama

![Step 1](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-01.png)

**Apa yang kita pelajari:** `pd.read_csv` memuatkan fail ke dalam DataFrame, dan `df.head()` menunjukkan lima baris pertama. Ini sentiasa pandangan pertama pada set data baharu.

## Langkah 2: Bentuk dan nama lajur

![Step 2](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-02.png)

**Apa yang kita pelajari:** `df.shape` menunjukkan 51 baris dan 6 lajur, dan `df.columns` memberi nama lajur yang kita gunakan kemudian.

## Langkah 3: Nilai yang hilang

![Step 3](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-03.png)

**Apa yang kita pelajari:** `df.isna()` menandakan setiap sel NaN. Baris terakhir ialah nota sumber dengan nilai kosong, iaitu data sampah.

## Langkah 4: Bersihkan data

![Step 4](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-04.png)

**Apa yang kita pelajari:** `df.dropna()` memulangkan DataFrame baharu tanpa baris sampah itu, meninggalkan 50 jurusan. Yang asal tidak berubah.

## Langkah 5: Gaji permulaan tertinggi

![Step 5](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-05.png)

**Apa yang kita pelajari:** Lajur dipilih dengan kurungan siku. `max()` memberi nilai, `idxmax()` memberi indeks baris dan `.loc` mencari jurusan: Physician Assistant pada 74,300.

## Langkah 6: Gaji pertengahan kerjaya tertinggi dan pendapatan terendah

![Step 6](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-06.png)

**Apa yang kita pelajari:** Alat yang sama dengan `min()` dan `idxmin()` menjawab cabaran: Chemical Engineering mempunyai gaji pertengahan kerjaya tertinggi (107,000), Spanish gaji permulaan terendah (34,000) dan Education gaji pertengahan kerjaya terendah (52,000).

## Langkah 7: Sebaran dan jurusan paling rendah risiko

![Step 7](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-07.png)

**Apa yang kita pelajari:** Lajur boleh dikira, jadi persentil ke-90 tolak ke-10 memberi Spread. `insert` menambahnya sebagai lajur baharu dan `sort_values` menyusunnya. Nursing mempunyai sebaran terkecil, jadi ia jurusan paling rendah risiko.

## Langkah 8: Potensi tertinggi dan sebaran terbesar

![Step 8](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-08.png)

**Apa yang kita pelajari:** `sort_values(..., ascending=False)` menyusun daripada tinggi ke rendah. Economics, Finance dan Math muncul dalam kedua-dua kedudukan: sesetengah graduan berpendapatan sangat tinggi, yang lain tidak.

## Langkah 9: Kumpul mengikut kategori

![Step 9](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-09.png)

**Apa yang kita pelajari:** `groupby('Group')` berfungsi seperti jadual pangsi Excel. Pengiraan menunjukkan 12 jurusan Business, 22 HASS dan 16 STEM.

## Langkah 10: Gaji purata mengikut kumpulan

![Step 10](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-10.png)

**Apa yang kita pelajari:** `.mean()` pada kumpulan menjawab soalan terakhir: STEM berpendapatan paling tinggi secara purata, kemudian Business, kemudian HASS. Format nombor dengan dua tempat perpuluhan menjadikan jadual mudah dibaca.
