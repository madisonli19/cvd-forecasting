import pandas as pd
import plotly.express as px
import json
from config import mapping_filepath

_mappings = None

def load_mappings():
    '''Load the mapping file only once and cache it'''
    global _mappings
    if _mappings is None:
        with open(mapping_filepath, 'r') as fp:
            _mappings = json.load(fp)
    return _mappings

def categorical_ct(df:pd.DataFrame, field:str):
    '''
    Chart the frequency of each category within a categorical field.

    Input: dataframe, field name, chart title, and axis titles
    Output: bar chart
    '''
    map_ = load_mappings()
    data = df[field].astype('str').replace(map_[field]).value_counts().to_dict()
    fig = px.bar(df, 
                x=data.keys(),
                y=data.values())
    return fig
    
def grouped_categorical_ct(df:pd.DataFrame, grouper:str, counter:str, colors:list=None):
    '''
    Chart two categorical variables, where one is a grouping condition 
    and the other is counted (frequency).
    Ex. Split data into those with and without heart disease. Then, 
    count how many men and women are in each group.

    Input: the dataframe, the name of the field to group by, and the 
    name of the field to count. Optional: list of bar colors in order
    Output: grouped bar chart
    '''
    map_ = load_mappings()

    data = df.groupby(grouper).agg(Count=(counter, 'value_counts')).reset_index()

    #ensures that bars appear in consistent order across charts
    grodataupdf = data.sort_values([counter],ascending=[False]) 
    
    data[grouper] = data[grouper].astype('str').replace(map_[grouper])
    data[counter] = data[counter].astype('str').replace(map_[counter])

    fig = px.bar(data, 
                x=grouper,
                y="Count",
                color_discrete_sequence=colors,
                color=counter,
                barmode='group')
    return fig