# author: Jade Bouchard
# date: 2024-04-27
#
# This script converts a dictionary of raw salary text data into a clean dataframe.
# The script then saves the data in csv format in the data folder
#
# Usage: python scripts/clean_salary_data.py data/salary_data/raw_salary_data.pickle data/salary_data

import click
import pandas as pd
import re
import pickle
from unidecode import unidecode
pd.options.mode.chained_assignment = None  # copy warnings are not an issue for this script

# Helper functions for cleaning data
def take_subset_of_text(text, start_phrase, end_phrase):
    '''return all text between two phrases
    
    Parameters:
    ----------
    text : str
        A long peice of text
    start_phrase : str
        We want to keep text after this start phrase
    end_phrase : str
        We want to keep text before this end phrase

    Returns:
    -------
    text_subset : str
        Text between the start phrase and end phrase
        '''
    
    text_subset = text.split(end_phrase)[0].split(start_phrase)[1]
    return text_subset


def remove_extra_spaces_and_new_lines(str):
    '''remove extra spaces and new line charachters from a string
    
    Parameters:
    ----------
    str : str
        Long string
        
    Returns:
    -------
    str_clean2 : str
        Spaces and new-line characters now removed from string

    Example:
    _______
    >>> str = "  \nAbdulai, Fatawu  89,454   8,049  \nAbdul -Mageed, \nMuhammad  105,795   13,458"
    >>> str_clean2 = remove_extra_spaces_and_new_lines(str)
    >>> print(str_clean2)
    >>> "Abdulai, Fatawu 89,454 8,049 Abdul -Mageed, Muhammad 105,795 13,458"
    '''

    str_clean = str.replace('\n',' ').replace("  "," ").strip()
    str_clean2 = str_clean.replace("  "," ")  # extra space removal takes two iterations
    return str_clean2


def split_by_person(salary_text):
    '''Splits text into a list of strings with each string containing salary data for one person.
    
    Parameters:
    ----------
    salary_text : str
        Text containing salary information for staff members
        
    Returns:
    -------
    list_of_peoples_salaries : list
        List where each element is a string containing an individual's salary information

    Example:
    --------
    >>> salary_text = "Aamodt, Tor 193,153 5,597 Abanto Salguero, Arleni Karina 107,723 393 Abbassi, Arash 109,136 82" 
    >>> list_of_peoples_salaries = split_by_person(salary_text)
    >>> print(list_of_peoples_salaries)
    >>> ['Aamodt, Tor 193,153 5,597','','Abanto Salguero, Arleni Karina 107,723 393','','Abbassi, Arash 109,136 82']
    '''
    
    # Regex captures groups that look like: [text] [numbers-including-commas] [numbers-including-commas-and-brackets or -]
    list_of_peoples_salaries = re.split("([a-zA-Z-\s.\(\)\'\-,]+\s[0-9,]+\s[0-9,\)\(|-]+)", salary_text) # split into individual data points
    list_of_peoples_salaries_stripped = [i.strip() for i in list_of_peoples_salaries] # strip whitespace from elements
    return list_of_peoples_salaries_stripped


def remove_uninformative_values(list_of_str, keep_lst, dont_keep_lst):
    '''Only keep items in a given list if they contain all keep-strings and they don't contain any dont-keep-strings

    Parameters:
    ----------
    list_of_str : list
        List where each element is of type string
    keep_lst : list
        Strings in list_of_str_clean should contain all substrings in the keep_lst
    dont_keep_lst : list
        Strings in list_of_str_clean should not contain any substrings in the dont_keep_lst
        
    Returns:
    -------
    list_of_str_clean : list
        List where each element is a string. Some uninformative values in the original list removed.
    
    Example:
    -------
    >>> list_of_str = ['Name Remuneration Expenses*', 'Aamodt, Tor 193,153 5,597', '']
    >>> list_of_str_clean = remove_uninformative_values(list_of_str, [","], ["SCHEDULE","Expenses*"])
    >>> print(list_of_str_clean)
    >>> ['Aamodt, Tor 193,153 5,597']
    '''

    list_of_str_clean = [i for i in list_of_str if (all(k in i for k in keep_lst) and not any(dk in i for dk in dont_keep_lst))]
    return list_of_str_clean


def hasNumbers(inputString):
    '''returns true if there are any numbers in the input string'''
    return any(char.isdigit() for char in inputString)


def split_name_with_and_without_comma(name):
    '''splits names into first and last names. Helper function for split_name_column_into_first_and_last
    
    Parameters:
    ----------
    name : str
        someone's name
        
    Returns:
    -------
    first_name : str
        person's first name
    last_name : str
        person's family name
    
    Examples:
    -------
    >>> name = "John Doe"
    >>> first_name, last_name = split_name_with_and_without_comma(name)
    >>> print(first_name, last_name)
    >>> John Doe

    >>> name = "Doe, John"
    >>> first_name, last_name = split_name_with_and_without_comma(name)
    >>> print(first_name, last_name)
    >>> John Doe

    >>> name = "John"
    >>> first_name, last_name = split_name_with_and_without_comma(name)
    >>> print(first_name, last_name)
    >>> John

    >>> name = "123,456"
    >>> first_name, last_name = split_name_with_and_without_comma(name)
    >>> print(first_name, last_name)
    >>> 
    '''

    if hasNumbers(name): # if number in name, then pdf reader did not parse names and salary properly (fix in progress)
        first_name, last_name = "",""
    elif ',' in name:
        # Splitting on comma for "Last, First" format
        last_name, first_name = name.split(', ', 1)
    elif " " in name:
        # Splitting on space for "First Last" format
        first_name, last_name = name.split(' ', 1)
    else: # if only one name, return it as the first name with empty last name
        first_name, last_name = name, ""
    return first_name, last_name


