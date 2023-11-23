import os
import pandas as pd

def loadcsv(path=None):
    """
    Load all csv files in the path into a single DataFrame.
    Only load files with the .csv extension.
    Convert specified datetime columns to datetime format.
    """
    if path is None:
        path = os.getcwd()  # if path is not specified, use current working directory

    csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
    dfs = []

    datetime_columns = ['Datetime', 'Expiration_Date']  # Specify the datetime columns to parse

    for file in csv_files:
        file_path = os.path.join(path, file)
        df = pd.read_csv(file_path, parse_dates=datetime_columns, infer_datetime_format=True)
        dfs.append(df)

    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        return None

df = loadcsv("E:/RoboAdvisor/newOptionData")

df.to_csv('merged_test.csv', index=False)
