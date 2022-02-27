import os
import time

import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from language_check import check_language


def create_col(df, col):
    df[col] = 'None'
    df[col] = df['words'].apply(check_language)
    
    return df


def pie(fig, row, col, x, y):
    fig.add_trace(
        go.Pie(labels=x, values=y),
        row=row, col=col
    )

    
def histogram(fig, row, col, x, y):
    fig.add_trace(
        go.Bar(x=x, y=y),
        row=row, col=col
    ) 

def show_stats(df, col_name, save=False, title='Stats'):
    fig = make_subplots(rows=1, cols=2, specs=[
        [{"type": "domain"}, {"type": "xy"}],
     ])
    
    series = df[col_name].value_counts()
    x= series.index
    y= series.values
    
    pie(fig, 1, 1, x, y)
    histogram(fig, 1, 2, x, y)
    
    fig.update_layout(height=400, width=800, title_text=title)
    fig.show()
    
    if save:
        c_time = time.strftime("%Y%m%d-%H%M%S")
        save_stats(fig, c_time)

        
def save_stats(fig, time):
    path_name = 'Stat_Results/' 
    
    if not os.path.exists(path_name):
        os.mkdir(path_name)
    
    fig_name = path_name + time + '.png'
    fig.write_image(fig_name)

    
# Works on csv
def show_lang_stats(path, save=False, title='Data language'):
    df = pd.read_csv(path)
    df = create_col(df, 'lang')
    
    show_stats(df, 'lang', save=save, title=title)   
    return df