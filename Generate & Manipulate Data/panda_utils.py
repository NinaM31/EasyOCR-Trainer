import pandas as pd

from Data_cleaning.clean_utils import clean_text



def add_col_vals(df, col_name):
    df.insert(0, col_name,'')
    df[col_name] = df.index
    return df


def change_col_name(df, col, new_name):
    df.rename(columns={col: new_name}, inplace=True)
    return df


def drop_col(df, col):
    df.drop([col], axis=1, inplace=True)
    return df


def get_data(path):
    return pd.read_csv(path)


def display_data(df):
    display(df.head(10))
    print('Number of entries: ', len(df))

    
def check_nan(df, col): 
    nan = False
    nan_values = df[col].isna().sum()
    
    if nan_values > 0:
        print('Data cannot be cleaned there are nan values. Resolve the folowing values manually and try again.')
        display(df[df[col].isna()])
        nan = True
    return nan
 
    
def clean_df(df, col):
    if check_nan(df, col):
        return False, df
        
    print('data before cleaning')
    display_data(df)
    
    df[col] = df[col].apply(clean_text)    
    return True, df


def save_csv(df, header, path):
    df.to_csv(path, header=header, index=False)