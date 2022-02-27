import os
import sys

sys.path.append(os.path.dirname("__file__") + '..')

import pandas as pd
import shutil

from dataset_stats import show_stats, create_col
from SynthData_generator.synth_generator import generate_data
from SynthData_generator.string_utils import get_strings_from_csv
from Data_cleaning.move_utils import move


def fill_synth(df, col, fill_dir, df_fill_from):
    max_val = find_max(df, col)
    headers = df_fill_from.columns
    col_dict = dict(df[col].value_counts())
    
    
    missing= {}
    df_dicts = {}
    df_from_dicts ={}
    df_synth_dict = []
    
    for key, value in col_dict.items():
        missing[key] = max_val - value
        df_dicts[key] = df[df[col] == key]
        df_from_dicts[key] = df_fill_from[df_fill_from[col] == key]
        
    for key, value in df_from_dicts.items():
        string = get_strings_from_csv(df_from_dicts[key])
        
        file_name = generate_data(string, size=64, output_dir=fill_dir, limit=missing[key], prefx=key)
        df_key = pd.read_csv(file_name, sep='\t', names=headers)
        df_key[col] = key
        df_synth_dict.append(df_key)
    
    return pd.concat(df_synth_dict, ignore_index=True)


def find_max(df, col):
    return max(df[col].value_counts())


def find_min(df, col):
    return min(df[col].value_counts())


def balance(path, col, save=False, show=False, title='Data', fill=False, fill_dir=None, df_fill_from=None, move_to=None):
    df = pd.read_csv(path)
    df = create_col(df, col)
    if fill:
        if fill_dir and df_fill_from:
            fill_from = pd.read_csv(df_fill_from)
            fill_from = create_col(fill_from, col)
    
            syn_df = fill_synth(df, col, fill_dir, fill_from) 
            file_dir, file_name = os.path.split(fill_dir)
            file_name = str(file_dir)+ '/'+ str(file_name) + '.csv'
           
            saved_df = syn_df.drop(columns=col)
            saved_df.to_csv(file_name, header=saved_df.columns, index=False)
            df_original = df.copy(deep=True)
            df = pd.concat([df, syn_df], ignore_index=True)
        else:
            sys.exit('You need to specify the fill directory (were images will be stored) and data frame to fill from')
    
    split = df[col].nunique()

    value_frac = find_min(df, col)
    print(f'{col} column will be split into {split}, each {value_frac}')

    df = df.groupby(col).sample(n=value_frac, random_state=1)
    
    if show:
        show_stats(df, col, save=save, title=title)
        
    if move_to:
        dir_name, basename = os.path.split(path)
        
        if fill:
            move(df_original, dir_name, move_to, basename)
        else:
            move(df, dir_name, move_to, basename)
        
        file_name =  move_to + '/balanced.csv'
        df.to_csv(file_name, header=df.columns, index=False)
        
    return df