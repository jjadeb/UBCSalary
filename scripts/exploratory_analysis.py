# author: Jade Bouchard
# date: 2024-05-02
#
# This script creates plots for the salary and gender data 
#
# Usage: python scripts/exploratory_analysis.py --predictions_input_file=data/gender_predictions/all_clean_gender_predictions.csv --plot_output_folder=plots 


import pandas as pd
import numpy
import matplotlib.pyplot as plt
from math import log10
import numpy as np
import seaborn as sns
import click

plt.rcParams.update({'font.size': 14, 'font.family': 'sans-serif'})
sns.set_theme(rc={'figure.figsize':(10,4)},font = "sans-serif")
pd.options.mode.chained_assignment = None  # copy warnings are not an issue for this script


def prepare_data_for_plot(data, year, salary_col, first_name_col, last_name_col, name_col):
    """
    Prepare data for plotting by filtering for a specific year, dividing salary by 1000, and
    adding a new column that contains first and last name.

    Parameters:
    -----------
    data : pandas.DataFrame
        The input DataFrame containing the data.
    year : int
        The specific year to filter the data.
    salary_col : str
        The name of the column containing salary information.
    first_name_col : str
        The name of the column containing first names.
    last_name_col : str
        The name of the column containing last names.
    name_col : str
            =The name of the column to be created containing both first and last names.

    Returns:
    processed_data : pandas.DataFrame
        Processed DataFrame with filtered data for the specified year, salary divided by 1000,
        and a new column containing combined first and last names for plotting.

    Example:

    data:
    | Year | Salary | First_Name | Last_Name |
    |------|--------|------------|-----------|
    | 2023 | 50000  | John       | Doe       |
    | 2023 | 60000  | Jane       | Smith     |
    | 2022 | 70000  | Alex       | Johnson   |

    prepare_data_for_plot(data, 2023, 'Salary', 'First_Name', 'Last_Name', 'Full_Name')

    processed_data:
    | Year | Salary | First_Name | Last_Name | Full_Name   |
    |------|--------|------------|-----------|-------------|
    | 2023 | 50     | John       | Doe       | John Doe    |
    | 2023 | 60     | Jane       | Smith     | Jane Smith  |

    """
    # filter for specific year
    processed_data = data[data["Year"] == year]
    # devide salary by 1000 to help with plot readability
    processed_data[salary_col] = processed_data[salary_col]/1000
    # create column with both names for bar plots
    processed_data[name_col] = processed_data[first_name_col] + ' ' + processed_data[last_name_col]
    return processed_data


