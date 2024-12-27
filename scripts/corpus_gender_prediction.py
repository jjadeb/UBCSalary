# author: Jade Bouchard
# date: 2024-04-29
#
# This script predicts peoples genders based off their first name
# We do this by finding the most common gender associated with a given name in baby name datasets
#
# Usage: python scripts/corpus_gender_prediction.py \
# --clean_salary_data_file=data/salary_data/clean_salary_data/all_clean_salary_data.csv \
# --canadian_babyname_data_file=data/gender_corpus/canadian_babyname.csv \
# --american_babyname_data_file=data/gender_corpus/american_babyname.csv \
# --indian_f_babyname_data_file=data/gender_corpus/Indian-Female-Names.csv \
# --indian_m_babyname_data_file=data/gender_corpus/Indian-Male-Names.csv \
# --clean_babyname_corpus_output_folder=data/gender_corpus \
# --prediction_ouput_folder=data/gender_predictions


import pandas as pd
import click
from clean_salary_data import shorten_name


def sum_frequency_counts(df):
    '''Group by first name and sex, then sum frequency counts over the years

    Parameters:
    ----------
    df : pandas.DataFrame
        data with columns 'Sex_at_birth', 'First_Name', 'Count', and 'Year' 
        
    Returns:
    -------
    df : pandas.DataFrame
        data with columns 'Sex_at_birth', 'First_Name', and 'Count'
    
    Example:
    ___________

    Input:

    | First_Name | Sex_at_birth | Indicator | Count    | Year |
    | ---------- | -------------| ----------| -------- | ---- |
    | Sam        | Female       | Frequency | 5000     | 1999 |
    | Sam        | Female       | Frequency | 2000     | 2000 |
    | Sam        | Male         | Frequency | 3000     | 1999 |
    | Sam        | Male         | Frequency | 2000     | 2000 |

    Returns:

    | Sex_at_birth | First_Name | Count    |
    | ------------ | -----------| -------- | 
    | Female       | Sam        | 7000     | 
    | Male         | Sam        | 5000     |
    '''

     # Group by baby name and sum frequency counts over the years, remove unnecessary features
    df = df[['Sex_at_birth', 'First_Name','Count']].groupby(['Sex_at_birth', 'First_Name']).sum().reset_index()
    return df


def find_totals(df):
    '''add column with total counts for each baby name (summing up across genders)

    Parameters:
    ----------
    df : pandas.DataFrame
        data with columns 'Sex_at_birth', 'First_Name', and 'Count' 
        
    Returns:
    -------
    df : pandas.DataFrame
        data with columns 'Sex_at_birth', 'First_Name', 'Count', and 'Total_Count'
    
    Example:
    ________

    Input:

    | Sex_at_birth | First_Name | Count |
    | ------------ | -----------| ----- | 
    | Female       | Sam        | 7000  | 
    | Male         | Sam        | 5000  | 

    Returns:

    | Sex_at_birth | First_Name | Count | Total_Count |
    | ------------ | ---------- | ----- | ----------- | 
    | Female       | Sam        | 7000  | 12000       | 
    | Male         | Sam        | 5000  | 12000       | 
    '''

    # create a dataframe with the total count of male + female babys for each baby name
    totals = df[['First_Name','Count']].groupby(['First_Name']).sum().reset_index().rename(columns = {'Count':'Total_Count'})
    # Merge the total count with the rest of the baby name data
    df = pd.merge(df, totals, on = 'First_Name', how = 'left')
    return df


