# -*- coding: utf-8 -*-
# Copyright 2018-2019 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pickle
import numpy as np
from os import path
import pandas as pd
import altair as alt
import pydeck as pdk
import streamlit as st
from DATA.zipcodes import CLEVELAND_ZIPCODES, MONTREAL_ZIPCODES, \
    PITTSBURGH_ZIPCODES, TORONTO_ZIPCODES

FILTERS_TO_CHOOSE = ['good_for_groups', 'wifi',
       'good_for_dancing', 'good_for_kids', 'karaoke', 'jazz', 'dj', 'live',
       'romantic', 'casual', 'trendy', 'classy', 'upscale']

#DATA_URL = (
#    "http://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"
#)
DATA_DIR = "DATA"
CITIES = ["Montréal", "Pittsburgh", "Toronto", "Cleveland"]
CITY2ZIPCODE = dict(
    Montréal=MONTREAL_ZIPCODES,
    Toronto=TORONTO_ZIPCODES,
    Pittsburgh=PITTSBURGH_ZIPCODES,
    Cleveland=CLEVELAND_ZIPCODES
    )


def round_(x):
    return round(x, 4)


@st.cache()
def load_data(filename):
    data = pd.read_csv(path.join(DATA_DIR, filename), index_col=None)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    if "date" in data:
        data["date"] = pd.to_datetime(data["date"], errors="coerce")
        data = data[~pd.isnull(data["date"])] # remove null
        # remove timezone
        data["date"] = data["date"].apply(lambda x: x.replace(tzinfo=None))
    return data


def map(data, display_by, second, lat, lon, zoom):
    if len(data):
        #data["tmp_stars"] = data["stars"] * 50
        data = data[["name", "address", "stars", "review_count",
                     "longitude", "latitude"]].dropna()
        data["tmp_stars"] = data["stars"]
        data["tmp_stars"] = data["tmp_stars"].apply(lambda x: 0 if x <= 2 else x)
        data["tmp_stars"] = data["tmp_stars"].apply(lambda x: 1 if 2 < x <= 3 else x)
        data["tmp_stars"] = data["tmp_stars"].apply(lambda x: 2 if 3 < x <= 4 else x)
        column_layer = pdk.Layer(
            "ColumnLayer",
            data=data,
            get_position=["longitude", "latitude"],
            #get_elevation="review_count",
            get_elevation=display_by,
            elevation_scale=200 if display_by == "stars" else 10,
            radius=50,
            #get_fill_color=["stars * 0.1", "stars * 0.5", "stars", 20],
            get_fill_color=(["255 - review_count", "255 - review_count",  230, 230]
                            if second == "review_count"
                            else ["255 - 50 * tmp_stars", "255 - 50 * tmp_stars", 230, 230]),
            pickable=True,
            auto_highlight=True,
        )
        tooltip = {
            "html": "Name: <b>{name}</b><br />Address: <b>{address}</b><br />Star: <b>{stars}</b><br />#Reviews: <b>{review_count}</b>",
            "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
            }

        st.write(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={
                "latitude": lat,
                "longitude": lon,
                "zoom": zoom,
                "pitch": 50,
            },
            tooltip=tooltip,
            layers=[column_layer]))

