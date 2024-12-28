# Visualizing UBC Salaries Split by Gender

The aim of this project is to create an exploratory analysis of The University of British Columbia (UBC) staff salaries based on guessed gender. A secondary goal is to make sure my analysis is reproducible.

The project involves several steps: gathering and cleaning salary data, making staff gender predictions using large babyname datasets and a machine learning model, and visualizing the cleaned data.

To make sure the analysis is up to date, please follow the instructions in [Running the Analysis](#running-the-analysis). If you don't care if the analysis is up to date, you can read the report from Dec 28th, 2024 [here](https://github.com/jjadeb/UBCSalary/blob/main/reports/UBC_salary_report.pdf).

## Table Of Contents  

- [Running the Analysis](#running-the-analysis)
- [Developer Notes](#developer-notes)
- [Ethics](#ethics)
- [Key Skills Learned](#key-skills-learned)
- [Dependencies](#dependencies)
- [License](#license)

## Running the Analysis

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

You can find the created report at the following path: `reports/UBC_salary_report.pdf`.

### Docker

Docker is a tool that can be used to run my analysis in a reproducible environment. Build a Docker container by following these steps:

#### Setup

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

You can find the created report at the following path: `reports/UBC_salary_report.pdf`.

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
docker-compose rm
```

Some instructions have been borrowed from [this repository](https://github.com/ttimbers/breast_cancer_predictor_py)

## Ethics

In this project first names are used to guess whether someone is "male" or "female". I acknowledge that gender identity is a spectrum and not limited to binary categories. Misgendering, or incorrectly assigning gender to individuals, can have harmful effects and perpetuate stereotypes. While first names can sometimes be an indication of someones gender, first names are not inherintly gendered. 

I encourage anyone who notices a misgendering within this project to raise an issue in the issues tab, and it will be corrected. In addition, I encourage respectful and inclusive language in all discussions related to gender.

Please refer to the [Code of Conduct](CODE_OF_CONDUCT.md) for further details on the inclusive standards of this project. Your cooperation in fostering an inclusive environment is greatly appreciated.

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

--------------------

For any use of the UBC salary data, please see UBC's Terms of Use [here](https://www.ubc.ca/site/legal.html).
