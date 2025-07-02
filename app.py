import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import preprocessor,helper
from helper import medal_tally
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff

df = preprocessor.preprocessor()

st.sidebar.title('Summer Olympic Analysis')
st.sidebar.image(r'C:\Users\PC\OneDrive\Desktop\Olympic.png')

user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)

if user_menu == 'Medal Tally':

    st.sidebar.header('Medal Tally')
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.get_medal_tally(df, selected_year, selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')

    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in ' + str(selected_year) + ' Olympics')

    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + 'Overall Tally')

    elif selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + "'s Tally in " + str(selected_year) + ' Olympics')

    st.table(medal_tally)


if user_menu == 'Overall Analysis':
    no_of_olympics = df['Year'].unique().shape[0] - 1
    no_of_cities = df['City'].unique().shape[0]
    no_of_events = df['Event'].unique().shape[0]
    no_of_sports = df['Sport'].unique().shape[0]
    no_of_athletes = df['Name'].unique().shape[0]
    no_of_countries = df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1,col2,col3 = st.columns(3)

    with col1:
        st.header('Number of Olympics')
        st.title(no_of_olympics)

    with col2:
        st.header('Host Cities')
        st.title(no_of_cities)

    with col3:
        st.header('Number of Sports')
        st.title(no_of_sports)


    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Number of Events')
        st.title(no_of_events)
    with col2:
        st.header('Nations')
        st.title(no_of_countries)
    with col3:
        st.header('Number of Athletes')
        st.title(no_of_athletes)

    #st.markdown("<br><br>", unsafe_allow_html=True)
    st.write("\n")
    st.write("\n")
    st.write("\n")

    st.title('Number of Countries per Year')
    nations_per_year = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().sort_values().reset_index()
    nations_per_year.rename(columns={'count': 'No of Countries'}, inplace=True)
    nations_per_year.sort_values('Year', inplace=True)

    fig = px.line(nations_per_year,x='Year',y='No of Countries',width=800,height=500,markers=True)
    fig.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#bebbbb")
    st.plotly_chart(fig)

############

    st.title('Number of Events per Year')
    events_per_year = df.drop_duplicates(['Year', 'Event'])['Year'].value_counts().sort_values().reset_index()
    events_per_year.sort_values('Year', inplace=True)
    events_per_year.rename(columns={'count': 'No of Events'}, inplace=True)

    fig1 = px.line(events_per_year, x='Year', y='No of Events', width=800, height=500,markers=True)
    fig1.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#bebbbb")
    st.plotly_chart(fig1)

############

    st.title('Number of Sports per Year')
    sports_per_year = df.drop_duplicates(['Year', 'Sport'])['Year'].value_counts().sort_values().reset_index()
    sports_per_year.sort_values('Year', inplace=True)
    sports_per_year.rename(columns={'count': 'No of Sports'}, inplace=True)

    fig2 = px.line(sports_per_year, x='Year', y='No of Sports', width=800, height=500,markers=True)
    fig2.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#bebbbb")
    st.plotly_chart(fig2)

############

    st.title('Number of Athletes per Year')
    athletes_per_year = df.drop_duplicates(['Year', 'Name'])['Year'].value_counts().sort_values().reset_index()
    athletes_per_year.sort_values('Year', inplace=True)
    athletes_per_year.rename(columns={'count': 'No of Athletes'}, inplace=True)

    fig3 = px.line(athletes_per_year, x='Year', y='No of Athletes', width=800, height=500, markers=True)
    fig3.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#bebbbb")
    st.plotly_chart(fig3)

############

    st.title('Number of Events over time (Every Sport)')
    fig4,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig4)

############

    st.title('Most Successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)

    x = helper.most_successful(df,selected_sport)
    st.table(x)

##########################################################

if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df = helper.year_wise_medal_tally(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal', width=800, height=500, markers=True)
    fig.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#bebbbb")
    st.title('Medal Tally over the Years')
    st.plotly_chart(fig)

############

    st.title(selected_country + "'s Medal Heatmap")

    pt = helper.country_event_heatmap(df,selected_country)
    fig,ax = plt.subplots(figsize=(20,10))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

############

    st.title('Most Successful Athletes Country-wise')

    x = helper.most_successful_countrywise(df, selected_country)
    st.table(x)

##########################################################

if user_menu == 'Athlete-wise Analysis':

    st.title('Age Distribution')

    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=True, width=1200, height=600)

    st.plotly_chart(fig)

############

    x = []
    name = []

    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'shooting', 'Boxing', 'Taekwondo', 'cycling', 'Diving', 'canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

    for sport in famous_sports:
        temp_df = athlete_df[(athlete_df['Sport'] == sport) &
                             (athlete_df['Medal'] == 'Gold')]

        ages = temp_df['Age'].dropna()

        if not ages.empty:
            x.append(ages)
            name.append(sport)

    if x:
        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
        fig.update_layout(autosize=True, width=1200, height=600)
        st.title('Age Distribution wrt Sports (Gold Medalist)')
        st.plotly_chart(fig)
    else:
        st.warning("No valid age data found for gold medalists in the selected sports.")

############

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Weight v. Height Distribution')

    selected_sport = st.selectbox('Select a Sport', sport_list)

    temp_df = helper.weight_v_height(df,selected_sport)
    fig, ax = plt.subplots(figsize=(20,10))
    ax = sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=50)

    st.pyplot(fig)

############

    st.title('Men vs Women Participation over the Years')

    final = helper.men_v_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    st.plotly_chart(fig)









