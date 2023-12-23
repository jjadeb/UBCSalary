# Visualizing UBC Salaries: Split by Gender, Department, and Job Title

An exercise in data wrangling, machine learning and data visualization.

The final Tableau dashboard can be found [here](https://public.tableau.com/views/UBCSalariesAllYears/Dashboard1?:language=en-US&:display_count=n&:origin=viz_share_link).

## Key Tools Used
- requests
- DBScan
- nltk
- Tableau

## Key Skills Learned
- Data Collecting
- Data Wrangling
- Data Visualization
- Machine Learning (clustering, natural language processing)

## Technologies
The project was made in Jupyter notebooks, using python.

## Data

Due to restrictions in distribution of faculty department and job title data, this analysis is not completely reproducible. That being said, below are instructions I can give to making sure the data is availible so that this project runs smoothly.

**For UBC Salary data**:

Other than running the code in UBCSalaries_ALL.ipynb, no additional work is needed to collect the UBC salary data. When the code is run it scrapes all salary data availible on this webpage: [https://finance.ubc.ca/reporting-planning-analysis/financial-reports](https://finance.ubc.ca/reporting-planning-analysis/financial-reports). This scraped data can be found in the data folder of this repository.

**For department/job title data**:

This data is not provided in a tabular format by the University of British Columbia. I collected this data on this website: [https://directory.ubc.ca/index.cfm](https://directory.ubc.ca/index.cfm) 
using the python requests package, but it is forbiden to distribute it publicly. Therefore, I will not be providing access to this data and this project is not completely reproducible.

**For gender training data**:

This data should already in the data folder but if it isn't it can be added by following these steps:

Go to the following link: [https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710014701](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710014701)
Download the data with the largest time period possible (1991-2021 chosen for this analysis).
Drop the csv data into the "data" folder and name it "17100147.csv".

Go to the following link: [https://www.kaggle.com/datasets/kaggle/us-baby-names/code](https://www.kaggle.com/datasets/kaggle/us-baby-names/code)
Download the kaggle data.
Drop the csv data into the "data" folder and name it "NationalNames.csv".

Go to the following link: [https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710014701](https://www.kaggle.com/datasets/ananysharma/indian-names-dataset)
Download the data.
Drop the male-names and female-names csv datasets into the "data" folder and name them "Indian-Male-Names.csv" and "Indian-Female-Names.csv" respectively.


Open up the final report (`UBCSalaries.ipynb`), install the necessary packages, then run all the cells.
