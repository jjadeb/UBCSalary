# author: Jade Bouchard
# date: 2024-04-27
#
# This script converts a dictionary of raw salary text data into a clean dataframe.
# The script then saves the data in csv format in the data folder
#
# Usage: python scripts/clean_salary_data.py data/salary_data/clean_salary_data.csv

import click
import pandas as pd
import re

def take_subset_of_text(text, start_phrase, end_phrase):
    '''return all text between two phrases'''
    text_subset = text.split(end_phrase)[0].split(start_phrase)[1]
    return text_subset

def split_by_person(salary_text):
    '''Splits text into a list of strings with each string containing salary data for one person.
    example string in returned list: "nAbdi, Ali  238,203   2,981" '''
    list_of_peoples_salaries = re.split('([\.\p{L},\s-]+[\s\n]+[0-9,-]+[\s\n]+[0-9,-]+)', salary_text)
    return list_of_peoples_salaries

def remove_schedule_and_non_comma_lines(list_of_str):
    '''Remove items in a list if they dont contain a comma or they contain the word "SCHEDULE".
    This removes incomplete values and values such as: "SCHEDULE OF REMUNERATION AND EXPENSES" '''
    list_of_str_clean = [i for i in list_of_str if (',' in i) and ('SCHEDULE' not in i)]
    return list_of_str_clean
    
#def remove_spaces


def clean_salary_data(raw_data, year):
    '''take salary data in string form and turn it into a dataframe, add a column and fill it with the given year'''
    # Remove beginning/end text
    salary_text = take_subset_of_text(raw_data, 'external cost recoveries.', 'Earnings greater than')

    # Split text into a list of people's salary information
    list_of_peoples_salaries = split_by_person(salary_text)
    
    # Remove unnessessary lines
    list_of_peoples_salaries_clean = remove_schedule_and_non_comma_lines(list_of_peoples_salaries)
    
    # Remove spaces and new lines
    raw_data_d = [i.replace('\n',' ').replace("  "," ").strip() for i in list_of_peoples_salaries_clean]
    raw_data_d = [i.replace("  "," ") for i in raw_data_d]
    
    # # Split data into Names/Remuneration/Expenses
    raw_data_e = [i.rsplit(' ',2) for i in raw_data_d]
    raw_data_e
    
    # Create Column names
    ubc_salary_data = pd.DataFrame(raw_data_e, columns = ['Name', 'Remuneration', 'Expenses'])
    
    # Split Name into First/Last Name
    ubc_salary_data['First Name'] = ubc_salary_data['Name'].str.split(', ', expand = True)[1]
    ubc_salary_data['Last Name'] = ubc_salary_data['Name'].str.split(', ', expand = True)[0]
    
    
    # Select necessary columns
    ubc_salary_data = ubc_salary_data[['Last Name','First Name','Remuneration','Expenses']]
    
    # turn salary column from string to numeric
    ubc_salary_data['Remuneration'] = ubc_salary_data['Remuneration'].astype(str).str.replace(',','')
    ubc_salary_data['Remuneration'] = pd.to_numeric(ubc_salary_data['Remuneration'], errors='coerce')

    ubc_salary_data['Year'] = f"{year}"

    return ubc_salary_data



@click.command()
@click.argument('clean_salary_data_output_folder', type=str)
def main(clean_salary_data_output_folder):
    salary_data = pd.DataFrame(columns = ['Last Name', 'First Name', 'Remuneration', 'Expenses','Year']) # create empty dataframe for salary data
    most_recent = True # keeps track of most recent salary data
    for year, link in links.items(): # for each year that UBC has data for
        raw = fetch_salary_data(link) # get raw data in string form
        salaries = clean_salary_data(raw, year) # get clean data as a dataframe
        if most_recent: # export the most recent salary data so that we can collect the new department/job title info
            salaries.to_csv(f"/Users/jadebouchard/Desktop/UBC Salaries/Salary Data/{year}.csv")
            most_recent = False
        if salary_data.empty: # avoid warning that we shouldn't be concatenating empty dataframes
            salary_data = salaries
        else:
            salary_data = pd.concat([salary_data,salaries]) # paste dataframes together
    salary_data.to_csv(clean_salary_data_output_folder)

if __name__ == "__main__":
    main()