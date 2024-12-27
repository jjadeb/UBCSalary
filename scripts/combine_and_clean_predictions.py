# author: Jade Bouchard
# date: 2024-05-01
#
# This script combines the gender predictions from the corpus and machine learning (nltk) methods
# the script then removes weak predictions and fixes known incorrect predictions
#
# Usage: python scripts/combine_and_clean_predictions.py \
# --nltk_gender_predictions_input=data/gender_predictions/nltk_gender_predictions.csv \
# --corpus_gender_predictions_input=data/gender_predictions/corpus_gender_predictions.csv \
# --all_gender_predictions_output=data/gender_predictions/all_clean_gender_predictions.csv


import click
import pandas as pd

def change_sex(dataframe, first_name, last_name, update_sex):
    '''Change the sex of a person in the given DataFrame.

    This function modifies the 'Guessed_Gender' column of the DataFrame to change the sex of a person 
    specified by their first name and last name. If a person with the specified first name and last name 
    is found in the DataFrame, their sex is updated to the specified sex.

    Parameters:
    -----------
    dataframe : pandas.DataFrame
        DataFrame containing person data with columns 'First_Name', 'Last_Name', and 'Guessed_Gender'.
    first_name : str
        First name of the person whose sex is to be changed.
    last_name : str
        Last name of the person whose sex is to be changed.
    update_sex : str
        Sex to set for the person specified by the first name and last name.

    Returns:
    --------
    pandas.DataFrame
        Modified DataFrame with the sex of the specified person updated.

    Example
    -------
    data:
    | First_Name | Last_Name | Guessed_Gender |
    |------------|-----------|--------------|
    | John       | Smith     | Male         |
    | Emily      | Johnson   | Female       |

    change_gender(data, 'Emily', 'Johnson', 'Male')
    Output:
    | First_Name | Last_Name | Guessed_Gender |
    |------------|-----------|--------------|
    | John       | Smith     | Male         |
    | Emily      | Johnson   | Male         |
    '''
    dataframe.loc[(dataframe['First_Name'] == first_name) & (dataframe['Last_Name'] == last_name),'Guessed_Gender'] = update_sex
    return dataframe


@click.command
@click.option('--nltk_gender_predictions_input',type=str)
@click.option('--corpus_gender_predictions_input',type=str)
@click.option('--all_gender_predictions_output',type=str)
def main(nltk_gender_predictions_input,corpus_gender_predictions_input,all_gender_predictions_output):
    '''Combine and process gender predictions from different sources and output the final predictions.

    This function serves as the entry point for combining and processing gender predictions from 
    two different sources: NLTK classifier predictions and corpus predictions. It reads in the predictions 
    from the specified input files, concatenates them together, drops unnecessary columns, removes 
    predictions with an accuracy of less than 0.8, and corrects gender predictions that were found 
    to be incorrect for specific individuals. Finally, it exports the cleaned and combined predictions 
    to the specified output file.

    Parameters:
    -----------
    nltk_gender_predictions_input : str
        Path to the file containing NLTK classifier predictions.
    corpus_gender_predictions_input : str
        Path to the file containing corpus predictions.
    all_gender_predictions_output : str
        Path to the output file where the final predictions will be saved.
    '''

    # read in the corpus predictions and nltk classifier predictions
    nltk_predictions = pd.read_csv(nltk_gender_predictions_input)
    corpus_predictions = pd.read_csv(corpus_gender_predictions_input)

    # concat the prediction data together
    complete_predictions = pd.concat([corpus_predictions, nltk_predictions])

    # drop the unecessary index column
    complete_predictions_clean = complete_predictions.drop(columns = ['index'])

    # remove gender predictions that have an accuracy of less than 0.8
    complete_predictions_clean.loc[complete_predictions_clean['Confidence_Score'] < 0.8,'Guessed_Gender'] = ""

    # change gender predictions that were found to be incorrect
    complete_predictions_clean = change_sex(complete_predictions_clean, "Lakshmi", "Yatham", "Male")
    complete_predictions_clean = change_sex(complete_predictions_clean, "Santa", "Ono", "Male")
    complete_predictions_clean = change_sex(complete_predictions_clean, "Ali", "Lazrak", "Male")
    complete_predictions_clean = change_sex(complete_predictions_clean, "Jan", "Bena", "Female")
    complete_predictions_clean = change_sex(complete_predictions_clean, "Zu-Hua", "Gao", "Male")
    
    # export dataset
    complete_predictions_clean.to_csv(all_gender_predictions_output, index = False)


if __name__ == "__main__":
    main()