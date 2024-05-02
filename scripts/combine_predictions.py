

import click

@click.command
def main():

    # Collect all the data together
    pop_df_complete = pd.concat([pop_df_predictions, pop_df_needs_predictions]).drop(columns = ['First name at birth','index'])


    pop_df_complete.loc[pop_df_complete['Accuracy'] < 0.8,'Sex at birth'] = ""

    pop_df_complete.loc[(pop_df_complete['First Name'] == "Lakshmi") & (pop_df_complete['Last Name'] == "Yatham"),'Sex at birth'] = "Male"
    pop_df_complete.loc[(pop_df_complete['First Name'] == "Santa") & (pop_df_complete['Last Name'] == "Ono"),'Sex at birth'] = "Male"
    pop_df_complete.loc[(pop_df_complete['First Name'] == "Ali") & (pop_df_complete['Last Name'] == "Lazrak"),'Sex at birth'] = "Male"
    pop_df_complete.loc[(pop_df_complete['First Name'] == "Jan") & (pop_df_complete['Last Name'] == "Bena"),'Sex at birth'] = "Female"

    # export dataset
    pop_df_complete.to_excel('/Users/jadebouchard/Desktop/UBC Salaries/ubc_salary_deparment_gender_all.xlsx', index = False)

if __name__ == "__main__":
    main()