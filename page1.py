# CLAY YOO & LYDIA SCHWEITZER Assignment 3
# Yelp Data visualization using Streamlit

# IMPORTS **********************************************************************
import streamlit as st
import copy
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
import warnings
warnings.filterwarnings('ignore')
# SETTING PAGE CONFIG TO WIDE MODE

################################################################################
# DATA SETUP
################################################################################
bFile = 'DATA/business.csv' # business file
rFile, rDateCol = 'DATA/reviewCity.csv', 'date' # reviews file
#uFile, uDateCol = 'user.csv', 'yelping_since' # user file

#dataFile = bFile
@st.cache(allow_output_mutation=True)
def load_data(dataFile, dateCol = None, nrows = 400000):
    data = pd.read_csv(dataFile, nrows = nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    if dateCol in data.columns:
        data[dateCol] = pd.to_datetime(data[dateCol])
    return data

def app():
    # Load 6,000 rows of data into the dataframe.
    bData = load_data(bFile)
    rRawData = load_data(rFile, rDateCol, 6000)

    # add col to bData for int version of ratings
    bData['starsInt'] = [int(i) for i in bData['stars']]

    # parse rData to add year column
    rRawData['year'] = pd.DatetimeIndex(rRawData['date'],tz='UTC').year
    rData = copy.copy(rRawData)
    rData = rData.drop(columns = ['date'])
    # st.subheader('Dropped date col')
    # st.write(rData.head())

    yearSet = set(rData['year'])

    bSmallData = bData.head()
    rSmallData = rData.head()
    #uSmallData = uData.head()

    ################################################################################
    # Titles and Information
    ################################################################################
    st.title('Explore City-Wide Restaurant Reviews')
    st.subheader('Check out the ratings of restaurants in Pittsburgh and other major cities, their reviews, and what they have to offer.')
   
    ################################################################################
    # Maps
    ################################################################################
    # MAP VISUALIZATION
    st.write('Select one of the three sentiments below to see the concentration of each overtime:')
    # break apart data into city specific data
    pittsburghData = bData.loc[bData['city'] == 'Pittsburgh']
    montrealData = bData.loc[bData['city'] == 'Montréal']
    clevelandData = bData.loc[bData['city'] == 'Cleveland']
    torontoData = bData.loc[bData['city'] == 'Toronto']

    st.header('City Restaurant Data')

    # slider and data from user input
    #st.map(bData)
    selectedStars = st.sidebar.slider('Filter maps by selecting ratings:', 0, 5, (0,5))
    filteredDataP = pittsburghData[(pittsburghData['starsInt'] >= selectedStars[0]) & (pittsburghData['starsInt'] <= selectedStars[1])]
    filteredDataM = montrealData[(montrealData['starsInt'] >= selectedStars[0]) & (montrealData['starsInt'] <= selectedStars[1])]
    filteredDataC = clevelandData[(clevelandData['starsInt'] >= selectedStars[0]) & (clevelandData['starsInt'] <= selectedStars[1])]
    filteredDataT = torontoData[(torontoData['starsInt'] >= selectedStars[0]) & (torontoData['starsInt'] <= selectedStars[1])]



    # PREFERENCE OF FILTERED DATA
    # initiate bar chart below maps
    starsBarP = barChart = alt.Chart(pittsburghData,title='Pittsburgh Restaurant Rating').mark_bar().encode(
        alt.X('count():Q', title = 'Number of reviews'),
        alt.Y('starsInt:N', title = 'Stars Rated'),
        alt.Color('starsInt:Q', legend = None)
        )

    starsBarM = barChart = alt.Chart(montrealData,title='Montreal Restaurant Rating').mark_bar().encode(
        alt.X('count():Q', title = 'Number of reviews'),
        alt.Y('starsInt:N', title = 'Stars Rated'),
        alt.Color('starsInt:Q', legend = None)
        )

    starsBarC = barChart = alt.Chart(clevelandData,title='Cleveland Restaurant Rating').mark_bar().encode(
        alt.X('count():Q', title = 'Number of reviews'),
        alt.Y('starsInt:N', title = 'Stars Rated'),
        alt.Color('starsInt:Q', legend = None)
        )

    starsBarT = barChart = alt.Chart(torontoData,title='Toronto Restaurant Rating').mark_bar().encode(
        alt.X('count():Q', title = 'Number of reviews'),
        alt.Y('starsInt:N', title = 'Stars Rated'),
        alt.Color('starsInt:Q', legend = None)
        )

    #CONFIGURE LAYOUT
    # first 2 maps
    col1, col2 = st.beta_columns(2)

    col1.subheader('Pittsburgh')
    col1.map(filteredDataP)
    col1.write(starsBarP)

    col2.subheader('Montreal')
    col2.map(filteredDataM)
    col2.write(starsBarM)

    # second 2 maps
    col3, col4 = st.beta_columns(2)

    col3.subheader('Cleveland')
    col3.map(filteredDataC)
    col3.write(starsBarC)

    col4.subheader('Toronto')
    col4.map(filteredDataT)
    col4.write(starsBarT)
    
    ################################################################################
    # Exploratory Visuals
    ################################################################################
    # PREFERENCE OVER TIME
    rDataFiltered = copy.copy(rData)
    cola, colb, colc = st.beta_columns(3)

    pref = 'neu'
    prefTitle = 'Neutral '
    st.subheader('View colorized sentiment overtime.')
    st.write('Select review type to filter preference overtime')

    if cola.button('Negative Reviews'):
        #rDataFiltered = rDataFiltered[rDataFiltered['neg']]
        pref = 'neg'
        prefTitle = 'Negative '
    if colb.button('Positive Reviews'):
        #rDataFiltered = rDataFiltered[rDataFiltered['pos']]
        pref = 'pos'
        prefTitle = 'Positive '
    if colc.button('Neutral Reviews'):
        #rDataFiltered = rDataFiltered[rDataFiltered['neu']]
        pref = 'neu'
        prefTitle = 'Neutral '

    st.write('Preference Over Time:')
    preference = alt.Chart(rDataFiltered, title = 'Preference Over Time').mark_circle(
        strokeWidth=2
    ).encode(
        alt.X('year:N', title = 'Date', axis=alt.Axis(labelAngle=0)),
        alt.Y('bcity:N', title = 'City'),
        alt.Size('count():Q',
            scale=alt.Scale(range=[0, 4000]),
            legend=alt.Legend(title='Number of Reviews')),
        #alt.Opacity(pref, type = 'quantitative', aggregate = 'mean'),
        alt.Stroke('bcity:N', legend = None),
        alt.Color(pref, type = 'quantitative', aggregate = 'mean'),
        alt.Tooltip('neg:Q', aggregate = 'mean')
    ).properties(
        height=440,
        width=800
    )

    # map total average pref reviews over time
    totalPreference = alt.Chart(rDataFiltered, title= prefTitle + 'Over Time').mark_area(
        opacity=0.8,
        color='black'
    ).encode(
        alt.X('year:O', axis=alt.Axis(labelAngle=0), title = 'Year'),
        alt.Y(pref, type = 'quantitative', title = prefTitle + 'Sentiment Average')
    ).properties(
        height=150,
        width = 800
    )

    st.write(preference & totalPreference)
