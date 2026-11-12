**English** · [Dansk](Lecture-Steps-da) · [Bahasa Malaysia](Lecture-Steps-ms)

# Lecture steps

Each step below matches a section of the notebook `notebooks/day_72_data_exploration.ipynb` and a function in `college_majors.application.lecture_steps`. The images are taken from the executed notebook.

## Step 1: Read the .csv file and look at the first rows

![Step 1](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-01.png)

**What we gained:** `pd.read_csv` loads a file into a DataFrame, and `df.head()` shows the first five rows. This is always the first look at a new dataset.

## Step 2: Shape and column names

![Step 2](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-02.png)

**What we gained:** `df.shape` tells us there are 51 rows and 6 columns, and `df.columns` gives the column names we use later.

## Step 3: Missing values

![Step 3](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-03.png)

**What we gained:** `df.isna()` marks every NaN cell. The last row is a source note with blank values, which is junk data.

## Step 4: Clean the data

![Step 4](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-04.png)

**What we gained:** `df.dropna()` returns a new DataFrame without the junk row, leaving 50 majors. The original stays unchanged.

## Step 5: Highest starting salary

![Step 5](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-05.png)

**What we gained:** A column is selected with square brackets. `max()` gives the value, `idxmax()` gives the row index and `.loc` looks up the major: Physician Assistant at 74,300.

## Step 6: Highest mid-career salary and the lowest earners

![Step 6](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-06.png)

**What we gained:** The same tools with `min()` and `idxmin()` answer the challenge: Chemical Engineering has the highest mid-career salary (107,000), Spanish the lowest starting salary (34,000) and Education the lowest mid-career salary (52,000).

## Step 7: Spread and the lowest-risk majors

![Step 7](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-07.png)

**What we gained:** Columns support arithmetic, so the 90th minus the 10th percentile gives a Spread. `insert` adds it as a new column and `sort_values` ranks it. Nursing has the smallest spread, so it is the lowest-risk major.

## Step 8: Highest potential and greatest spread

![Step 8](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-08.png)

**What we gained:** `sort_values(..., ascending=False)` ranks from high to low. Economics, Finance and Math appear in both rankings: some graduates earn very much, others do not.

## Step 9: Group by category

![Step 9](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-09.png)

**What we gained:** `groupby('Group')` works like an Excel pivot table. Counting shows 12 Business, 22 HASS and 16 STEM majors.

## Step 10: Average salary by group

![Step 10](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-10.png)

**What we gained:** `.mean()` on the groups answers the last question: STEM earns most on average, then Business, then HASS. A number format with two decimals makes the table readable.

## Step 11: Answers to the five questions

![Step 11](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/raw/branch/main/docs/images/step-11.png)

**What we gained:** `answer_five_questions` collects every result. Highest starting salaries: Physician Assistant, then the engineering majors. Lowest earnings: Spanish, Religion and Education. Highest potential: Economics, Finance and Chemical Engineering. Lowest risk: Nursing. On average STEM earns most, then Business, then HASS.
