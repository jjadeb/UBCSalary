# author: Jade Bouchard
# date: 2024-04-29
#
# This script predicts peoples genders based off their first name
# We do this by finding the most common gender associated with a given name in baby name datasets
#
# Usage: python scripts/corpus_gender_prediction.py data/salary_data/all_clean_salary_data.csv

import pandas as pd
import click
from clean_salary_data import shorten_name

def sum_frequency_counts(df):
    '''Group by first name and sex, then sum frequency counts (value) over the years
    
    Example:
    ___________

    Input:

    | First_name_at_birth | Sex_at_birth | Indicator | Count    | Year |
    | ------------------- | -------------| ----------| -------- | ---- |
    | Sam                 | Female       | Frequency | 5000     | 1999 |
    | Sam                 | Female       | Frequency | 2000     | 2000 |
    | Sam                 | Male         | Frequency | 3000     | 1999 |
    | Sam                 | Male         | Frequency | 2000     | 2000 |

    Output:

    | Sex_at_birth | First_name_at_birth | Count    |
    | ------------ | ------------------- | -------- | 
    | Female       | Sam                 | 7000     | 
    | Male         | Sam                 | 5000     | 

    '''
     # Group by baby name and sum frequency counts over the years, remove unnecessary features
    df = df[['Sex_at_birth', 'First_name_at_birth','Count']].groupby(['Sex_at_birth', 'First_name_at_birth']).sum().reset_index()
    return df

def find_totals(df):
    '''add column with total counts for each baby name (summing up across genders)
    
    Example:
    ________

    Input:

    | Sex_at_birth | First_name_at_birth | Count |
    | ------------ | ------------------- | ----- | 
    | Female       | Sam                 | 7000  | 
    | Male         | Sam                 | 5000  | 

    Output:

    | Sex_at_birth | First_name_at_birth | Count | Total_Count |
    | ------------ | ------------------- | ----- | ----------- | 
    | Female       | Sam                 | 7000  | 12000       | 
    | Male         | Sam                 | 5000  | 12000       | 
    
    
    '''
    # create a dataframe with the total count of male + female babys for each baby name
    totals = df[['First_name_at_birth','Count']].groupby(['First_name_at_birth']).sum().reset_index().rename(columns = {'Count':'Total_Count'})
    # Merge the total count with the rest of the baby name data
    df = pd.merge(df, totals, on = 'First_name_at_birth', how = 'left')
    return df


def prepare_canadian_babyname_data(canada_df):
    '''Select necessary columns and perform aggregation functions on the canadian baby name dataset
    so that we are left with columns of sex, name, count for specified sex, and count accross all sexes
    
    Parameters:
    ----------
    canada_df : pandas.DataFrame
        canadian babyname data that contains the columns: "First name at birth", "Sex at birth", "Indicator", 
        "Year" (optional), "Count"
        
    Returns:
    -------
    canadian_names_gender_totals : pandas.DataFrame
        clean candadian babyname data containing the columns: "Sex_at_birth", "First_name_at_birth", 
        "Count", "Total_Count"
    '''
    # rename columns to remove spaces:
    canada_df = canada_df.rename(columns = {'First name at birth':'First_name_at_birth', 'Sex at birth':'Sex_at_birth','VALUE':'Count'})
    # shorten baby name to match salary data names
    canada_df.loc[:,'First_name_at_birth'] = canada_df['First_name_at_birth'].apply(shorten_name)
    # filter for frequency of baby name values (each baby name has a row for frequency, rank, and proportion)
    canadian_names_frequency = canada_df.query("Indicator == 'Frequency'")
    # Group by baby name and sum frequency counts over the years, remove unnecessary features
    canadian_names_over_all_years = sum_frequency_counts(canadian_names_frequency)
    # Find the total count of male + female for each baby name
    canadian_names_gender_totals = find_totals(canadian_names_over_all_years)
    return canadian_names_gender_totals

def prepare_american_babyname_data(american_df):
    '''Select necessary columns and perform aggregation functions on the american baby name dataset 
    so that we are left with columns of sex, name, count for specified sex, and count accross all sexes
    
    Parameters:
    ----------
    american_df : pandas.DataFrame
        american babyname data that contains the columns: "Name", "Gender", "Year" (optional), "Count"
        
    Returns:
    -------
    american_names_totals : pandas.DataFrame
        clean american babyname data containing the columns: "Sex_at_birth", "First_name_at_birth", 
        "Count", "Total_Count"
    '''
    # If there are multiple names, just keep the first one
    american_df.loc[:,'Name'] = american_df['Name'].apply(shorten_name)
    # Rename columns to match Canadian data
    american_names_relable = american_df.rename(columns = {'Name':'First_name_at_birth', 'Gender':'Sex_at_birth'})
    # Relabel sex data to match Canadian data
    american_names_relable['Sex_at_birth'] = american_names_relable['Sex_at_birth'].replace({'F':'Female','M':'Male'})

    # Find counts for each name/gender combo over the years
    american_names_summed_counts = sum_frequency_counts(american_names_relable)
    # Find total for each name across gender
    american_names_totals = find_totals(american_names_summed_counts)

    return american_names_totals

