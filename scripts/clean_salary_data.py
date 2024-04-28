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
import pickle

# Helper functions for cleaning data
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
    This removes incomplete list items and items such as: "SCHEDULE OF REMUNERATION AND EXPENSES" that
    do not refer to someone's salary'''
    list_of_str_clean = [i for i in list_of_str if (',' in i) and ('SCHEDULE' not in i)]
    return list_of_str_clean
    
def remove_extra_spaces_and_new_lines(list_of_str):
    '''remove extra spaces and new line charachters from the text. space removal takes two iterations'''
    list_of_str_clean = [i.replace('\n',' ').replace("  "," ").strip() for i in list_of_str]
    list_of_str_clean2 = [i.replace("  "," ") for i in list_of_str_clean]
    return list_of_str_clean2

def split_name_column_into_first_and_last(dataframe, name_column):
    '''split a name column into first name and last name by the comma deliminator'''
    dataframe['First Name'] = dataframe[name_column].str.split(', ', expand = True)[1]
    dataframe['Last Name'] = dataframe[name_column].str.split(', ', expand = True)[0]
    return dataframe

def make_column_numeric(dataframe, column_name):
    '''make a column have numeric values by removing commas and then applying the pandas numeric function'''
    dataframe[column_name] = dataframe[column_name].astype(str).str.replace(',','') # remove commas
    dataframe[column_name] = pd.to_numeric(dataframe[column_name], errors='coerce') # make column numeric



def clean_salary_data(year, raw_data):
    '''take salary data in string form and turn it into a dataframe, add a column and fill it with the given year'''
    # Remove beginning/end text
    salary_text = take_subset_of_text(raw_data, 'external cost recoveries.', 'Earnings greater than')

    # Split text into a list of people's salary information
    list_of_peoples_salaries = split_by_person(salary_text)
    
    # Remove unnessessary lines
    list_of_peoples_salaries_clean = remove_schedule_and_non_comma_lines(list_of_peoples_salaries)
    
    # Remove spaces and new lines
    list_of_peoples_salaries_formatted = remove_extra_spaces_and_new_lines(list_of_peoples_salaries_clean)
    
    # # Split data into Names/Remuneration/Expenses
    list_of_split_salaries = [i.rsplit(' ',2) for i in list_of_peoples_salaries_formatted]
    
    # Create Column names
    ubc_salary_data = pd.DataFrame(list_of_split_salaries, columns = ['Name', 'Remuneration', 'Expenses'])
    
    # Split Name into First/Last Name
    ubc_salary_data_first_last_name = split_name_column_into_first_and_last(ubc_salary_data, "Name")
    
    # Select necessary columns
    ubc_salary_data_subset = ubc_salary_data_first_last_name[['Last Name','First Name','Remuneration','Expenses']]
    
    # turn salary column from string to numeric
    ubc_salary_data_clean = make_column_numeric(ubc_salary_data_subset, 'Remuneration')

    # add given year as column
    ubc_salary_data_clean['Year'] = f"{year}"

    return ubc_salary_data_clean



@click.command()
@click.argument('raw_salary_data_file', type=str)
@click.argument('clean_salary_data_output_folder', type=str)
def main(raw_salary_data_file, clean_salary_data_output_folder):
    '''clean salary data for all years and then export the dataframes to csv files'''
    salary_data = pd.DataFrame(columns = ['Last Name', 'First Name', 'Remuneration', 'Expenses','Year']) # create empty dataframe for salary data

    # read in the raw salary data dictionary
    with open(raw_salary_data_file, "rb") as raw_salary_dict:
        raw_salary_text_data = pickle.load(raw_salary_dict)

    for year, raw_text_data in raw_salary_text_data.items(): # for each year that UBC has data for
        salaries = clean_salary_data(year, raw_text_data) # get clean data as a dataframe
        salaries.to_csv(f"{clean_salary_data_output_folder}/FY{year}_clean_salary_data.csv") # export individual clean dataframes
        salary_data = pd.concat([salary_data,salaries]) # paste dataframes together
    salary_data.to_csv(f"{clean_salary_data_output_folder}/all_clean_salary_data.csv") # export dataframe with all years

if __name__ == "__main__":
    main()