def prepare_canadian_babyname_data(canada_df):
    '''Select necessary columns and perform aggregation functions on the canadian baby name dataset
    so that we are left with columns of sex, name, count for specified name and sex, and count for name accross all sexes
    
    Parameters:
    ----------
    canada_df : pandas.DataFrame
        canadian babyname data that contains the columns: "First name at birth", "Sex at birth", "Indicator", 
        "Year" (optional), "Count"
        
    Returns:
    -------
    canadian_names_gender_totals : pandas.DataFrame
        clean candadian babyname data containing the columns: "Sex_at_birth", "First_Name", 
        "Count", "Total_Count"
    '''

    # rename columns to remove spaces:
    canada_df = canada_df.rename(columns = {'First name at birth':'First_Name', 'Sex at birth':'Sex_at_birth','VALUE':'Count'})
    # shorten baby name to match salary data names
    canada_df.loc[:,'First_Name'] = canada_df['First_Name'].apply(shorten_name)
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
        clean american babyname data containing the columns: "Sex_at_birth", "First_Name", 
        "Count", "Total_Count"
    '''

    # If there are multiple names, just keep the first one
    american_df.loc[:,'Name'] = american_df['Name'].apply(shorten_name)
    # Rename columns to match Canadian data
    american_names_relable = american_df.rename(columns = {'Name':'First_Name', 'Gender':'Sex_at_birth'})
    # Relabel sex data to match Canadian data
    american_names_relable['Sex_at_birth'] = american_names_relable['Sex_at_birth'].replace({'F':'Female','M':'Male'})

    # Find counts for each name/gender combo over the years
    american_names_summed_counts = sum_frequency_counts(american_names_relable)
    # Find total for each name across gender
    american_names_totals = find_totals(american_names_summed_counts)

    return american_names_totals


def combine_two_babyname_datasets(dataset1, dataset2):
    '''combine two datasets, adding together counts and total counts from each dataset

    Parameters:
    ----------
    dataset1 : pandas.DataFrame
        data with columns 'Sex_at_birth', 'First_Name', 'Count', and 'Total_Count'
    dataset2 : pandas.DataFrame
        data with columns 'Sex_at_birth', 'First_Name', 'Count', and 'Total_Count'
        
    Returns:
    -------
    df : pandas.DataFrame
        data with columns 'Sex_at_birth', 'First_Name', 'Count', and 'Total_Count'
    
    Example
    _______

    Input:

    dataset1
    | Sex_at_birth | First_Name | Count | Total_Count |
    | ------------ | ---------- | ----- | ----------- | 
    | Female       | Sam        | 7000  | 12000       |  
    | Male         | Sam        | 5000  | 12000       | 

    dataset2
    | Sex_at_birth | First_Name | Count | Total_Count |
    | ------------ | ---------- | ----- | ----------- | 
    | Female       | Stephanie  | 1000  | 1000        | 
    | Male         | Sam        | 3000  | 3000        |  

    Returns:

    combined_names
    | Sex_at_birth | First_Name | Count | Total_Count |
    | ------------ | ---------- | ----- | ----------- | 
    | Female       | Stephanie  | 1000  | 1000        |
    | Female       | Sam        | 7000  | 15000       |
    | Male         | Sam        | 8000  | 15000       |  
    '''
    
    # Concat two datasets
    combined_names = pd.concat([dataset1,dataset2])
    # drop null values
    combined_names = combined_names.dropna()
    # make sure that the names are in Title Case to ensure consistency.
    combined_names['First_Name'] = combined_names['First_Name'].str.title()
    # group by name and sex, then add together up the value and total value counts from both datasets
    combined_names = combined_names[['Sex_at_birth', 'First_Name','Count','Total_Count']].groupby(['Sex_at_birth', 'First_Name']).sum().reset_index()
    return combined_names


def create_and_filter_accuracy_column(dataframe):
    '''Create a new column representing the accuracy of gender prediction for each baby name and filter to 
    keep the rows with the largest accuracy value for each name.

    Parameters:
    -----------
    dataframe : pandas.DataFrame
        Input DataFrame containing columns 'Sex_at_birth', 'First_Name', 'Count', and 'Total_Count'.

    Returns:
    --------
    dataframe: pandas.DataFrame
        filtered DataFrame with columns 'Sex_at_birth', 'First_Name', and 'Confidence_Score'

    Example
    -------
    Input:
    | Sex_at_birth | First_Name | Count | Total_Count |
    | ------------ | ---------- | ----- | ----------- | 
    | Female       | Stephanie  | 1000  | 1000        |
    | Female       | Sam        | 7000  | 15000       |
    | Male         | Sam        | 8000  | 15000       |

    Returns:
    | Sex_at_birth | First_Name  | Confidence_Score |
    |--------------|------------ |----------|
    | Male         | Sam         | 0.53     |
    | Female       | Stephanie   | 1.0      |
    '''

    # Create a new column that contains the percentage of counts that are [fem/male] for the given baby name
    dataframe['Confidence_Score'] = round(dataframe['Count']/dataframe['Total_Count'],2)
    # keep row with the sex that has the highest accuracy
    dataframe = dataframe.sort_values('Confidence_Score', ascending=False).drop_duplicates('First_Name').reset_index()
    # drop useless columns
    dataframe = dataframe.drop(columns = ['Count', 'Total_Count'])
    return dataframe


def prepare_indian_babyname_data(indian_female_df,indian_male_df):
    '''Prepare Indian baby name data for analysis by combining and standardizing female and male datasets. Add an accuracy column.
    IMPORTANT-NOTE: The assigned accuracy value is fairly arbitrary since there is no frequency measure in this data

    Parameters:
    -----------
    indian_female_df : pandas.DataFrame
        DataFrame containing Indian female baby name data with columns 'name','gender', and 'race'
    indian_male_df : pandas.DataFrame
        DataFrame containing Indian male baby name data with columns 'name','gender', and 'race'

    Returns:
    --------
    pandas.DataFrame
        DataFrame containing combined Indian baby names data with columns 'Sex_at_birth', 'First_Name', and 'Confidence_Score'.

    Example
    -------
 
    indian_female_df:
    | name      | gender | race   |
    |-----------|--------|--------|
    | Aaradhya  | f      | indian |
    | diya Min  | f      | indian |

    indian_male_df:
    | name      | gender | race   |
    |-----------|--------|--------|
    | Aarav     | m      | indian |
    | Arjun     | m      | indian |

    Returns:
    | Sex_at_birth | First_Name | Confidence_Score |
    |--------------|----------- |----------|
    | Female       | Aaradhya   | 0.85     |
    | Female       | Diya       | 0.85     |
    | Male         | Aarav      | 0.85     |
    | Male         | Arjun      | 0.85     |
    '''

    # Combine female and male names
    indian_names = pd.concat([indian_female_df,indian_male_df])
    # rename columns to match name corpus
    indian_names = indian_names.rename(columns = {'name':'First_Name', 'gender':'Sex_at_birth'})
    # relabel sex data to match name corpus
    indian_names['Sex_at_birth'] = indian_names['Sex_at_birth'].replace({'f':'Female','m':'Male'})
    # make sure names are in title case
    indian_names['First_Name'] = indian_names['First_Name'].str.title()
    # If there are multiple names, just keep the first one
    indian_names['First_Name'] = indian_names['First_Name'].apply(shorten_name)
    # Drop names that appear in the male and female datasets - since cannot determine which is most frequent
    indian_names = indian_names.drop_duplicates(subset=['First_Name'], keep = False)
    # drop unnecessary columns
    indian_names = indian_names.drop(columns = ['race'])
    # Apply arbitrary accuracy value
    indian_names['Confidence_Score'] = 0.85
    return indian_names


def make_gender_predictions_using_corpus(salary_data, name_corpus):
    '''Make gender predictions for individuals in salary data using a large dataset of names 
    and their associated genders.

    Parameters:
    -----------
    salary_data : pandas.DataFrame
        DataFrame containing salary data with at least a column 'First_Name' representing individual names.
    name_corpus : pandas.DataFrame
        DataFrame containing a name corpus with at least columns 'First_Name' and 'Sex_at_birth' 
        representing baby names and their associated genders.

    Returns:
    --------
    pop_df_predictions : pandas.DataFrame
        data which contains predictions for individuals with exact name matches found in the name corpus.
    pop_df_needs_predictions : pandas.DataFrame
        data which contains individuals where there was no exact name match, and their gender still needs to be predicted.

    Example
    -------
    Input:
    salary_data:
    | First_Name | Salary |
    |------------|--------|
    | John       | 50000  |
    | Emily      | 60000  |
    | Jane       | 610000 |
    | Alex       | 20000  |

    name_corpus:
    | First_Name | Sex_at_birth |
    |----------------------|--------------|
    | John                 | Male         |
    | Emily                | Female       |

    Returns:
    pop_df_predictions:
    | First_Name | Salary | Guessed_Gender |
    |------------|--------|--------------|
    | John       | 50000  | Male         |
    | Emily      | 60000  | Female       |

    pop_df_needs_predictions:
    | First_Name | Salary |
    |------------|--------|
    | Jane       | 610000 |
    | Alex       | 20000  |
    '''
    pop_df_predicted = pd.merge(salary_data, name_corpus, on = ['First_Name'], how = 'left')
    pop_df_predicted = pop_df_predicted.rename(columns={'Sex_at_birth': 'Guessed_Gender'})
    # Create dataset for exact name matches
    pop_df_predictions = pop_df_predicted[pop_df_predicted['Guessed_Gender'].notnull()]
    # Create dataset where there was no exact match and sex still needs to be predicted
    pop_df_needs_predictions = pop_df_predicted[~pop_df_predicted['Guessed_Gender'].notnull()]

    return pop_df_predictions, pop_df_needs_predictions
     
   
@click.command
@click.option('--clean_salary_data_file', type=str)
@click.option('--canadian_babyname_data_file', type=str)
@click.option('--american_babyname_data_file', type=str)
@click.option('--indian_f_babyname_data_file', type=str)
@click.option('--indian_m_babyname_data_file', type=str)
@click.option('--clean_babyname_corpus_output_folder', type=str)
@click.option('--prediction_ouput_folder', type=str)
def main(clean_salary_data_file, canadian_babyname_data_file, american_babyname_data_file, 
         indian_f_babyname_data_file, indian_m_babyname_data_file, clean_babyname_corpus_output_folder, prediction_ouput_folder):
    '''Main function to process salary data and make gender predictions.
    read in the data, clean babyname data, combine babyname data, and make predictions

    Parameters:
    -----------
    clean_salary_data_file : str
        Path to the clean salary data file.
    canadian_babyname_data_file : str
        Path to the canadian babyname data file.
    american_babyname_data_file : str
        Path to the american babyname data file.
    indian_f_babyname_data_file : str
        Path to the indian female babyname data file.
    indian_m_babyname_data_file : str
        Path to the indian male babyname data file.

    Output:
    -------
    corpus_gender_predictions.csv : csv
        data which contains predictions for individuals with exact name matches found in the name corpus.
    needs_gender_predictions.csv : csv
        data which contains individuals where there was no exact name match, and their gender still needs to be predicted.
    '''

    ############# READ IN DATA ##############
    # Read in canadian data we will use to make predictions
    # Data from statcan - https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710014701
    # Includes baby name data (name, sex at birth) for babies from 1991 to 2021
    canadian_names = pd.read_csv(canadian_babyname_data_file)

    # Read in extra data for american names and clean it up so that it can be merged with other name-sex data
    # https://www.kaggle.com/datasets/kaggle/us-baby-names/code
    american_names = pd.read_csv(american_babyname_data_file)

    # Read in data for indian names and clean it up so that it can be merged with other name-sex data
    # https://www.kaggle.com/datasets/ananysharma/indian-names-dataset
    f_indian_names = pd.read_csv(indian_f_babyname_data_file)
    m_indian_names = pd.read_csv(indian_m_babyname_data_file)

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
    canadian_and_american_babyname_data = combine_two_babyname_datasets(canadian_babyname_data,american_babyname_data)

    canadian_and_american_babyname_data_with_accuracy = create_and_filter_accuracy_column(canadian_and_american_babyname_data)

    name_corpus = pd.concat([canadian_and_american_babyname_data_with_accuracy,indian_babyname_data]).drop_duplicates(subset = 'First_Name')

    ############# MAKE PREDICTIONS ##############
    # Merge the names and gender dataset onto the UBC dataset to see if there are exact name matches

    gender_predictions, needs_gender_predictions = make_gender_predictions_using_corpus(salary_data, name_corpus)

    ############# SAVE PREDICTIONS AND CORPUS ##############
    gender_predictions.to_csv(f'{prediction_ouput_folder}/corpus_gender_predictions.csv', index = False)
    needs_gender_predictions.to_csv(f'{prediction_ouput_folder}/needs_gender_predictions.csv', index = False)
    name_corpus.to_csv(f'{clean_babyname_corpus_output_folder}/clean_name_corpus.csv', index = False)


if __name__ == "__main__":
    main()