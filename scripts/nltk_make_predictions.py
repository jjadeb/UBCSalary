# author: Jade Bouchard
# date: 2024-04-30
#
# This script uses a naive bayes natural language processing classifier to classify people's genders
#
# Usage: python scripts/nltk_make_predictions.py \
	# --model_path=models/gender_classifier.pickle \
	# --nltk_test_data=data/gender_predictions/nltk_test_data.pickle \
	# --needs_predictions_file_path=data/gender_predictions/needs_gender_predictions.csv \
	# --nltk_predictions_output_path=data/gender_predictions/nltk_gender_predictions.csv

import click
import pickle
import pandas as pd
from nltk_train_gender_classifier import feature_engineering
import nltk

@click.command
@click.option('--model_path',type=str)
@click.option('--nltk_test_data',type=str)
@click.option('--needs_predictions_file_path',type=str)
@click.option('--nltk_predictions_output_path',type=str)
@click.option('--accuracy_output_path',type=str)
def main(model_path,nltk_test_data,needs_predictions_file_path,nltk_predictions_output_path, 
         accuracy_output_path):

    ################ read in the model and the data ################

    # reading in the classifier
    with open(model_path, "rb") as model_file:
        classifier = pickle.load(model_file)

    # reading in the data that needs predictions
    needs_predictions_df = pd.read_csv(needs_predictions_file_path)

    # reading in the test data for the model
    with open(nltk_test_data, "rb") as test_data_file:
        test_set = pickle.load(test_data_file)

    # calculating the accuracy of the model on the test set
    accuracy = round(nltk.classify.accuracy(classifier, test_set),2)
    with open(accuracy_output_path, 'w') as file:
        file.write(str(accuracy))

    ######### collect features for each name in our UBC data that still needs a sex assigned ########

    # create a list of tuples with the first item in the tuple being a featureset
    # and the second item in the tuble being an empty string for the unknown sex 
    ### ex: [({name: 'bobby', last_3_letters: 'bby'},'')]
    list_of_features = feature_engineering(needs_predictions_df, 'First_Name', 'Guessed_Gender')

    # Retrieve only the featuresets from the list tuples
    list_of_features = [i[0] for i in list_of_features]

    ################ make predictions and assign accuracy ################

    # Make sex column of type string, then make sex predictions 
    needs_predictions_df['Guessed_Gender'] = ""
    needs_predictions_df.loc[:,'Guessed_Gender'] = classifier.classify_many(list_of_features)

    # For the accuracy column, I am using the predict proba score given by the classifier
    # multiplied by the accuracy score on the test set
    # The predict proba score represents the uncertainty of the model between the two sexes
    needs_predictions_df.loc[:,'Confidence_Score'] = [round(max(i.prob('Male'),i.prob('Female'))*accuracy,2) for i in classifier.prob_classify_many(list_of_features)]

    ################ save the predictions ################
    # saving the nltk predictions
    needs_predictions_df.to_csv(nltk_predictions_output_path, index = False)


if __name__ == "__main__":
    main()