
import pandas as pd
import click
import nltk



# Return features of a name to be fed into our model
def gender_features(word):
    word = word.lower()
    return {'last_5_letters': word[-5:], 'last_two_letters': word[-2:],
            'last_letter': word[-1:], 'last_3_letters': word[-3:], 'last_4_letters': word[-4:], 'name': word}



@click.command
@click.option('--training_data_path',type=str)
@click.option('--needs_predictions_file_path',type=str)
@click.option('--nltk_predictions_output_path',type=str)
def main(needs_predictions_file_path,nltk_predictions_output_path):
    # shuffle our data
    name_corpus = name_corpus.sample(frac=1,random_state=123)

    # collect features for each name in our data
    featuresets = [(gender_features(row['First name at birth']), row['Sex at birth']) for (index, row) in name_corpus.iterrows()]


    # split the shuffled data into train and test sets
    train_set, test_set = featuresets[3157:], featuresets[:3157]

    # train our classifier with the train set
    classifier = nltk.NaiveBayesClassifier.train(train_set)

    # score our classifier with the test set
    accuracy = round(nltk.classify.accuracy(classifier, test_set),2)
    accuracy

    # print out most informative features for the classifier
    classifier.show_most_informative_features()

    pop_df_needs_predictions = pd.read_csv(needs_predictions_file_path)

    # collect features for each name in our UBC data that still needs a sex assigned
    pop_df_needs_predictions.loc[:,'First Name'] = pop_df_needs_predictions['First Name'].astype(str)
    pop_testset = [(gender_features(row['First Name'])) for (index, row) in pop_df_needs_predictions.iterrows()]

    # Make predictions and note the classifier accuracy
    pop_df_needs_predictions.loc[:,'Sex at birth'] = classifier.classify_many(pop_testset)
    # For accuracy I am using the predict proba score given by the classifier
    pop_df_needs_predictions.loc[:,'Accuracy'] = [max(i.prob('Male'),i.prob('Female')) for i in classifier.prob_classify_many(pop_testset)]


    pop_df_predictions = pd.read_csv('data/gender_predictions/corpus_gender_predictions.csv')


    pop_df_predictions.to_csv(nltk_predictions_output_path, index = False)

if __name__ == "__main__":
    main()