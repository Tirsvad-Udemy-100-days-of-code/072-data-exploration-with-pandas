[English](Lecture-Steps) · **Dansk** · [Bahasa Malaysia](Lecture-Steps-ms)

# Forelæsningstrin

Hvert trin nedenfor svarer til et afsnit i notebooken `notebooks/day_72_data_exploration.ipynb` og en funktion i `college_majors.application.lecture_steps`. Billederne er taget fra den kørte notebook.

## Trin 1: Læs .csv-filen og se de første rækker

![Step 1](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-01.png)

**Det lærte vi:** `pd.read_csv` indlæser en fil i en DataFrame, og `df.head()` viser de første fem rækker. Det er altid det første blik på et nyt datasæt.

## Trin 2: Form og kolonnenavne

![Step 2](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-02.png)

**Det lærte vi:** `df.shape` viser 51 rækker og 6 kolonner, og `df.columns` giver de kolonnenavne, vi bruger senere.

## Trin 3: Manglende værdier

![Step 3](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-03.png)

**Det lærte vi:** `df.isna()` markerer hver NaN-celle. Den sidste række er en kildenote med tomme værdier, altså ubrugelige data.

## Trin 4: Ryd op i dataene

![Step 4](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-04.png)

**Det lærte vi:** `df.dropna()` returnerer en ny DataFrame uden den ubrugelige række, så der er 50 studieretninger tilbage. Originalen er uændret.

## Trin 5: Højeste startløn

![Step 5](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-05.png)

**Det lærte vi:** En kolonne vælges med kantede parenteser. `max()` giver værdien, `idxmax()` giver rækkeindekset, og `.loc` slår studieretningen op: Physician Assistant med 74.300.

## Trin 6: Højeste løn midt i karrieren og de lavest lønnede

![Step 6](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-06.png)

**Det lærte vi:** De samme værktøjer med `min()` og `idxmin()` besvarer udfordringen: Chemical Engineering har den højeste løn midt i karrieren (107.000), Spanish den laveste startløn (34.000), og Education den laveste løn midt i karrieren (52.000).

## Trin 7: Spredning og studieretninger med lavest risiko

![Step 7](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-07.png)

**Det lærte vi:** Kolonner kan regnes med, så 90. minus 10. percentil giver en Spread. `insert` tilføjer den som ny kolonne, og `sort_values` rangerer den. Nursing har den mindste spredning og er derfor den studieretning med lavest risiko.

## Trin 8: Højeste potentiale og største spredning

![Step 8](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-08.png)

**Det lærte vi:** `sort_values(..., ascending=False)` rangerer fra høj til lav. Economics, Finance og Math optræder i begge rangeringer: nogle uddannede tjener meget, andre gør ikke.

## Trin 9: Gruppér efter kategori

![Step 9](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-09.png)

**Det lærte vi:** `groupby('Group')` virker som en pivottabel i Excel. Optælling viser 12 Business-, 22 HASS- og 16 STEM-studieretninger.

## Trin 10: Gennemsnitsløn pr. gruppe

![Step 10](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-10.png)

**Det lærte vi:** `.mean()` på grupperne besvarer det sidste spørgsmål: STEM tjener mest i gennemsnit, derefter Business og til sidst HASS. Et talformat med to decimaler gør tabellen læsbar.

## Trin 11: Svar på de fem spørgsmål

![Step 11](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-11.png)

**Det lærte vi:** `answer_five_questions` samler alle resultater. Højeste startløn: Physician Assistant, derefter ingeniørstudierne. Laveste indtjening: Spanish, Religion og Education. Højeste potentiale: Economics, Finance og Chemical Engineering. Lavest risiko: Nursing. I gennemsnit tjener STEM mest, derefter Business og til sidst HASS.
