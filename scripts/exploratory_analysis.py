# author: Jade Bouchard
# date: 2024-05-02
#
# This script creates plots for the salary and gender data 
#
# Usage: python scripts/exploratory_analysis.py


import pandas as pd
import numpy
import matplotlib.pyplot as plt
from math import log10
import numpy as np
plt.rcParams.update({'font.size': 14, 'font.family': 'sans-serif'})

def prepare_data_for_plot(data, year, salary_col, first_name_col, last_name_col, name_col):
    # filter for specific year
    processed_data = data[data["Year"] == year]
    # devide salary by 1000 to help with plot readability
    processed_data[salary_col] = processed_data[salary_col]/1000
    # create column with both names for bar plots
    processed_data[name_col] = processed_data[first_name_col] + ' ' + processed_data[last_name_col]
    return processed_data


def create_top_ten_bar_plot(data, numeric_column_name, categorical_column_name, colour_bar_column_name, colour_bar_opt1,
                            colour_bar_opt2, file_name, plot_title, x_axis_lab, y_axis_lab):
    # Sort the data by remuneration in descending order and select the top ten rows
    top_ten_data = data.nlargest(10, numeric_column_name)

    # Set font sizes and style
    plt.rcParams.update({'font.size': 14, 'font.family': 'sans-serif'})

    # Define colors 
    colours = ['#FF8C00', '#2B2F42','#808080']

    # Create bar plot for the top ten values colored by colour column
    plt.figure(figsize=(10, 6))
    for index, row in top_ten_data.iterrows():
        if row[colour_bar_column_name] == colour_bar_opt1:
            colour = colours[0] 
        elif row[colour_bar_column_name] == colour_bar_opt2:
            colour = colours[1]
        else:
            colour = colours[2]
        plt.bar(row[categorical_column_name], row[numeric_column_name], color=colour)

    # Set labels and title
    plt.xlabel(x_axis_lab, fontdict={'size':14})
    plt.ylabel(y_axis_lab, fontdict={'size':14})
    plt.title(plot_title, fontdict={'size':22})

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Hide the top and right spines
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # Create legend for bar plot colors
    plt.legend(handles=[
        plt.Rectangle((0,0),1,1, color=colours[0], label=colour_bar_opt1),
        plt.Rectangle((0,0),1,1, color=colours[1], label=colour_bar_opt2),
        plt.Rectangle((0,0),1,1, color=colours[2], label='Unknown')
    ], loc='upper right', title='Guessed Gender')

    plt.grid(False)

    plt.tight_layout()
    plt.savefig(f'plots/bar_plots/top_ten_{file_name}.png')


def create_top_ten_bar_plots_for_all_years():
    pass

def create_histogram_plot_for_one_year(data, min_value, max_value, numeric_col, category_col,
                                       plot_title, xlab, ylab, file_name, cut_off_factor, bins):

    # Define bins
    bins = np.linspace(min_value, round(max_value), bins)

    # Separate data by gender
    female_expenses = data[data[category_col] == "Female"][numeric_col]
    male_expenses = data[data[category_col] == "Male"][numeric_col]

    # Create histogram plot
    plt.figure(figsize=(9, 5))
    plt.hist(male_expenses, bins, alpha=0.5, label='Male', color="#2B2F42")
    plt.hist(female_expenses, bins, alpha=0.5, label='Female', color="#FF8C00")
    plt.legend(loc='upper right', title = "Guessed Gender")

    # Set labels and title
    plt.xlabel(xlab, fontdict={'size':14})
    plt.ylabel(ylab, fontdict={'size':14})
    plt.title(plot_title, fontdict={'size':16})
    plt.xlim(min_value,max_value*cut_off_factor)

    # Hide the top and right spines
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    plt.grid(True)
    plt.savefig(f'plots/histogram_plots/histogram_of_{file_name}.png')



def main():
    ## read in data
    data = pd.read_csv('data/gender_predictions/all_clean_gender_predictions.csv')
  

    ## for each year create a bar plot of the top ten salaries and box plots of salaries and expenses
    years = data["Year"].unique().tolist()
    for year in years:
        processed_data = prepare_data_for_plot(data, year, 'Remuneration', 
                                            'First_Name',"Last_Name","Name")

        year = str(int(year))

        ## create summary data table and store min/max values
        data_summary_year = processed_data[["Remuneration","Expenses"]].apply(
        {
            "Remuneration":["mean","median","min","max"],
            "Expenses":["mean","median","min","max"]
        }
        ).map(lambda x: round(x, 2))

        max_expenses = data_summary_year.loc['max','Expenses']
        min_expenses = data_summary_year.loc['min','Expenses']
        max_remuneration = data_summary_year.loc['max','Remuneration']
        min_remuneration = data_summary_year.loc['min','Remuneration']

        # create top ten bar plots for salaries
        create_top_ten_bar_plot(processed_data, 'Remuneration', 'Name', 'Sex_at_birth', 'Female',
                                'Male', f'salaries_{year}', f'Top Ten Salaries in {year}', 
                                'Name', 'Salary (CAD, in thousands)')
        
        # create top ten bar plots for expenses
        create_top_ten_bar_plot(processed_data, 'Expenses', 'Name', 'Sex_at_birth', 'Female',
                                'Male', f'expenses_{year}', f'Top Ten Expenses in {year}', 
                                'Name', 'Expenses (CAD)')
        
        # create histogram for salaries split by gender
        create_histogram_plot_for_one_year(processed_data, min_remuneration, max_remuneration, 
                                           'Remuneration', 'Sex_at_birth', 
                                           f'Distribution of Salary by Gender {year}', 
                                           'Salary (CAD, in thousands)', 'Frequency', 
                                           f'salaries_by_gender_{year}',0.5,100)
        
        # create histogram for expenses split by gender
        create_histogram_plot_for_one_year(processed_data, min_expenses, max_expenses, 
                                           'Expenses', 'Sex_at_birth', 
                                           f'Distribution of Expenses by Gender {year}', 
                                           'Expenses (CAD)', 'Frequency', 
                                           f'expenses_by_gender_{year}',0.2,200)



if __name__ == "__main__":
    main()
