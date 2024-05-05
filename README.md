# Visualizing UBC Salaries: Split by Gender, Department, and Job Title

The aim of this project is to create an exploratory analysis of The University of British Columbia (UBC) faculty salaries based on guessed gender. A secondary goal is to make sure my analysis is reproducible and auditable.

Located in the reports directory, there is a [notebook](reports/UBC_salary_analysis.ipynb) that contains a record of the original data wrangling steps of this project. This original analysis contained department and job title information of staff memebrs, and the final exploratory analysis is displayed as a [tableau dashboard](https://public.tableau.com/views/2023UBCSalariesJobTitleDepartmentandGuessedGender/Dashboard1?:language=en-US&:sid=&:display_count=n&:origin=viz_share_link). However, due to copyright the [department and job title data](https://www.directory.ubc.ca/index.cfm) and the scraping script used to obtain the data are not permitted to be published in this repository. Therefore, for the sake of reproducibility, I narrowed my scope to focus on the relationship between staff salaries and guessed genders of staff members.

To prioritize learning, rather than directly requesting salary data from UBC by department and gender, I will rely on the [annual PDF](https://finance.ubc.ca/reporting-planning-analysis/financial-reports) of salary data released by UBC, along with global baby name datasets. To learn more about the sources of the datasets, visit the [data](data) folder.

The project involves several steps: gathering and cleaning salary data, making staff gender predictions using large babyname datasets, using a machine learning model to guess remaining genders, and ultimately visualizing the cleaned data.

This approach incorporates tasks such as scraping, clustering, and data transformation, offering an in-depth exploration of data manipulation techniques and fostering a comprehensive understanding of the intricacies involved in data wrangling.

# Ethics



## Running the Analysis in a Reprodicible Environment

**IMPORTANT NOTE:** This analysis is not completely reproducible (see [Data](#data) for more details).

There are two options for running my analysis in a reproducible environment. You can use the `environment.yml` file or use Docker. The `environment.yml` file is a lighter-weight option compared to Docker. 

### environment.yml

Ensure that [conda](https://docs.anaconda.com/free/miniconda/miniconda-install/) and [nb_conda_kernels](https://github.com/Anaconda-Platform/nb_conda_kernels) are installed on your machine.

[Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) this repository, and **navigate to the root of the repository** in a terminal window. Then, run the following from the root of this repository:

```{bash}
conda env create --file environment.yml
```

```{bash}
conda activate ubcsalary
```

To create a kernel for Jupyter Lab run:

```{bash}
python -Xfrozen_modules=off -m ipykernel install --user --name=ubcsalaryenv
```

Then run the following from the root of this repository:

```{bash}
jupyter lab
```

Open `reports/UBC_salary_analysis.ipynb` in Jupyter Lab and navigate to `Kernel` >>> `Change Kernel...` and choose `ubcsalaryenv` from the dropdown menu.

Next, to run the analysis, under the "Kernel" menu click "Restart Kernel and Run All Cells...".

### Docker

Docker is a tool that can be used to run my analysis in a reproducible environment. Build a Docker container by following these steps:

**Setup**

1. First, ensure you have [Docker](https://www.docker.com/products/docker-desktop/) installed and running on your machine.
2. [Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) this repository, and **navigate to the root of the repository** in a terminal window.

Run the following commands in the terminal to build and start the container. These commands activate the commands specified in [docker-compose.yml](docker-compose.yml).

```bash
docker-compose pull
```
```bash
docker-compose up
```
After launching the Docker Container, in the terminal look for a URL that starts with http://127.0.0.1:8888/lab?token= . Copy and paste that URL into your browser.

You should now see the Jupyter lab IDE in your browser, with all the project files visible in the file browser pane on the left side of the screen.

To run the analysis, open `reports/UBC_salary_analysis.ipynb` in Jupyter Lab and under the "Kernel" menu click "Restart Kernel and Run All Cells...".

Stop the Docker container by first typing `Cntrl + C`in the terminal where you launched the container, and then run the following command:

```
docker-compose rm
```

## Key Skills Learned
- Data Collecting
- Data Wrangling
- Data Visualization
- Machine Learning (clustering, natural language processing)

## License

The UBC Salary Analysis report contained herein is licensed under the
[Creative Commons Attribution 4.0 International (CC BY 4.0) License](https://creativecommons.org/licenses/by/4.0/legalcode).
See [the license file](LICENSE.md) for more information. If
re-using/re-mixing please provide attribution and link to this webpage.
The software code contained within this repository is licensed under the
MIT license. See [the license file](LICENSE.md) for more information.
