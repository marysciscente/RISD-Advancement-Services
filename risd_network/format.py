'''
Mary Sciscente Bonilla
Database Management Intern
Rhode Island School of Design

Thie file contains functions to parse the RISD Network data according to the RE
database demands.
'''
import pandas as pd


def split_groups(data, sheet_name, column, file_type):
    '''
    Parameters
    ----------
    data: str, the name of the .xls file to read in.

    sheet_name: str, name of sheet in the given excel workbook.

    column: str, the name of the column containing the affiliations we want to
            split.

    file_type: a string representing the type of file (csv or xls)


    Behavior
    --------
    Reads in a file containing aggregated constituent affiliaton data and
    separates their affiliations into unique rows.

    Outputs
    -------
    report: csv, a csv file of unique user-group affiliations.

    '''

    # Read in the data
    if file_type == 'csv':
        df = pd.DataFrame(pd.read_csv(data))
    elif file_type == 'xls':
        df = pd.DataFrame(pd.read_excel(data, sheet_name=sheet_name))

    # Separate the groups
    new_values = []
    for row in range(0, len(df)):
        db_key = df.loc[row, 'Database key']
        group_list = df.loc[row, 'Groups']
        group_list = group_list.split(';')
        for group in group_list:
            affiliation = {'Database key': db_key, 'Group': group}
            new_values.append(affiliation)
    mod_df = pd.DataFrame(new_values)

    # Write to CSV and export
    split_name = str.split(data, ' ')
    date = str.split(split_name[2], '.xls')
    date = date[0]

    # Export as a csv
    mod_df.to_csv('RISD Network User Update ' + date + '.csv',
                  index=False)