def app():
    st.title("Restaurant Distribution and Sentimenet Analysis")

    business_data = load_data("business.csv")
    top_business_data = load_data("top_business.csv")
    review_data = load_data("review.csv")

    # CREATING FUNCTION FOR MAPS
    ####
    # WIDGETS (on the sidebar)
    ####
    display_by = st.sidebar.radio("Select the variable to display with",
                                  ["review_count", "stars"])
    second = "stars" if display_by == "review_count" else "review_count"
    star_range = st.sidebar.slider("Select minimum star (inclusive)", 0, 5, (0, 5))
    price_range = st.sidebar.slider("Price range",
                                    0, 5, (1, 3))
    city = st.sidebar.radio("Select the city you want to view", CITIES)

    # FIRST ROW
    row1_1, row1_2 = st.beta_columns((1, 2))
    # FIRST ROW
    row2_1, row2_2, row2_3 = st.beta_columns((1, 1, 2))

    filters_selected = st.sidebar.multiselect("Choose filters to apply",
                                      FILTERS_TO_CHOOSE)
    zipcodes_selected = st.sidebar.multiselect("Choose zipcode to show",
                                       CITY2ZIPCODE[city])
    if not len(zipcodes_selected):
        zipcodes_selected = CITY2ZIPCODE[city]

    # filter data by postal_code, price_range and stars
    business_data = business_data[business_data["postal_code"].isin(zipcodes_selected)]
    for filter in filters_selected:
        business_data = business_data[business_data[filter]]
    business_data = business_data[(business_data["price_range"] >= price_range[0]) &
                                  (business_data["price_range"] <= price_range[1])]
    business_data = (business_data[(business_data["stars"] >= star_range[0]) &
                                   (business_data["stars"] <= star_range[1])]
                     .sort_values([display_by, second], ascending=False))

    # do the same for top_business_data
    top_business_data = \
        top_business_data[top_business_data["postal_code"].isin(zipcodes_selected)]
    for filter in filters_selected:
        top_business_data = top_business_data[top_business_data[filter]]
    top_business_data = \
        top_business_data[(top_business_data["price_range"] >= price_range[0]) &
                          (top_business_data["price_range"] <= price_range[1])]
    top_business_data = \
        (top_business_data[(top_business_data["stars"] >= star_range[0]) &
                           (top_business_data["stars"] <= star_range[1])]
         .sort_values([display_by, second], ascending=False))

    sentiment_success = False
    with row1_1:
        st.write(f"**Top 20 Restaurants in {city}**")
        st.write(top_business_data[["name", "address", "stars", "review_count"]]
                 .head(20).reset_index(drop=True))

        restaurant_name = st.text_input("Choose the restaurant you want to analyze")
        restaurant_id = top_business_data[top_business_data["name"] ==
                                      restaurant_name]["business_id"]
        if len(restaurant_id):
            restaurant_id = restaurant_id.iloc[0]
            review_data = review_data[review_data["business_id"] == restaurant_id]
            review_count = \
                (top_business_data[top_business_data["business_id"] == restaurant_id]
                 ["review_count"].iloc[0])
            if np.isnan(review_data["pos"].mean()):
                st.write(
                    f"""
                    Oh, No! **{restaurant_name}** sentiment is not available. \n
                    Please try out a different restaurant!
                    """)
            else:
                st.write(
                    f"""
                    **{restaurant_name}** has {review_count} reviews\n
                    with **{round_(review_data['pos'].mean())}** avg. **positive** sentiment\n
                    with **{round_(review_data['neg'].mean())}** avg. **neutral** sentiment\n
                    with **{round_(review_data['neu'].mean())}** avg. **negative** sentiment\n
                    """)
                sentiment_success = True

    midpoint = (business_data["latitude"].mean(), business_data["longitude"].mean())
    with row1_2:
        st.write(
        """
        # Restaurants in 4 Major Cities in North America
        ##
        """)
        map(business_data, display_by, second, midpoint[0], midpoint[1], 11)

    if sentiment_success:
        with open("model/lr_model.pkl", "rb") as r_obj:
            model = pickle.load(r_obj)

        coef = model.coef_
        with row2_1:
            what = st.radio("Choose the sentiment to analyze",
                            ["pos", "neu", "neg"])
        with row2_2:
            delta = st.text_input("Choose the average amount to change (e.g. -0.2, +0.1)")
            try:
                delta = float(delta)
            except:
                if delta != "":
                    st.write("Invalid value is given as the average amount to change.")
                return

        sign = "decreases" if delta < 0 else "increases"
        delta = abs(delta)

        if what == "pos":
            w = coef[-3]
        elif what == "neu":
            w = coef[-2]
        else:
            w = coef[-1]

        rating = \
            (business_data[business_data["business_id"] == restaurant_id]
             ["stars"].iloc[0])
        if sign == "decreases":
            rating = max(0, rating + w * delta)
        else:
            rating = min(5.0, rating + w * delta)

        with row2_3:
            st.write(
                f"""
                If {restaurant_name} {sign} {what} sentiment by {delta},
                it's average rating will reach {rating}!!
                """)

        st.altair_chart(alt.Chart(review_data)
            .mark_line(
                interpolate='step-after',
            ).encode(
                x=alt.X("date:T", scale=alt.Scale(nice=False)),
                y=alt.Y("pos:Q"),
                tooltip=["date", "pos"]
            ).configure_mark(
                opacity=0.5,
                color='red'
            ), use_container_width=True)

        st.altair_chart(alt.Chart(review_data)
            .mark_line(
                interpolate='step-after',
            ).encode(
                x=alt.X("date:T", scale=alt.Scale(nice=False)),
                y=alt.Y("neu:Q"),
                tooltip=["date", "neu"]
            ).configure_mark(
                opacity=0.5,
                color='red'
            ), use_container_width=True)

        st.altair_chart(alt.Chart(review_data)
            .mark_line(
                interpolate='step-after',
            ).encode(
                x=alt.X("date:T", scale=alt.Scale(nice=False)),
                y=alt.Y("neg:Q"),
                tooltip=["date", "neg"]
            ).configure_mark(
                opacity=0.5,
                color='red'
            ), use_container_width=True)
