import pandas as pd
import numpy as np
import preprocessor

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region')[['Gold', 'Silver', 'Bronze']] \
        .sum().sort_values('Gold', ascending=False).reset_index()

    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country


def get_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0  # Indicates if we should NOT group by region

    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    else:  # both country and year are selected.
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Year',
                                                                                    ascending=True).reset_index()
    else:
        x = temp_df.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold',
                                                                                      ascending=False).reset_index()
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Count the top 15 athletes
    top_athletes = temp_df['Name'].value_counts().reset_index().head(15)
    top_athletes.columns = ['Name', 'Medal_Count']  # Rename columns properly

    # Merge to get sport and region info
    top_athletes = top_athletes.merge(df, on='Name', how='left')[['Name', 'Medal_Count', 'Sport', 'region']]

    # Drop duplicate names (in case the same athlete appeared in multiple sports/events)
    top_athletes = top_athletes.drop_duplicates('Name')

    # Reset index to remove 0, 30, 49, etc.
    top_athletes.reset_index(drop=True, inplace=True)

    return top_athletes


def year_wise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df


def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count')
    pt.fillna(0, inplace=True)  # <-- fill NaN with 0
    pt = pt.astype(int)

    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    # Count top 15 athletes
    top_athletes = temp_df['Name'].value_counts().reset_index().head(15)
    top_athletes.columns = ['Name', 'Medal_Count']  # Rename columns properly

    # Merge to get sport and region info
    top_athletes = top_athletes.merge(df, on='Name', how='left')[['Name', 'Medal_Count', 'Sport']]

    # Drop duplicate names (in case same athlete appeared in multiple sports/events)
    top_athletes = top_athletes.drop_duplicates('Name')

    # Reset index to remove 0, 30, 49, etc.
    top_athletes.reset_index(drop=True, inplace=True)

    return top_athletes


def weight_v_height(df,sport):

    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df1 = athlete_df[athlete_df['Sport'] == sport]
        return temp_df1
    else:
        return athlete_df


def men_v_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final


