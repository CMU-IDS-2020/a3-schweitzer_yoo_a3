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
# SETTING PAGE CONFIG TO WIDE MODE
st.beta_set_page_config(layout="wide")

################################################################################
# DATA SETUP
################################################################################
bFile = 'business.csv' # business file
rFile, rDateCol = 'reviewCity.csv', 'date' # reviews file
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

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
bData = load_data(bFile)
rRawData = load_data(rFile, rDateCol, 6000)
#uData = load_data(10000, uFile, uDateCol)
# Notify the reader that the data was successfully loaded.
# data_load_state.text("Done! (using st.cache)")

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
st.title('Restaurant Ratings!')
st.header('Check out the ratings of restaurants in Pittsburgh and other major cities, their reviews, and what they have to offer.')
################################################################################
# Inspect raw data
################################################################################
# def inspectData(title, data):
#     st.subheader(title)
#     st.write(data)
#     st.write("Data written!")

# st.title('Inspect Data')
# inspectData('Business', bSmallData)
# inspectData('Review', rSmallData)
# #inspectData('User', uSmallData)

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
# PREFERENCE OVER TIME 2
rDataFiltered = copy.copy(rData)
cola, colb, colc = st.beta_columns(3)

pref = 'neu'
prefTitle = 'Neutral '

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
methods2 = alt.Chart(rDataFiltered, title = 'Preference Over Time').mark_circle(
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
#st.write(methods2)

# map total average pref reviews over time
total = alt.Chart(rDataFiltered, title= prefTitle + 'Over Time').mark_area(
    opacity=0.8,
    color='black'
).encode(
    alt.X('year:O', axis=alt.Axis(labelAngle=0), title = 'Year'),
    alt.Y(pref, type = 'quantitative', title = prefTitle + 'Average Preference')
).properties(
    height=150,
    width = 800
)

st.write(methods2 & total)

################################################################################
# Maps 
################################################################################
# MAP VISUALIZATION
# break apart data into city specific data
pittsburghData = bData.loc[bData['city'] == 'Pittsburgh']
montrealData = bData.loc[bData['city'] == 'Montréal']
clevelandData = bData.loc[bData['city'] == 'Cleveland']
torontoData = bData.loc[bData['city'] == 'Toronto']

st.header('City Restaurant Data')

# slider and data from user input
#st.map(bData)
selectedStars = st.slider('Select ratings:', 0, 5, (0,5))
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