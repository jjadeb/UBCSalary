# Visualizing UBC Salaries: Split by Gender, Department, and Job Title

An exercise in data wrangling, machine learning and data visualization.

The final Tableau dashboard can be found [here](https://public.tableau.com/views/UBCSalariesAllYears/Dashboard1?:language=en-US&:display_count=n&:origin=viz_share_link).

Please feel free to add suggestions or point out bugs in the issues tab!

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

Due to restrictions in distribution of faculty department and job title data, this analysis is not completely reproducible. That being said, below are details about the different data sources used in this project.

**For UBC Salary data**:

Other than running the code in UBCSalaries_ALL.ipynb, no additional work is needed to collect the UBC salary data. When the code is run it scrapes all salary data availible on this webpage: [https://finance.ubc.ca/reporting-planning-analysis/financial-reports](https://finance.ubc.ca/reporting-planning-analysis/financial-reports). This scraped data can be found in the data folder of this repository.

**For department/job title data**:

I collected this data on this website: [https://directory.ubc.ca/index.cfm](https://directory.ubc.ca/index.cfm) 
using the python requests package, but it is forbiden for me to distribute it publicly. Therefore, I will not be providing access to this data. However, position data is publicly available through the Vancouver Sun here: https://github.com/vs-postmedia/public-sector-salary-data. I chose not to use this dataset in order to learn more about scraping and data cleaning.


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
