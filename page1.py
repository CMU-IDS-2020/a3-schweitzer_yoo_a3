# CLAY YOO & LYDIA SCHWEITZER Assignment 3
# Yelp Data visualization using Streamlit
# code referenced from demo-uper-nyc-pickups
# https://github.com/streamlit/demo-uber-nyc-pickups/blob/master/streamlit_app.py

# IMPORTS **********************************************************************
import streamlit as st
import copy
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
import warnings
warnings.filterwarnings('ignore')

################################################################################
# DATA SETUP
################################################################################
bFile = 'DATA/business.csv' # business file
#rFile, rDateCol = 'DATA/reviewCity.csv', 'date' # reviews file
rFile, rDateCol = 'DATA/review.csv', 'date' # reviews file
#uFile, uDateCol = 'user.csv', 'yelping_since' # user file

#dataFile = bFile
@st.cache()
def load_data(dataFile, dateCol = None, nrows = 400000):
    data = pd.read_csv(dataFile, nrows = nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    if dateCol in data.columns:
        data[dateCol] = pd.to_datetime(data[dateCol])
    return data

def app():
    # Create a text element and let the reader know the data is loading.
    data_load_state = st.text('Loading data...')
    # Load 10,000 rows of data into the dataframe.
    bData = load_data(bFile)
    rRawData = load_data(rFile, rDateCol, 6000)
    #uData = load_data(10000, uFile, uDateCol)
    # Notify the reader that the data was successfully loaded.
    data_load_state.text("Done! (using st.cache)")

    # add col to bData for int version of ratings
    bData['starsInt'] = [int(i) for i in bData['stars']]

    # parse rData to add year column
    rRawData['year'] = pd.DatetimeIndex(rRawData['date'],tz='UTC').year
    rData = copy.copy(rRawData)
    rData = rData.drop(columns = ['date'])
    st.subheader('Dropped date col')
    st.write(rData.head())

    yearSet = set(rData['year'])

    bSmallData = bData.head()
    rSmallData = rData.head()
    #uSmallData = uData.head()

    ################################################################################
    # Titles and Information
    ################################################################################
    st.title('Restaurant Ratings!')
    st.header('Check out the ratings of restaurants in Pittsburgh and other major cities, their reviews, and what they have to offer.')
    ################################################################################
    # Inspect raw data
    ################################################################################
    def inspectData(title, data):
        st.subheader(title)
        st.write(data)
        st.write("Data written!")

    st.title('Inspect Data')
    #inspectData('Business', bSmallData)
    #inspectData('Review', rSmallData)
    #inspectData('User', uSmallData)

    # ################################################################################
    # # Test Visuals: BAR CHARTS
    # ################################################################################
    # st.title('Test Visuals')

    # # BAR CHARTS
    # st.subheader('Simple Bar Charts')
    # # specify x and y with (ordial, quantitative, nominal); 'name:O/Q/N'
    # def barChart(myTitle, data, x, y):
    #     barChart = alt.Chart(data,title=myTitle).mark_bar().encode(
    #     alt.X(x),
    #     alt.Y(y)
    #     )
    #     return barChart

    # businessBar = barChart('Business Reviews', bSmallData, 'review_count:Q','name:O')
    # reviewBar = barChart('Positive Reviews', rSmallData, 'pos:Q','business_id:O')
    # #userBar = barChart('Person Review Count', uSmallData, 'review_count:Q','name:O')
    # st.write(businessBar & reviewBar)

    # st.write("Bar charts done!")

    ################################################################################
    # Exploratory Visuals
    ################################################################################
    st.title('Exploratory Visuals')
    testChart = barChart = alt.Chart(rData,title='Test Chart').mark_bar().encode(
        alt.X('count():O'),
        alt.Y('year:N')
        )
    st.write(testChart)

    # PREFERENCE OVER TIME 2
    rDataFiltered = copy.copy(rData)

    if st.button('Negative Reviews'):
        rDataFiltered = rDataFiltered['neg']
    if st.button('Positive Reviews'):
        rDataFiltered = rDataFiltered['pos']
    if st.button('Neutral Reviews'):
        rDataFiltered = rDataFiltered['neu']

    st.write('Version 2 Try:')
    methods2 = alt.Chart(rDataFiltered, title = 'Preference Over Time').mark_circle(
        opacity=0.8,
        stroke='black',
        strokeWidth=1
    ).encode(
        alt.X('year:N', title = 'Date', axis=alt.Axis(labelAngle=0)),
        alt.Y('bcity:N', title = 'City'),
        alt.Size('neg:Q',
            scale=alt.Scale(range=[0, 4000]),
            legend=alt.Legend(title='Number of Reviews')),
        alt.Color('bcity:N', legend=None),
        alt.Tooltip('count()')
    ).properties(
        height=440,
        width=600
    )
    st.write(methods2)

    st.write('Version 3 Try:')
    methods3 = alt.Chart(rDataFiltered, title = 'Preference Over Time').mark_circle(
        opacity=0.8,
        stroke='black',
        strokeWidth=1
    ).encode(
        alt.X('year:N', title = 'Date', axis=alt.Axis(labelAngle=0)),
        alt.Y('bcity:N', title = 'City'),
        alt.Size('count():Q',
            scale=alt.Scale(range=[0, 4000]),
            legend=alt.Legend(title='Number of Reviews')),
        alt.Color('bcity:N', legend=None),
        alt.Tooltip('year')
    ).properties(
        height=440,
        width=600
    )
    st.write(methods3)

    ################################################################################
    # Maps
    ################################################################################
    # MAP VISUALIZATION
    st.subheader('Pittsburgh Restaurants')
    attributes = ["goodforkids", "bikeparking", "wifi", "restaurantdelivery", "restauranttakeout", "latenight", "breakfast", "lunch", "dinner"]
    st_ms = st.multiselect("Seach restaurant atributes", attributes)

    bDataFiltered = copy.copy(bData)

    for attr in st_ms:
        bDataFiltered = bData[bData[attr]]

    # break apart data into city specific data
    pittsburghData = bData.loc[bData['city'] == 'Pittsburgh']
    montrealData = bData.loc[bData['city'] == 'Montréal']
    clevelandData = bData.loc[bData['city'] == 'Cleveland']
    torontoData = bData.loc[bData['city'] == 'Toronto']

    # slider and data from user input
    #st.map(bData)
    selectedStars = st.slider('Select ratings:', 0, 5, (1,5))
    filteredDataP = pittsburghData[(pittsburghData['starsInt'] >= selectedStars[0]) & (pittsburghData['starsInt'] <= selectedStars[1])]
    filteredDataM = montrealData[(montrealData['starsInt'] >= selectedStars[0]) & (montrealData['starsInt'] <= selectedStars[1])]
    filteredDataC = clevelandData[(clevelandData['starsInt'] >= selectedStars[0]) & (clevelandData['starsInt'] <= selectedStars[1])]
    filteredDataT = torontoData[(torontoData['starsInt'] >= selectedStars[0]) & (torontoData['starsInt'] <= selectedStars[1])]

    st.subheader('City Restaurant Data')
    #st.map(filteredData)
    #st.write(filteredData)

    # PREFERENCE OF FILTERED DATA
    # initiate bar chart below maps
    starsBarP = barChart = alt.Chart(pittsburghData,title='Pittsburgh Restaurant Rating').mark_bar().encode(
        alt.X('count():Q', title = 'Number of reviews'),
        alt.Y('starsInt:N', title = 'Stars Rated')
        )

    starsBarM = barChart = alt.Chart(montrealData,title='Monteal Restaurant Rating').mark_bar().encode(
        alt.X('count():Q', title = 'Number of reviews'),
        alt.Y('starsInt:N', title = 'Stars Rated')
        )

    starsBarC = barChart = alt.Chart(clevelandData,title='Cleveland Restaurant Rating').mark_bar().encode(
        alt.X('count():Q', title = 'Number of reviews'),
        alt.Y('starsInt:N', title = 'Stars Rated')
        )

    starsBarT = barChart = alt.Chart(torontoData,title='Toronto Restaurant Rating').mark_bar().encode(
        alt.X('count():Q', title = 'Number of reviews'),
        alt.Y('starsInt:N', title = 'Stars Rated')
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
