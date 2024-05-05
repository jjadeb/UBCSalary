# Visualizing UBC Salaries Split by Gender

The aim of this project is to create an exploratory analysis of The University of British Columbia (UBC) faculty salaries based on guessed gender. A secondary goal is to make sure my analysis is reproducible and auditable.

To prioritize learning, rather than directly requesting salary data from UBC by department and gender, I will rely on the [annual PDF](https://finance.ubc.ca/reporting-planning-analysis/financial-reports) of salary data released by UBC, along with global baby name datasets. To learn more about the sources of the datasets, visit the [data](data) folder.

The project involves several steps: gathering and cleaning salary data, making staff gender predictions using large babyname datasets, using a machine learning model to guess remaining genders, and visualizing the cleaned data.

## Table Of Contents  
- [Project History](#project-history)
- [Ethics](#ethics)
- [Reprodicible Environment](#reprodicible-environment)
- [Developer Notes](#developer-notes)
- [Key Skills Learned](#key-skills-learned)
- [Dependencies](#dependencies)
- [License](#license)


## Project History 

The final phase of this project, a report detailing the analysis, is a work in progress. For now, you can see the plots created for the analysis in the [plots directory](plots). 

The most up-to-date analysis code is located in the [scripts](scripts) folder.

Located in the reports directory, there is a [notebook](reports/UBC_salary_analysis.ipynb) that contains a record of the original data wrangling steps of this project. This original analysis contained department and job title data for staff memebrs, and the final exploratory analysis is displayed as a [tableau dashboard](https://public.tableau.com/views/2023UBCSalariesJobTitleDepartmentandGuessedGender/Dashboard1?:language=en-US&:sid=&:display_count=n&:origin=viz_share_link). Due to UBC's copyright, the [department and job title data](https://www.directory.ubc.ca/index.cfm) and the scraping script used to obtain the data are not permitted to be published in this repository. So, the original report is not reproducible. Therefore, for the sake of reproducibility, I removed the use of department and job title data and focused on the relationship between staff salaries and guessed genders of staff members. 

## Ethics

In this project first names are used to guess whether someone is "male" or "female". I acknowledge that gender identity is a spectrum and not limited to binary categories. Misgendering, or incorrectly assigning gender to individuals, can have harmful effects and perpetuate stereotypes. While first names can sometimes be an indication of someones gender, first names are not inherintly gendered. 

I encourage anyone who notices a misgendering within this project to raise an issue in the issues tab, and it will be corrected. In addition, I encourage respectful and inclusive language in all discussions related to gender. 

Please refer to the [Code of Conduct](CODE_OF_CONDUCT.md) for further details on the inclusive standards of this project. Your cooperation in fostering an inclusive environment is greatly appreciated.


## Reprodicible Environment

There are two options for running my analysis in a reproducible environment. You can use the `environment.yml` file or use Docker. The `environment.yml` file is a lighter-weight option compared to Docker. 

### environment.yml

Ensure that [conda](https://docs.anaconda.com/free/miniconda/miniconda-install/) is installed on your machine.

[Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) this repository, and **navigate to the root of the repository** in a terminal window. Then, run the following commands from the root of this repository:

```{bash}
conda env create --file environment.yml
```

```{bash}
conda activate ubcsalary
```

Run the following command to reset the project to a clean state (i.e., remove all files generated by previous runs of the analysis):

```{bash}
make clean
```
To run the analysis in its entirety, run the following command:

```{bash}
make all
```

### Docker

Docker is a tool that can be used to run my analysis in a reproducible environment. Build a Docker container by following these steps:

**Setup**

1. First, ensure you have [Docker](https://www.docker.com/products/docker-desktop/) installed and running on your machine.
2. [Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) this repository, and **navigate to the root of the repository** in a terminal window.

Run the following command in the terminal to pull the latest version of the Docker Image.

```bash
docker-compose pull
```
Run the following command to reset the project to a clean state (i.e., remove all files generated by previous runs of the analysis):

```bash
docker-compose run --rm ubcsalaryimg make clean
```

To run the analysis in its entirety, enter the following command in the terminal:

```bash
docker-compose run --rm ubcsalaryimg make all
```

Some instructions have been borrowed from [this repository](https://github.com/ttimbers/breast_cancer_predictor_py).

## Developer Notes

### Working with the project in the container using Jupyter lab

Navigate to the root of this project on your computer using the command line and enter the following command:

```{bash}
docker-compose up
```

In the terminal, look for a URL that starts with http://127.0.0.1:8888/lab?token= . Copy and paste that URL into your browser.

You should now see the Jupyter lab IDE in your browser, with all the project files visible in the file browser pane on the left side of the screen.

To shut down the container and clean up the resources, type Cntrl + C in the terminal where you launched the container, and then type

```{bash}
docker compose rm
```

### Working with the project in the container using VSCode
Note if you prefer to work in VS Code, you can run the following from the root of the project in a terminal in VS Code to launch the container in the terminal there:

```{bash}
docker compose run --rm terminal bash
```

To exit the container type exit in the terminal.

Some instructions have been borrowed from [this repository](https://github.com/ttimbers/breast_cancer_predictor_py)

## Key Skills Learned
- Reproducibility in Data Science
- Data Collecting
- Data Wrangling
- Data Visualization
- Machine Learning (natural language processing)

## Dependencies

Docker is a container solution used to manage the software dependencies for this project. The Docker image used for this project is based on the quay.io/jupyter/minimal-notebook:aarch64-ubuntu-22.04 image. Additional dependencies are specified int the [Dockerfile](Dockerfile).

## License

The UBC Salary Analysis report contained herein is licensed under the
[Creative Commons Attribution 4.0 International (CC BY 4.0) License](https://creativecommons.org/licenses/by/4.0/legalcode).
See [the license file](LICENSE.md) for more information. If
re-using/re-mixing please provide attribution and link to this webpage.
The software code contained within this repository is licensed under the
MIT license. See [the license file](LICENSE.md) for more information.