def create_top_ten_bar_plot(data, numeric_column_name, categorical_column_name, colour_bar_column_name, colour_bar_opt1,
                            colour_bar_opt2, file_name, plot_title, x_axis_lab, y_axis_lab,plot_output_folder):
    '''Finds the ten largest values in the data and crates a bar plot of them. Categorical column values
    are put on the x axis. The bars are coloured by another categorical column.
    
    Parameters:
    -----------
    data : pandas.DataFrame
        The input DataFrame containing the data.
    numeric_column_name : str
        The name of the column containing numeric values to plot.
    categorical_column_name : str
        The name of the column containing categorical values to plot on the x-axis.
    colour_bar_column_name : str
        The name of the column to use for coloring bars.
    colour_bar_opt1 : str
        The first categorical value for coloring bars.
    colour_bar_opt2 : str
        The second categorical value for coloring bars.
    file_name : str
        The name of the file to save the plot.
    plot_title : str
        The title of the plot.
    x_axis_lab : str
        The label for the x-axis.
    y_axis_lab : str
        The label for the y-axis.
    plot_output_folder : str
        The folder to save the plot in.

    '''
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
    plt.savefig(f'{plot_output_folder}/bar_plots/top_ten_{file_name}.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_histogram_plot_for_one_year(data, min_value, max_value, numeric_col, category_col,
                                       plot_title, xlab, ylab, file_name, cut_off_factor, bins, 
                                       plot_output_folder):
    '''
    Create two overlapping histograms of female and male numeric data. Outliers will be cut off to 
    improve the clarity of the plots.

    Parameters:
    ------------
    data : pandas.DataFrame
        The input DataFrame containing the data.
    min_value : float
        The minimum value of the numeric data.
    max_value : float
        The maximum value of the numeric data.
    numeric_col : str
        The name of the column containing the numeric values to plot.
    category_col : str
        The name of the column containing the categorical values to divide the data by.
    plot_title : str
        The title of the plot.
    xlab : str
        The label for the x-axis.
    ylab : str
        The label for the y-axis.
    file_name : str
        String to include in the file name.
    cut_off_factor : float
        The factor by which to shorten the maximum value on the x-axis. Between 0 and 1.
    bins : int
        The number of bins for the histogram.
    plot_output_folder : str
        The folder to save the plot in.
    '''

    # Define bins
    bins = np.linspace(min_value, max_value, bins)

    # Separate data by gender
    female_expenses = data[data[category_col] == "Female"][numeric_col]
    male_expenses = data[data[category_col] == "Male"][numeric_col]

    # Create histogram plot
    plt.figure(figsize=(9, 5))
    plt.hist(male_expenses, bins, alpha=0.5, label='Male', color="#6495ED")
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
    plt.savefig(f'{plot_output_folder}/histogram_plots/histogram_of_{file_name}.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_summary_table(data, numeric_col1, numeric_col2):
    '''
    This function calculates summary statistics (mean, median, minimum, and maximum) for two 
    specified numeric columns in the DataFrame. Additionally, it extracts the minimum and maximum 
    values of each column.

    Parameters:
    -----------
    data : pandas.DataFrame
        DataFrame containing the data.
    numeric_col1 : str
        The name of the first numeric column.
    numeric_col2 : str
        The name of the second numeric column.

    Returns:
    --------
    data_summary : pandas.DataFrame
        Summary table containing mean, median, minimum, and maximum values of the 
        specified numeric columns.
    min_col1 : float
        Minimum value of numeric_col1.
    max_col1 : float
        Maximum value of numeric_col1.
    min_col2 : float
        Minimum value of numeric_col2.
    max_col2 : float
        Maximum value of numeric_col2.

    Example:
    --------
    data:
    | First_Name | Last_Name | Age | Income |
    |------------|-----------|-----|--------|
    | John       | Smith     | 35  | 60000  |
    | Emily      | Johnson   | 40  | 55000  |
    | Jessica    | Brown     | 30  | 48000  |

    create_summary_table(data, "Age", "Income")

    Returns:
    |           | Age              | Income            |
    |-----------|------------------|-------------------|
    | mean      | 35.00            | 54333.33           |
    | median    | 35.00            | 55000.00          |
    | min       | 30.00            | 48000.00          |
    | max       | 40.00            | 60000.00          |

    '''
    ## create summary data table and store min/max values
    data_summary = data[[numeric_col1,numeric_col2]].apply(
    {
        numeric_col1:["mean","median","min","max"],
        numeric_col2:["mean","median","min","max"]
    }
    ).map(lambda x: round(x, 2))

    max_col2 = data_summary.loc['max',numeric_col2]
    min_col2 = data_summary.loc['min',numeric_col2]
    max_col1 = data_summary.loc['max',numeric_col1]
    min_col1 = data_summary.loc['min',numeric_col1]
    return data_summary, min_col1, max_col1, min_col2, max_col2


def create_box_plots(data, numeric_col, categorical_col, xlab, ylab, title, file_name,plot_output_folder):
    '''
    Creates box plots to visualize the distribution of numeric data across different categories.
    Uses specific stylistic features.

    Parameters:
    -----------
    data : pandas.DataFrame
        The input DataFrame containing the data.
    numeric_col : str
        The name of the column containing numeric data to be plotted on the y-axis of the box plot.
    categorical_col : str
        The name of the column containing categorical data to be plotted on the x-axis of the box plot.
    xlab : str
        The label for the x-axis.
    ylab : str
        The label for the y-axis.
    title : str
        The title of the plot.
    file_name : str
        String to include in the file name.
    plot_output_folder : str
        The folder to save the plot in.
    '''
    plt.figure(figsize=(9, 5))
    sns.boxplot(
        data=data, x= numeric_col, y=categorical_col,
        hue = categorical_col,
        palette=[sns.xkcd_rgb["light blue"], sns.xkcd_rgb["light orange"]]
    )

    # Set labels and title
    plt.legend([],[], frameon=False)
    plt.xlabel(xlab , fontsize=14)
    plt.ylabel(ylab, fontsize=14)
    plt.title(title , fontsize=16)
    plt.savefig(f'{plot_output_folder}/box_plots/boxplot_of_{file_name}.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_line_plot(data, male_colour, female_colour, min_x, max_x, max_y, min_y,
                     title, xlab, ylab, file_name, plot_output_folder):
    '''
    Creates a line plot for median male and female data over time. 
    This function customizes the font sizes and styles for improved readability.

    Parameters:
    -----------
    data : pandas.DataFrame
        DataFrame containing the data with index representing time and columns 'Male' and 'Female' 
        representing median salary for males and females over time.
    title : str
        Title of the plot.
    xlab : str
        Label for the x-axis.
    ylab : str
        Label for the y-axis.
    male_colour : str
        Colour for the male line plot. 
    female_colour : str
        Colour for the female line plot.
    min_x : float
        Minimum value for the x-axis data. 
    max_x : float
        Maximum value for the x-axis data. 
    min_y : float
        Minimum value for the y-axis data. 
    max_y : float
        Maximum value for the y-axis data.
    file_name : str
        String to include in the file name.
    plot_output_folder : str
        Folder path to which we save the plot image.
    '''

    fig, ax = plt.subplots(figsize=(9, 5))

    # Define font sizes
    SIZE_DEFAULT = 14
    SIZE_LARGE = 16
    plt.rc("font", family="sans-serif")  # controls default font
    plt.rc("font", weight="normal")  # controls default font
    plt.rc("font", size=SIZE_DEFAULT)  # controls default text sizes
    plt.rc("axes", titlesize=SIZE_LARGE)  # fontsize of the axes title
    plt.rc("axes", labelsize=SIZE_LARGE)  # fontsize of the x and y labels
    plt.rc("xtick", labelsize=SIZE_DEFAULT)  # fontsize of the tick labels
    plt.rc("ytick", labelsize=SIZE_DEFAULT)  # fontsize of the tick labels

    # Plot median salary for males
    ax.plot(data.index, data['Male'], marker='o', label='Male', color=male_colour)


    # Plot median salary for females
    ax.plot(data.index, data['Female'], marker='o', label='Female', color=female_colour)


    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)

    # Hide the all but the bottom spines (axis lines)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)

    # Only show ticks on the left and bottom spines
    ax.yaxis.set_ticks_position("left")
    ax.xaxis.set_ticks_position("bottom")
    ax.spines["bottom"].set_bounds(min_x, max_x)

    plt.legend(title = "Guessed Gender")

    plt.ylim(min_y*1.2, max_y*1.2)
    plt.grid(True)
    plt.xticks(data.index)  # Ensure all years are shown on x-axis
    plt.tight_layout()
    plt.savefig(f'{plot_output_folder}/line_plots/lineplot_of_{file_name}.png', dpi=300, bbox_inches='tight')
    plt.close()


