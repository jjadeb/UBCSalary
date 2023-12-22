# Visualizing UBC Salaries: Split by Gender, Department, and Job Title

An exercise in data wrangling, machine learning and data visualization.

The final Tableau dashboard can be found [here](https://public.tableau.com/views/UBCSalary/Dashboard1?:language=en-US&:display_count=n&:origin=viz_share_link).

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

## Setup

Due to restrictions in distribution of faculty department and job title data, this analysis is not completely reproducible. That being said, below are all the instructions I can give on how to make the project run smoothly.

**For UBC Salary data**:

Data from 2022 is already in the data folder. However, you can update the analysis with more recent data by following these instructions:
Go to the following link: [https://finance.ubc.ca/reporting-planning-analysis/financial-reports](https://finance.ubc.ca/reporting-planning-analysis/financial-reports). 
Open the most recent Financial Information Act Report, and click Control + A to copy the contents of the pdf. 
Paste the contents into a text file and then upload the file into the "data" folder. Name it "UBC Staff Salary.txt".

**For department/job title data**:

This data is not provided in a tabular format by the University of British Columbia. I collected this data on this website: [https://directory.ubc.ca/index.cfm](https://directory.ubc.ca/index.cfm) 
using the python requests package, but it is forbiden to distribute it publicly. Therefore, I will not be providing access to this data and this project is not completely reproducible.

**For gender training data**:

This data is not already in the data folder as it was too large to upload to GitHub.

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