def combine_american_and_canadian_babyname_data(canadian_df, american_df):
    '''combine the american and canadian baby name data, ensuring proper formatting'''
    
    # Combine american and canadian data
    combined_names = pd.concat([canadian_df,american_df])
    # drop null values
    combined_names = combined_names.dropna()
    # make sure that the names are in Title Case to ensure consistency.
    combined_names['First_name_at_birth'] = combined_names['First_name_at_birth'].str.title()
    # group by name and sex, then sum up the value and total value counts for American and Canadian data
    combined_names = combined_names[['Sex_at_birth', 'First_name_at_birth','Count','Total_Count']].groupby(['Sex_at_birth', 'First_name_at_birth']).sum().reset_index()
    return combined_names

def create_accuracy_column(dataframe):
    # Create a new column that contains the percentage of counts that are [fem/male] for the given baby name
    dataframe['Accuracy'] = round(dataframe['Count']/dataframe['Total_Count'],2)
    # keep row with the sex that has the highest accuracy
    dataframe = dataframe.sort_values('Accuracy', ascending=False).drop_duplicates('First_name_at_birth').reset_index()
    # drop useless columns
    dataframe = dataframe.drop(columns = ['Count', 'Total_Count'])
    # sort values by accuracy
    dataframe.sort_values(by = 'Accuracy')

def prepare_indian_babyname_data(indian_female_df,indian_male_df):
    # Combine female and male names
    indian_names = pd.concat([indian_female_df,indian_male_df])
    # rename columns to match name corpus
    indian_names = indian_names.rename(columns = {'name':'First_name_at_birth', 'gender':'Sex_at_birth'})
    # relabel sex data to match name corpus
    indian_names['Sex_at_birth'] = indian_names['Sex_at_birth'].replace({'f':'Female','m':'Male'})
    # make sure names are in title case
    indian_names['First_name_at_birth'] = indian_names['First_name_at_birth'].str.title()
    # If there are multiple names, just keep the first one
    indian_names['First_name_at_birth'] = [str(i).split(' ')[0] for i in indian_names['First_name_at_birth']]
    # drop unnecessary columns
    indian_names = indian_names.drop(columns = ['race'])
    # Apply arbitrary accuracy value
    indian_names['Accuracy'] = 0.85
    return indian_names

def make_gender_predictions_using_corpus(salary_data, name_corpus):
    pop_df_predicted = pd.merge(salary_data, name_corpus, left_on = ['First_Name'], right_on = ['First_name_at_birth'], how = 'left')
    # Create dataset for exact name matches
    pop_df_predictions = pop_df_predicted[pop_df_predicted['Sex_at_birth'].notnull()]
    # Create dataset where there was no exact match and sex still needs to be predicted
    pop_df_needs_predictions = pop_df_predicted[~pop_df_predicted['Sex_at_birth'].notnull()]
    return pop_df_predictions, pop_df_needs_predictions
     
   
@click.command
@click.argument('clean_salary_data_file', type=str)
def main(clean_salary_data_file):

    ############# READ IN DATA ##############
    # Read in canadian data we will use to train our model
    # Data from statcan - https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710014701
    # Includes baby name data (name, sex at birth) for babies from 1991 to 2021
    canadian_names = pd.read_csv('data/gender_corpus/17100147.csv')

    # Read in extra data for american names and clean it up so that it can be merged with other training data
    # https://www.kaggle.com/datasets/kaggle/us-baby-names/code
    american_names = pd.read_csv("data/gender_corpus/NationalNames.csv")

    # Read in data for indian names and clean it up so that it can be merged with other training data
    # https://www.kaggle.com/datasets/ananysharma/indian-names-dataset
    f_indian_names = pd.read_csv('data/gender_corpus/Indian-Female-Names.csv')
    m_indian_names = pd.read_csv('data/gender_corpus/Indian-Male-Names.csv')

    # Read in clean salary data
    salary_data = pd.read_csv(clean_salary_data_file)
    
    ############# CLEAN DATA ##############
    # clean canadian data
    canadian_babyname_data = prepare_canadian_babyname_data(canadian_names)

    # clean american data
    american_babyname_data = prepare_american_babyname_data(american_names)

    # clean indian data
    indian_babyname_data = prepare_indian_babyname_data(f_indian_names, m_indian_names)

    ############# COMBINE DATA ##############
    canadian_and_american_babyname_data = combine_american_and_canadian_babyname_data(canadian_babyname_data,american_babyname_data)

    name_corpus = pd.concat([canadian_and_american_babyname_data,indian_babyname_data]).drop_duplicates(subset = 'First_name_at_birth')

    ############# MAKE PREDICTIONS ##############
    # Merge the names and gender dataset onto the UBC dataset to see if there are exact name matches

    gender_predictions, needs_gender_predictions = make_gender_predictions_using_corpus(salary_data, name_corpus)

    ############# SAVE PREDICTIONS ##############
    gender_predictions.to_csv('data/gender_predictions/corpus_gender_predictions.csv', index = False)
    needs_gender_predictions.to_csv('data/gender_predictions/needs_gender_predictions.csv', index = False)


if __name__ == "__main__":
    main()