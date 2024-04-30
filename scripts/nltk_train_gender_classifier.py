
# author: Jade Bouchard
# date: 2024-04-30
#
# This script trains a naive bayes natural language processing classifier 
# to predict someone's gender based off their first name
# The script then saves the training data, test data, and classifier 
#
# Usage: python scripts/nltk_train_gender_classifier.py --name_data_path=data/gender_corpus/clean_name_corpus.csv --model_output_folder=models --data_output_folder=data/gender_predictions


import pandas as pd
import click
import nltk
import pickle


# Return features of a name to be fed into our model
def gender_features(word):
    ''' Engineer features for a given name

    This function takes a word as input and generates a dictionary of features for gender classification. 
    The features include:
    - 'last_5_letters': Last 5 letters of the word
    - 'last_two_letters': Last 2 letters of the word
    - 'last_letter': Last letter of the word
    - 'last_3_letters': Last 3 letters of the word
    - 'last_4_letters': Last 4 letters of the word
    - 'name': The word itself

    Parameters:
    -----------
    word : str
        Input word for which features are to be engineered.

    Returns:
    --------
    word_feats : dict
        A dictionary containing the engineered features of the input word.

    Example
    -------
    gender_features('Emily')
    Output: {'last_5_letters': 'emily', 'last_two_letters': 'ly', 'last_letter': 'y',
             'last_3_letters': 'ily', 'last_4_letters': 'mily', 'name': 'emily'}
    '''
    word = word.lower()
    word_feats = {'last_5_letters': word[-5:], 'last_two_letters': word[-2:],
            'last_letter': word[-1:], 'last_3_letters': word[-3:], 'last_4_letters': word[-4:], 'name': word}

    return word_feats

def feature_engineering(data, name_col, gender_col):
    '''Perform feature engineering on a dataset

    This function takes a dataset containing names and associated genders and performs feature engineering. 
    It generates feature sets by applying the 'gender_features' function to each row in the dataset.

    Parameters:
    -----------
    data : pandas.DataFrame
        DataFrame containing the dataset with names and associated genders.
    name_col : str
        Name of the column in the DataFrame containing the names.
    gender_col : str
        Name of the column in the DataFrame containing the genders.

    Returns:
    --------
    featuresets : list of tuples
        A list of tuples where each tuple contains a dictionary of engineered features 
        and the corresponding gender label.

    Example
    -------
    data:
    | name      | gender |
    |-----------|--------|
    | Aaradhya  | f      |
    | Odiya     | f      |

    feature_engineering(data, 'name', 'gender')
    Output: [({'last_5_letters': 'adhya', 'last_two_letters': 'ya', 'last_letter': 'a',
               'last_3_letters': 'hya', 'last_4_letters': 'dhya', 'name': 'aaradhya'}, 'f'),
             ({'last_5_letters': 'odiya', 'last_two_letters': 'ya', 'last_letter': 'a',
               'last_3_letters': 'iya', 'last_4_letters': 'diya', 'name': 'odiya'}, 'f')]
    '''
    featuresets = [(gender_features(row[name_col]), row[gender_col]) for (index, row) in data.iterrows()]
    return featuresets

@click.command
@click.option('--name_data_path',type=str)
@click.option('--data_output_folder',type=str)
@click.option('--model_output_folder',type=str)
def main(name_data_path,model_output_folder,data_output_folder):
    '''Train a gender classifier model using baby name data and save the trained model and data.

    This function serves as the entry point for training a gender classifier model using baby name data. 
    It reads in the baby name data from the specified path, shuffles the data, 
    engineers features for each name, splits the data into train and test sets, 
    trains a Naive Bayes classifier using the train set, and saves the trained model 
    and data to the specified output folders.

    Parameters:
    -----------
    name_data_path : str
        Path to the babyname data file.
    model_output_folder : str
        Path to the folder where the trained model will be saved.
    data_output_folder : str
        Path to the folder where the training and test data will be saved.
'''

    #read in babyname data
    name_corpus = pd.read_csv(name_data_path)

    # shuffle our data
    name_corpus = name_corpus.sample(frac=1,random_state=123)

    # collect features for each name in our data
    featuresets = feature_engineering(name_corpus, 'First_name_at_birth', 'Sex_at_birth')

    # split the shuffled data into train and test sets
    train_set, test_set = featuresets[3157:], featuresets[:3157]

    # train our classifier with the train set
    classifier = nltk.NaiveBayesClassifier.train(train_set)

    pickle.dump(classifier, open(f'{model_output_folder}/gender_classifier.pickle', 'wb'))
    pickle.dump(train_set, open(f'{data_output_folder}/nltk_training_data.pickle', 'wb'))
    pickle.dump(test_set, open(f'{data_output_folder}/nltk_test_data.pickle', 'wb'))


if __name__ == "__main__":
    main()