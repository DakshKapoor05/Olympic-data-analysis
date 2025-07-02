import pandas as pd
import numpy as np


def preprocessor():
    df = pd.read_csv('athlete_events.csv')
    region_df = pd.read_csv('noc_regions.csv')

    #filtering for summer
    df = df[df['Season']=='Summer']
    #merge w region_df
    df = df.merge(region_df, on='NOC', how='left')
    #dropping duplicates
    df.drop_duplicates(inplace=True)
    #one hot encoding medals
    df = pd.concat([df,pd.get_dummies(df['Medal'])], axis=1)

    return df


