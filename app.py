import os
import streamlit as st
import requests
import pandas as pd


# Define the base URI of the API
#   - Potential sources are in `.streamlit/secrets.toml` or in the Secrets section
#     on Streamlit Cloud
#   - The source selected is based on the shell variable passend when launching streamlit
#     (shortcuts are included in Makefile). By default it takes the cloud API url
if 'API_URI' in os.environ:
    BASE_URI = st.secrets[os.environ.get('API_URI')]
else:
    BASE_URI = st.secrets['cloud_api_uri']
# Add a '/' at the end if it's not there
BASE_URI = BASE_URI if BASE_URI.endswith('/') else BASE_URI + '/'
# Define the url to be used by requests.get to get a prediction (adapt if needed)
url = BASE_URI + 'predict'

# Just displaying the source for the API. Remove this in your final version.
# st.markdown(f"Working with {url}")

# st.markdown("Now, the rest is up to you. Start creating your page.")

"""
Version for baseline model
"""

# TODO: ADD TITLES AND INTRODUCTION

st.title('How Happy Are You?')
st.header('Answer the questions below to find out!')


# TODO: REQUEST USER INPUT
## Here we would like to add some controllers in order to ask the user to select their responses


# make it so that one question appears at a time - use session state / cache data(resource)


# TODO: Call the API using the user's input
#   - url is already defined above
#   - create a params dict based on the user's input
#   - finally call your API using the requests package

with st.form(key='params_for_api'):

    cntry  = st.selectbox('What is your country:', # make DICT? (for easier readability)
                      ('AL', 'AT', 'BE', 'BG', 'CH', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 'FR', 'GB',
                       'GE', 'GR', 'HR', 'HU', 'IE', 'IL', 'IS', 'IT', 'LT', 'LU', 'LV', 'ME', 'MK', 'NL',
                       'NO', 'PL', 'RO', 'RS', 'RU', 'SE', 'SI', 'SK', 'TR', 'UA', 'XK'))

    gndr = st.radio('What is your gender:',
                    ['Male', 'Female', 'Prefer not to say'])
    gndr_mapping = {
        "Male": 1,
        "Female": 2,
        "Prefer not to say": 9
    }
    gndr = gndr_mapping[gndr]

    sclmeet = st.slider('How often meet with friends, relatives, colleagues:', # include explanation labels
                        min_value=1, max_value=7, step=1)

    inprdsc = st.selectbox('How many people with whom you can discuss intimate and personal matters:',
                            ('None', '1', '2', '3', '4-6', '7-9', '10 or more')) # THE CORRESPONDING VALUES ARE 0-6
    inprdsc_mapping = {
        'None': 0,
        '1': 1,
        '2': 2,
        '3': 3,
        '4-6': 4,
        '7-9': 5,
        '10 or more': 6
    }
    inprdsc = inprdsc_mapping[inprdsc]

    sclact = st.selectbox('Take part in social activites compared to others of same age:',
                            ('Much less than most', 'Less than most', 'About the same', 'More than most', 'Much more than most'))
    sclact_mapping = {
        'Much less than most': 1,
        'Less than most': 2,
        'About the same': 3,
        'More than most': 4,
        'Much more than most': 5
    }
    sclact = sclact_mapping[sclact]

    health = st.number_input('Subjective general health:')
    rlgdgr = st.number_input('How religious are you:')
    dscrgrp = st.number_input('Member of a group discriminated against in this country:') # 2 buttons y/n
    ctzcntr = st.number_input('Citizen of country:') # 2 buttons y/n
    brncntr = st.number_input('Born in country:') # 2 buttons y/n
    # assign number value to buttons
    happy = st.number_input('How happy are you:')

    st.form_submit_button('Make prediction')

params = dict(
    cntry=cntry,
    gndr=gndr,
    sclmeet=sclmeet,
    inprdsc=inprdsc,
    sclact=sclact,
    health=health,
    rlgdgr=rlgdgr,
    dscrgrp=dscrgrp,
    ctzcntr=ctzcntr,
    brncntr=brncntr,
    happy=happy)

#wagon_cab_api_url = 'https://taxifare.lewagon.ai/predict'
response = requests.get(url, params=params)

prediction = response.json()

pred = prediction#['happy'] # STATE OF HAPPINESS

st.text(pred)

# TODO: retrieve the results
#   - add a little check if you got an ok response (status code 200) or something else
#   - retrieve the prediction from the JSON


# TODO: display the prediction in some fancy way to the user


# TODO: [OPTIONAL] maybe you can add some other pages?
#   - some statistical data you collected in graphs
#   - description of your product
#   - a 'Who are we?'-page



"""
Below is preparation for final model.
"""

# TODO PROCESS AND MAP FEATURES

params = dict(
    stfmjob=stfmjob,
    trdawrk=trdawrk,
    jbprtfp=jbprtfp,
    pfmfdjba=pfmfdjba,
    dcsfwrka=dcsfwrka,
    wrkhome=wrkhome,
    wrklong=wrklong,
    wrkresp=wrkresp,
    health=health,
    stfeco=stfeco,
    hhmmb=hhmmb,
    hincfel=hincfel,
    trstplc=trstplc,
    sclmeet=sclmeet,
    hlthhmp=hlthhmp,
    iphlppl=iphlppl,
    ipsuces=ipsuces,
    ipstrgv=ipstrgv,
    gndr=gndr,
    cntry=cntry,
    happy=happy # SHOULD THIS STILL BE HERE??
)

# FEATURES_DICT = {
#     "stfmjob":  "How satisfied are you in your main job",
#     "trdawrk":  "Too tired after work to enjoy things like doing at home, how often",
#     "jbprtfp":  "Job prevents you from giving time to partner/family, how often",
#     "pfmfdjba": "Partner/family fed up with pressure of your job, how often",
#     "dcsfwrka": "Current job: can decide time start/finish work",
#     "wrkhome":  "Work from home or place of choice, how often",
#     "wrklong":  "Employees expected to work overtime, how often",
#     "wrkresp":  "Employees expected to be responsive outside working hours, how often",
#     "health":   "Subjective general health",
#     "stfeco":   "How satisfied with present state of economy in country",
#     "hhmmb":    "Number of people living regularly as member of household",
#     "hincfel":  "Feeling about household's income nowadays",
#     "trstplc":  "Trust in the police",
#     "sclmeet":  "How often socially meet with friends, relatives or colleagues",
#     "hlthhmp":  "Hampered in daily activities by illness/disability/infirmity/mental problem",
#     "sclact":   "Take part in social activities compared to others of same age",
#     "iphlppl":  "Important to help people and care for others well-being",
#     "ipsuces":  "Important to be successful and that people recognise achievements",
#     "ipstrgv":  "Important that government is strong and ensures safety",
#     "gndr"   :  "Gender",
#     "cntry"  :  "Country",
#     "happy":    "Happiness"}