def make_column_numeric(dataframe, column_name):
    '''make a column have numeric values by removing commas and then applying the pandas numeric function
    
    Parameters:
    ----------
    dataframe : pandas.DataFrame
        Dataframe that contains a column with numbers in it
    name_column : str
        the name of the column that contains numbers, but isn't of numeric type
        
    Returns:
    -------
    dataframe : pandas.DataFrame
        original dataframe with column that contains numbers now of numeric type
    '''

    dataframe[column_name] = dataframe[column_name].astype(str).str.replace(',','') # remove commas
    dataframe[column_name] = pd.to_numeric(dataframe[column_name], errors='coerce') # make column numeric
    return dataframe


def clean_salary_data(year, raw_data):
    '''take salary data in string form and turn it into a dataframe, add a column and fill it with the given year
    
    Parameters:
    ----------
    year : str
        year that the data was collected in
    raw_data : str
        string that contains salary data for every staff member
        
    Returns:
    -------
    dataframe : pandas.DataFrame
        clean salary data containing last name, first name, salary (renumeration), expenses, and data collection year for each staff member
    
    Example:
    _______
    raw_data = " \n \nName  Remuneration  Expenses* \nAamodt, Tor  193,153   5,597  \nAbanto Salguero, \nArleni Karina  107,723   393  " 
    clean_data = clean_salary_data("2023", raw_data)
    print(clean_data)
    
    | Last_Name     | First_Name      | Remuneration | Expenses | Year |
    | ------------- | --------------- | ------------ | -------- | ---- |
    | Tor           | Aamodt          | 193153       | 5,597    | 2023 |
    | Arleni Karina | Abanto Salguero | 107723       | 393      | 2023 |

    '''

    # Remove beginning/end text
    salary_text = take_subset_of_text(raw_data, 'external cost recoveries.', 'Earnings greater than')

    # Remove spaces and new lines
    peoples_salaries_formatted = remove_extra_spaces_and_new_lines(salary_text)

    # Split text into a list of people's salary information
    list_of_peoples_salaries = split_by_person(peoples_salaries_formatted)
    
    # Remove unnessessary lines
    list_of_peoples_salaries_clean = remove_uninformative_values(list_of_peoples_salaries,[","],["SCHEDULE","*"])
    
    # Split data into Names/Remuneration/Expenses
    list_of_split_salaries = [i.rsplit(' ',2) for i in list_of_peoples_salaries_clean]
    
    # Create Column names
    ubc_salary_data = pd.DataFrame(list_of_split_salaries, columns = ['Name', 'Remuneration', 'Expenses'])
    
    # Split Name into First/Last Name
    ubc_salary_data[['First_Name', 'Last_Name']] = ubc_salary_data["Name"].apply(lambda x: pd.Series(split_name_with_and_without_comma(x)))

    # Remove rows with empty first name
    ubc_salary_data_removed_empty_rows = ubc_salary_data[(ubc_salary_data['First_Name'] != "") & (ubc_salary_data['First_Name'] != "-")]
    
    # Select necessary columns
    ubc_salary_data_subset = ubc_salary_data_removed_empty_rows[['Last_Name','First_Name','Remuneration','Expenses']]
    
    # turn salary column from string to numeric
    ubc_salary_data_clean = make_column_numeric(ubc_salary_data_subset, 'Remuneration')

    # add given year as column
    ubc_salary_data_clean['Year'] = f"{year}"

    return ubc_salary_data_clean



@click.command()
@click.argument('raw_salary_data_file', type=str)
@click.argument('clean_salary_data_output_folder', type=str)
def main(raw_salary_data_file, clean_salary_data_output_folder):
    '''clean salary data for all years and then export the dataframes to csv files
    
    Parameters:
    ----------
    raw_salary_data_file : str
        file path that points to the raw salary dictionary.
        this dictionary has year-strings for keys (ex:"2023") 
        and the values are strings of salary information for that year
    clean_salary_data_output_folder : str
        path to the folder that the clean data should go to
        
    Outputs:
    -------
    FY{year}_clean_salary_data.csv : csv
        sparate salary informaiton data for every available fiscal year
    all_clean_salary_data.csv : csv
        data containing all salary information for every available fiscal year
    '''

    # create empty dataframe for salary data
    salary_data = pd.DataFrame(columns = ['Last_Name', 'First_Name', 'Remuneration', 'Expenses','Year']) 

    # read in the raw salary data dictionary
    with open(raw_salary_data_file, "rb") as raw_salary_dict:
        raw_salary_text_data = pickle.load(raw_salary_dict)

    # clean and write data
    for year, raw_text_data in raw_salary_text_data.items(): # for each year that UBC has data for
        decoded_raw_text_data = unidecode(raw_text_data) # decode raw string (ex: Ayşe -> Ayse)
        salaries = clean_salary_data(year, decoded_raw_text_data) # get clean data as a dataframe 
        salaries.to_csv(f"{clean_salary_data_output_folder}/FY{year}_clean_salary_data.csv", index = False) # export individual clean dataframes
        salary_data = pd.concat([salary_data,salaries]) # paste dataframes together


    salary_data.to_csv(f"{clean_salary_data_output_folder}/all_clean_salary_data.csv", index = False) # export dataframe with all years


if __name__ == "__main__":
    main()