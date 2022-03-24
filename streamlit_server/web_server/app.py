import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import requests
import base64
import os
import sys
import subprocess

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'geopy'])
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

API_URL = 'http://2e58-34-74-102-167.ngrok.io/event'

txt = st.text_input('Location', '')

df_catalog = pd.read_csv('./catlog_data.csv')
images_dir = 'images/'

def get_coordinates(location):
    # initialize Nominatim API 
    geolocator = Nominatim(user_agent="geoapiExercises")
    location_area = geolocator.geocode(location)
    return location_area.latitude, location_area.longitude

def get_event_id(lat,long):
    max = 10000000

    for i in range(0, len(df_catalog)):
        targ = (df_catalog.at[i, 'llcrnrlat'], df_catalog.at[i, 'llcrnrlon'])
        val = geodesic((lat,long), targ).miles
        #print(val)
        if (val < max and val < 200):
            max = val
            event_id = df_catalog.at[i, 'event_id']

    if (max == 10000000):
        print("Not Found")
    else:
        print("Shortest distance: ", max, "\nEvent ID: ", event_id)

    return event_id




if st.button('Submit'):
    lat,long = get_coordinates(txt)
    event_id = get_event_id(lat,long)
    st.write(event_id)
    params = {"idx_id": str(event_id)[-2:]}
    r = requests.get(API_URL,params=params)
    try:
        r_json = r.json()
        if r_json:
            image_b64 = r_json.get('data')
            with open(os.path.join(images_dir, 'image.png'), "wb") as file:
                file.write(base64.b64decode(image_b64))

            st.image(os.path.join(images_dir, 'image.png'))
    except:
        st.write(f'No records found for {txt}')