def find_change_over_years(data, numeric_col, numeric_str):
    '''
    Find changes in a numeric column over consecutive years.

    This function calculates the change in a numeric column over consecutive years for each individual 
    in the dataset. It computes both the absolute change and the percentage change.

    Parameters:
    -----------
    data : pandas.DataFrame
        DataFrame containing the data with columns 'First_Name', 'Last_Name', 'Year', 
        and the numeric column of interest.
    numeric_col : str
        The name of the numeric column for which changes are to be calculated.
    numeric_str : str
        String representation of the numeric column (e.g., 'salary') for column naming.

    Returns:
    --------
    result_df : pandas.DataFrame
        DataFrame containing columns 'First_Name', 'Last_Name', 'Sex_at_birth', 'transition_year', 
        '{numeric}_change_amount', and '{numeric}_change_percent' indicating the change in the 
        numeric column over consecutive years.

    Example:
    --------

    data:
    | First_Name | Last_Name | Year | Salary |
    |------------|-----------|------|--------|
    | John       | Smith     | 2019 | 50000  |
    | Emily      | Johnson   | 2020 | 60000  |
    | John       | Smith     | 2020 | 52000  |
    | Emily      | Johnson   | 2021 | 65000  |

    find_change_over_years(data, 'Salary', 'salary')

    result_df:
    | First_Name | Last_Name | Sex_at_birth | transition_year | salary_change_amount | salary_change_percent |
    |------------|-----------|--------------|-----------------|----------------------|-----------------------|
    | John       | Smith     | Male         | 2020            | 2000                 | 4.0                   |
    | Emily      | Johnson   | Female       | 2021            | 5000                 | 8.33                  |


    '''
    # looking at percentaage salary raises/decreases

    # Drop names that appear in the male and female datasets - since cannot determine the difference between the two
    sub_data = data.drop_duplicates(subset=['First_Name','Last_Name','Year'], keep = False)

    # Merge DataFrame with itself
    merged_df = sub_data.merge(sub_data, how='inner', on=['First_Name', 'Last_Name'])

    # Filter rows where years are consecutive
    merged_df = merged_df[merged_df['Year_y'] == merged_df['Year_x'] + 1]

    # Calculate salary change
    merged_df[f'{numeric_str}_change_amount'] = merged_df[f'{numeric_col}_y'] - merged_df[f'{numeric_col}_x']

    merged_df[f'{numeric_str}_change_percent'] = round(100*(merged_df[f'{numeric_col}_y'] - merged_df[f'{numeric_col}_x'])/merged_df[f'{numeric_col}_x'],2)

    merged_df['transition_year'] = merged_df['Year_y']

    # Select columns of interest
    result_df = merged_df[['First_Name', 'Last_Name', 'Sex_at_birth_x','transition_year', f'{numeric_str}_change_amount',f'{numeric_str}_change_percent']].rename(columns = {'Sex_at_birth_x':'Sex_at_birth'})
    
    return result_df

