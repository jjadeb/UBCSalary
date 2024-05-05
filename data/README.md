## Data

There are three main folders in this directory: salary data, gender corpus, and gender predictions. The salary data and gender prediction folders should be empty when the analysis is run as those folders will be populated throughout the analysis. However, 

**salary_data**:

Other than running the analysis, no additional work is needed to collect the UBC salary data. When the code is run it scrapes all salary data availible on this webpage: [https://finance.ubc.ca/reporting-planning-analysis/financial-reports](https://finance.ubc.ca/reporting-planning-analysis/financial-reports)

**gender_predictions**:

This folder is populated when the analysis is run. 

**gender_corpus**:

The gender corpus folder should have four files in it before the analysis is run. These files are babyname data files from various sources, used to train the gender classifier. 

This data should already in the `data/gender_corpus` folder but if it isn't it can be added by following these steps:

Go to the following link: [https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710014701](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710014701)
Download the data in the year range 1991-2021.
Drop the csv data into the `data/gender_corpus` folder and name it "canadian_babyname.csv".

Go to the following link: [https://www.kaggle.com/datasets/kaggle/us-baby-names/code](https://www.kaggle.com/datasets/kaggle/us-baby-names/code)
Download the kaggle data.
Drop the csv data into the `data/gender_corpus` folder and name it "american_babyname.csv".

Go to the following link: [https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710014701](https://www.kaggle.com/datasets/ananysharma/indian-names-dataset)
Download the data.
Drop the male-names and female-names csv datasets into the `data/gender_corpus` folder and name them "Indian-Male-Names.csv" and "Indian-Female-Names.csv" respectively.
