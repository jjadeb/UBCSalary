

# Run entire project
all : data/gender_predictions/nltk_gender_predictions.csv

# Run parts of the project
clean-salary-data : data/salary_data/clean_salary_data/all_clean_salary_data.csv
corpus-predictions: data/gender_predictions/corpus_gender_predictions.csv
nltk-predictions : data/gender_predictions/nltk_gender_predictions.csv

# Fetch new salary data from UBC website to update raw data file
data/salary_data/raw_salary_data.pickle : scripts/fetch_salary_data.py
	python scripts/fetch_salary_data.py \
	--raw_salary_data_file=data/salary_data/raw_salary_data.pickle

# Clean salary data
data/salary_data/clean_salary_data/all_clean_salary_data.csv : scripts/clean_salary_data.py data/salary_data/raw_salary_data.pickle
	mkdir -p data/salary_data/clean_salary_data
	python scripts/clean_salary_data.py \
	--raw_salary_data_file=data/salary_data/raw_salary_data.pickle \
	--clean_salary_data_output_folder=data/salary_data/clean_salary_data

# Make gender predictions using babyname dataset
data/gender_predictions/corpus_gender_predictions.csv data/gender_predictions/needs_gender_predictions.csv data/gender_corpus/clean_name_corpus.csv : \
scripts/corpus_gender_prediction.py data/salary_data/clean_salary_data/all_clean_salary_data.csv \
data/gender_corpus/canadian_babyname.csv data/gender_corpus/american_babyname.csv \
data/gender_corpus/Indian-Female-Names.csv \
data/gender_corpus/Indian-Male-Names.csv
	python scripts/corpus_gender_prediction.py \
	--clean_salary_data_file=data/salary_data/clean_salary_data/all_clean_salary_data.csv \
	--canadian_babyname_data_file=data/gender_corpus/canadian_babyname.csv \
	--american_babyname_data_file=data/gender_corpus/american_babyname.csv \
	--indian_f_babyname_data_file=data/gender_corpus/Indian-Female-Names.csv \
	--indian_m_babyname_data_file=data/gender_corpus/Indian-Male-Names.csv \
	--clean_babyname_corpus_output_folder=data/gender_corpus \
	--prediction_ouput_folder=data/gender_predictions

# create gender classification model
models/gender_classifier.pickle data/gender_predictions/nltk_test_data.pickle data/gender_predictions/nltk_training_data.pickle : \
scripts/nltk_train_gender_classifier.py data/gender_corpus/clean_name_corpus.csv
	python scripts/nltk_train_gender_classifier.py \
	--name_data_path=data/gender_corpus/clean_name_corpus.csv \
	--model_output_folder=models \
	--data_output_folder=data/gender_predictions

# make gender predictions using nltk model
data/gender_predictions/nltk_gender_predictions.csv : scripts/nltk_make_predictions.py \
models/gender_classifier.pickle data/gender_predictions/nltk_test_data.pickle \
data/gender_predictions/needs_gender_predictions.csv
	python scripts/nltk_make_predictions.py \
	--model_path=models/gender_classifier.pickle \
	--nltk_test_data=data/gender_predictions/nltk_test_data.pickle \
	--needs_predictions_file_path=data/gender_predictions/needs_gender_predictions.csv \
	--nltk_predictions_output_path=data/gender_predictions/nltk_gender_predictions.csv

# Remove intermediary files
clean :
	-rm -r data/salary_data/clean_salary_data
	-rm -f data/gender_predictions/corpus_gender_predictions.csv data/gender_predictions/needs_gender_predictions.csv 
	-rm -f models/gender_classifier.pickle data/gender_predictions/nltk_test_data.pickle data/gender_predictions/nltk_training_data.pickle data/gender_predictions/nltk_gender_predictions.csv