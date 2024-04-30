

# Run entire analysis
all : data/gender_predictions/corpus_gender_predictions.csv

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
data/gender_predictions/corpus_gender_predictions.csv data/gender_predictions/needs_gender_predictions.csv : \
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

# Remove intermediary files
clean :
	-rm -r data/salary_data/clean_salary_data
	-rm -f data/gender_predictions/corpus_gender_predictions.csv data/gender_predictions/needs_gender_predictions.csv 