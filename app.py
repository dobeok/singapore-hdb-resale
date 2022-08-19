import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.set_page_config(
     page_title="Explore Singapore HDB",
     layout="wide",
     initial_sidebar_state="expanded",
)

columns = [
    'town',
    'flat_type',
    'storey_range',
    'floor_area_sqm',
    'flat_model',
    'resale_price',
    'postal',
    'latitude',
    'longitude',
    'building',
]

st.title('Explore Singapore Public Housing')

df = pd.read_csv('data/processed/cleaned_data.csv', usecols=columns)
df = df[df['latitude'].notnull()]
for col in ['latitude', 'longitude', 'resale_price', 'floor_area_sqm']:
    df[col] = pd.to_numeric(df[col])

df['resale_price'] = df['resale_price'] / 1000

price_min_val = 0
price_max_val = df['resale_price'].max().astype(int).round(-1).item() + 10


price_iq1 = df['resale_price'].quantile(.25).astype(int).item()
price_iq3 = df['resale_price'].quantile(.75).astype(int).item()


with st.sidebar:
    st.multiselect('Town(s)', options=sorted(df['town'].unique()), key='town_list', default='KALLANG/WHAMPOA')
    st.slider('Price range (thousands SGD)', value=(price_iq1, price_iq3), min_value=price_min_val, max_value=price_max_val, step=10, key='resale_range')

    st.multiselect('Flat type(s)', options=sorted(df['flat_type'].unique()), key='flat_type', default=df['flat_type'].unique())


    
    st.button('Show all clusters', disabled=True)
    st.button('Download image', disabled=True)


if len(st.session_state.flat_type):
    df = df[df['flat_type'].isin(st.session_state.flat_type)]

if len(st.session_state.town_list):
    df = df[df['town'].isin(st.session_state.town_list)]
    df = df[(st.session_state.resale_range[0] < df['resale_price']) & (df['resale_price'] < st.session_state.resale_range[1])]
    

    # st.map(df)

 



    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            
            latitude=1.285,
            longitude=103.831,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=df,
                get_position='[longitude, latitude]',
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            # pdk.Layer(
            #     'ScatterplotLayer',
            #     data=df,
            #     get_position='[longitude, latitude]',
            #     get_color='[200, 30, 0, 160]',
            #     get_radius=200,
            # ),
        ],
    ))