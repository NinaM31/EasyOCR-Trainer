import os
import sys
sys.path.append(os.path.dirname("__file__") + '..')

from shutil import copy2

from panda_utils import save_csv, drop_col, display_data, change_col_name, add_col_vals



def add_extension(filename, x):
    extension = os.path.splitext(filename)[1]
    return str(x) + extension


def image_folder_stat(path, num):
    print(f'Number of files inside {path}: {num}')


def move_images(df, old_path_col, new_path_col, old_path, new_path):
    accepted = 0
    for _ in range(len(df)):
        old_file_name = df.iloc[accepted][old_path_col]
        new_file_name = df.iloc[accepted][new_path_col]
        
        copy2(old_path+'/' + old_file_name, new_path + '/' + new_file_name)
        accepted += 1
        
    
def move(df, old_path, new_path, labels_csv):
    temp = 'temp'
    col = 'filename'
    
    list_dir = os.listdir(old_path)
    image_folder_stat(old_path, len(list_dir))
    
    df = change_col_name(df, col, temp)
    df = add_col_vals(df, col) 
    
    df[col] = df.apply(lambda x: add_extension(x[temp], x[col]), axis=1)
    
    move_images(df, temp, col, old_path, new_path)
    
    df = drop_col(df, temp) 
    save_csv(df, df.columns, new_path+labels_csv)
    
    print('data after moving and cleaning')
    display_data(df)
    
    list_dir = os.listdir(new_path)
    image_folder_stat(new_path, len(list_dir))