def find_median_data(data, year_col, numeric_col):
    '''
    Compute median values of a numeric variable grouped by year and gender.

    Parameters:
    -----------
    data : pandas.DataFrame
        The input DataFrame containing the data.
    year_col : str
        The name of the column containing the years.
    numeric_col : str
        The name of the column containing the numeric variable.

    Returns:
    --------
    median_data : pandas.DataFrame
        DataFrame containing median values of the numeric variable grouped by year and gender.
    max_median : float
        Maximum median value across all genders and years.
    min_median : float
        Minimum median value across all genders and years.

    Example:
    --------
    data:
    |   Year   |  Sex_at_birth  |  Income  |
    |----------|----------------|----------|
    |   2020   |     Female     |   5000   |
    |   2020   |     Male       |   6000   |
    |   2021   |     Female     |   5500   |
    |   2021   |     Male       |   6500   |
    |   2022   |     Female     |   6000   |
    |   2022   |     Male       |   7000   |
    |   2022   |     Male       |   5000   |
    |   2022   |     Male       |   6000   |

    median_data, max_median, min_median = find_median_data(data, "Year", "Income")

    median_data:
    |   Year   |   Female  |  Male  |
    |----------|-----------|--------|
    |   2020   |    5000   |   6000 |
    |   2021   |    5500   |   6500 |
    |   2022   |    6000   |   6000 |

    max_median: 6500
    min_median: 5000

    '''
    median_data = data.groupby([year_col, 'Sex_at_birth'])[numeric_col].median().unstack()
    max_median = max(max(median_data["Male"]),max(median_data["Female"]))
    min_median = min([min(median_data["Male"]),min(median_data["Female"]),0])
    return median_data, max_median, min_median


