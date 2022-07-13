'''
Mary Sciscente Bonilla
Database Management Intern
Rhode Island School of Design
2022

Thie file contains functions to reformat event data according to the RE
database demands.
'''

import pandas as pd


def reformat(data, column):
    '''
    Parameters
    ----------
    data: str, the name of the .csv file to read in.

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

    # read in the data
    df = pd.DataFrame(pd.read_csv(data))

    # convert event start dates to DateTime objects
    df['Event Start Date'] = pd.to_datetime(df['Event Start Date'])

    # sort by date and group by person
    df = df.groupby('Name', sort=True).head(3)

    # Create new list of dictionaries with this data
    new_df = []

    # fix ID formatting error that cuts of preceding zeros
    const_ids = df['Constituent ID'].unique()

    const_names = df['Name'].unique()
    constituents = tuple(zip(const_ids, const_names))

    for (id, name) in constituents:
        constituent = {}
        count = 0

        const_df = df[df['Constituent ID'] == id]

        constituent['Constituent ID'] = str(id).zfill(7)
        constituent['Name'] = name

        events = const_df['Event Name']
        starts = const_df['Event Start Date']
        participation = tuple(zip(starts, events))

        for (date, event) in participation:
            count += 1

            if count == 1:
                constituent['Event Start Date 1'] = date
                constituent['Event Name 1'] = event
            elif count == 2:
                constituent['Event Start Date 2'] = date
                constituent['Event Name 2'] = event
            elif count == 3:
                constituent['Event Start Date 3'] = date
                constituent['Event Name 3'] = event

        new_df.append(constituent)

    # convert this list of dictionaries to a dataframe
    mod_df = pd.DataFrame(new_df)

    # Export as a csv
    mod_df.to_csv('New Event Formatting.csv', index=False)
