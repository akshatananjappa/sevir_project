from pydoc import locate
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import requests
import base64
import os
import sys
import subprocess
import traceback
import random

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'geopy'])
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

API_URL = os.environ.get('API_URL') + '/event'

txt = st.text_input('Location', '')

df_catalog = pd.read_csv('streamlit_server/web_server/catlog_data.csv')
images_dir = './'

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
        if (val < max and val < 100):
            max = val
            event_id = df_catalog.at[i, 'event_id']

    if (max == 10000000):
        print("Not Found")
    else:
        print("Shortest distance: ", max, "\nEvent ID: ", event_id)

    return max, event_id




# all cities below work
#houston
#adrian
#appleton
#omaha
#charlottesville

# all cities that don't work
#boston
#miami
#providence
#pawtucket
#chesapeake



import unittest

class TestWeatherMethods(unittest.TestCase):

    #dw
    def test_lesser_than_200(self):
        lat = 29.7589382
        long = -95.3676974
        max, event = get_event_id(lat,long)
        self.assertEqual(event, 792249)

    #dw - GeoPy 
    def test_get_coordinates_Non_City(self):
        location = "fasfas"
        coordinates = get_coordinates(location)
        self.assertEqual(coordinates, "None")

    #dw
    def test_front_end_input_non_exisiting_city(self):
        location = "Canton"
        coordinates = get_coordinates(location)
        self.assertEqual(coordinates, "None")

    #dw
    def test_front_end_input_numerical(self):
        location = "123"
        coordinates = get_coordinates(location)
        self.assertEqual(coordinates, "None")

    #dw
    def test_front_end_input_alphanumeric(self):
        location = "ball123"
        coordinates = get_coordinates(location)
        self.assertEqual(coordinates, "None")
    

    #dw
    def test_image_does_not_display(self):
        pass
        #any problem with plt.save(), image not displayed
    


    #w
    def test_greater_than_200(self):
        lat = 12.4124123
        long = -91.2532343
        max, event = get_event_id(lat,long)
        self.assertEqual(event, "Not Found")

    #w
    def test_get_coordinates_City(self):
        location = "Boston"
        coordinates = get_coordinates(location)
        self.assertEqual(coordinates, (42.3602534, -71.0582912))

    #w
    def test_get_event_id(self):
        lat = 42.3602534
        long = -71.0582912
        max, event = get_event_id(lat,long)
        self.assertEqual(event, 841365)

    #w
    def test_shortest_distance(self):
        lat = 42.3602534
        long = -71.0582912
        max, event = get_event_id(lat,long)
        self.assertEqual(max, 131.6285857763959)

    #w
    def test_front_end_input_exisiting_city(self):
        location = "Boston"
        coordinates = get_coordinates(location)
        max, event = get_event_id(lat,long)
        self.assertEqual(event, 841365)
        #image part can be added checking if the generated image matches the output image on the frontend




if st.button('Submit'):

    if txt == '' or txt.isnumeric() or txt.isalnum():
        # try to print an error message on frontend
        st.write("Wrong Input")

    else:
        lat,long = get_coordinates(txt)
        
    event_id = get_event_id(lat,long)

    st.write(event_id)
    #params = {"idx_id": str(event_id)[-2:]}
    params = {"idx_id": random.randrange(10,50)}
    r = requests.get(API_URL,params=params)
    try:
        r_json = r.json()
        if r_json:
            image_b64 = r_json.get('data')
            with open(os.path.join(images_dir, 'image.png'), "wb") as file:
                file.write(base64.b64decode(image_b64))

            st.image(os.path.join(images_dir, 'image.png'))
    except:
        print(traceback.format_exc())
        st.write(f'No records found for {txt}')