@click.command
@click.option("--predictions_input_file",type=str)
@click.option("--plot_output_folder",type=str)
def main(predictions_input_file, plot_output_folder):
    '''create bar plots, histograms, line plots, and box-plots to visualize the salary data 
    across genders'''
    
    ## read in data
    data = pd.read_csv(predictions_input_file)
  

    ## for each year create a bar plot of the top ten salaries and box plots of salaries and expenses
    years = data["Year"].unique().tolist()
    for year in years:
        processed_data = prepare_data_for_plot(data, year, 'Remuneration', 
                                            'First_Name',"Last_Name","Name")

        year = str(int(year))

        data_summary_year, min_remuneration, max_remuneration, min_expenses, max_expenses = create_summary_table(processed_data, "Remuneration", "Expenses")

        # create top ten bar plots for salaries
        create_top_ten_bar_plot(processed_data, 'Remuneration', 'Name', 'Sex_at_birth', 'Female',
                                'Male', f'salaries_{year}', f'Top Ten Salaries in {year}', 
                                'Name', 'Salary (CAD, in thousands)', plot_output_folder)
        
        # create top ten bar plots for expenses
        create_top_ten_bar_plot(processed_data, 'Expenses', 'Name', 'Sex_at_birth', 'Female',
                                'Male', f'expenses_{year}', f'Top Ten Expenses in {year}', 
                                'Name', 'Expenses (CAD)', plot_output_folder)
        
        # create histogram for salaries split by gender
        create_histogram_plot_for_one_year(processed_data, min_remuneration, max_remuneration, 
                                           'Remuneration', 'Sex_at_birth', 
                                           f'Distribution of Salary by Gender {year}', 
                                           'Salary (CAD, in thousands)', 'Frequency', 
                                           f'salaries_by_gender_{year}',0.5,100,plot_output_folder)
        
        # create histogram for expenses split by gender
        create_histogram_plot_for_one_year(processed_data, min_expenses, max_expenses, 
                                           'Expenses', 'Sex_at_birth', 
                                           f'Distribution of Expenses by Gender {year}', 
                                           'Expenses (CAD)', 'Frequency', 
                                           f'expenses_by_gender_{year}',0.2,200,plot_output_folder)
        
        # create box plots for salary split by gender
        create_box_plots(processed_data, 'Remuneration', 'Sex_at_birth', "\nSalary (CAD, in thousands)", 
                         "Guessed Gender", f"Salary Distribution by Gender in {year} \n", 
                         f'salary_by_gender_{year}',plot_output_folder)
        
        # create box plots for expenses split by gender
        create_box_plots(processed_data, 'Expenses', 'Sex_at_birth', "\nExpenses (CAD)", 
                         "Guessed Gender", f"Expenses Distribution by Gender in {year} \n", 
                         f'expenses_by_gender_{year}',plot_output_folder)
    
    # find the earliest and most recent year in the data
    min_year = min(data["Year"])
    max_year = max(data["Year"])
    
    # find the median values for each gender over the years (remuneration and expenses)
    median_salary, max_median_salary, min_median_salary = find_median_data(data, "Year", "Remuneration")
    median_expenses, max_median_expenses, min_median_expenses = find_median_data(data, "Year", "Expenses")

    # find the percentage and amount changes for salary over the years for each gender
    salary_change_data = find_change_over_years(data,"Remuneration","salary")
    median_salary_percent_change, max_median_salary_percent_change, min_median_salary_percent_change = find_median_data(salary_change_data, "transition_year", "salary_change_percent")
    median_salary_amount_change, max_median_salary_amount_change, min_median_salary_amount_change = find_median_data(salary_change_data, "transition_year", "salary_change_amount")
    salary_change_data.to_csv("data/test_salary_change.xlsx")

    # find the percentage and amount changes for expenses over the years for each gender
    expenses_change_data = find_change_over_years(data,"Expenses","expenses")
    median_expenses_percent_change, max_median_expenses_percent_change, min_median_expenses_percent_change = find_median_data(expenses_change_data, "transition_year", "expenses_change_percent")
    median_expenses_amount_change, max_median_expenses_amount_change, min_median_expenses_amount_change = find_median_data(expenses_change_data, "transition_year", "expenses_change_amount")


    # create line plot for median salary over time split by gender
    create_line_plot(median_salary, "#2B2F42", "#FF8C00", min_year, max_year, max_median_salary, min_median_salary,
                     'Median Salary by Gender \n', 'Year', 'Median Salary (CAD) \n', 
                     'median_salary_by_gender', plot_output_folder)
    
    # create line plot for median expenses over time split by gender
    create_line_plot(median_expenses, "#2B2F42", "#FF8C00", min_year, max_year, max_median_expenses, min_median_expenses,
                     'Median Expenses by Gender \n', 'Year', 'Median Expenses (CAD) \n', 
                     'median_expenses_by_gender', plot_output_folder)
    
    # create line plot for median salary percentage change over time split by gender
    create_line_plot(median_salary_percent_change, "#2B2F42", "#FF8C00", min_year + 1, max_year, 
                     max_median_salary_percent_change, min_median_salary_percent_change, 'Median Salary Percentage Change by Gender \n', 
                     'Year', 'Median Salary Change (%) \n', 'median_salary_percent_change_by_gender', 
                     plot_output_folder)
    
    # create line plot for median salary amount change over time split by gender
    create_line_plot(median_salary_amount_change, "#2B2F42", "#FF8C00", min_year + 1, max_year, 
                     max_median_salary_amount_change, min_median_salary_amount_change, 'Median Salary Amount Change by Gender \n', 
                     'Year', 'Median Salary Change (CAD) \n', 'median_salary_amount_change_by_gender', 
                     plot_output_folder)
    
    # create line plot for median expenses percentage change over time split by gender
    create_line_plot(median_expenses_percent_change, "#2B2F42", "#FF8C00", min_year + 1, max_year, 
                     max_median_expenses_percent_change, min_median_expenses_percent_change, 'Median Expenses Percentage Change by Gender \n', 
                     'Year', 'Median Expenses Change (%) \n', 'median_expenses_percent_change_by_gender', 
                     plot_output_folder)
    
    # create line plot for median expenses amount change over time split by gender
    create_line_plot(median_expenses_amount_change, "#2B2F42", "#FF8C00", min_year + 1, max_year, 
                     max_median_expenses_amount_change, min_median_expenses_amount_change, 'Median Expenses Amount Change by Gender \n', 
                     'Year', 'Median Expenses Change (CAD) \n', 'median_expenses_amount_change_by_gender', 
                     plot_output_folder)




if __name__ == "__main__":
    main()
