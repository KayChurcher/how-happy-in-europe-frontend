import os
import streamlit as st
import requests
import pandas as pd


# Define the base URI of the API

if 'API_URI' in os.environ:
    BASE_URI = st.secrets[os.environ.get('API_URI')]
else:
    BASE_URI = st.secrets['cloud_api_uri']
# Add a '/' at the end if it's not there
BASE_URI = BASE_URI if BASE_URI.endswith('/') else BASE_URI + '/'
# Define the url to be used by requests.get to get a prediction (adapt if needed)
url = BASE_URI + 'predict'

# TODO EDIT URL FOR FINAL MODEL

"""
Below is preparation for final model.
"""

# ADD TITLES AND INTRODUCTION
st.title('How Happy Are You?')
st.header('Answer the questions below to find out!')


# Initialize session state
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0


# Gender and Country Questions - 2 on 1 page
if st.session_state.current_question == 0:
    with st.form("question_form"):
        cntry = st.selectbox('What country do you live in?',
                            ('AL  Albania', 'AT  Austria', 'BE  Belgium', 'BG  Bulgaria', 'CH  Switzerland', 'CY  Cyprus',
                            'CZ  Czechia', 'DE  Germany', 'DK  Denmark', 'EE  Estonia', 'ES  Spain', 'FI  Finland', 'FR  France', 'GB  United Kingdom',
                            'GE  Georgia', 'GR  Greece', 'HR  Croatia', 'HU  Hungary', 'IE  Ireland', 'IL  Israel', 'IS  Iceland',
                            'IT  Italy', 'LT  Lithuania', 'LU  Luxembourg', 'LV  Latvia', 'ME  Montenegro', 'MK  North Macedonia', 'NL  Netherlands',
                            'NO  Norway', 'PL  Poland', 'PT  Portugal', 'RO  Romania', 'RS  Serbia', 'RU  Russian Federation',
                            'SE  Sweden', 'SI  Slovenia', 'SK  Slovakia', 'TR  Turkey', 'UA  Ukraine', 'XK  Kosovo'))
        cntry_mapping = {
                        'AL  Albania': 'AL', 'AT  Austria': 'AT', 'BE  Belgium': 'BE', 'BG  Bulgaria': 'BG', 'CH  Switzerland': 'CH', 'CY  Cyprus': 'CY',
                        'CZ  Czechia': 'CZ', 'DE  Germany': 'DE', 'DK  Denmark': 'DK', 'EE  Estonia': 'EE', 'ES  Spain': 'ES', 'FI  Finland': 'FI', 'FR  France': 'FR', 'GB  United Kingdom': 'GB',
                        'GE  Georgia': 'GE', 'GR  Greece': 'GR', 'HR  Croatia': 'HR', 'HU  Hungary': 'HU', 'IE  Ireland': 'IE', 'IL  Israel': 'IL', 'IS  Iceland': 'IS',
                        'IT  Italy': 'IT', 'LT  Lithuania': 'LT', 'LU  Luxembourg': 'LU', 'LV  Latvia': 'LV', 'ME  Montenegro': 'ME', 'MK  North Macedonia': 'MK', 'NL  Netherlands': 'NL',
                        'NO  Norway': 'NO', 'PL  Poland': 'PL', 'PT  Portugal': 'PT', 'RO  Romania': 'RO', 'RS  Serbia': 'RS', 'RU  Russian Federation': 'RU',
                        'SE  Sweden': 'SE', 'SI  Slovenia': 'SI', 'SK  Slovakia': 'SK', 'TR  Turkey': 'TK', 'UA  Ukraine': 'UA', 'XK  Kosovo': 'XK'
                        }
        st.session_state.cntry = cntry_mapping[cntry]

        gndr = st.radio('What is your gender:',
                    ['Male', 'Female', 'Prefer not to say'])
        gndr_mapping = {
            "Male": 1,
            "Female": 2,
            "Prefer not to say": 6 # UPDATED GNDR FROM JSON
        }
        st.session_state.gndr = gndr_mapping[gndr]

        submit = st.form_submit_button("Next")
        if submit:
            st.session_state.current_question += 1
            st.experimental_rerun()

# elif st.session_state.current_question == 1:
#     with st.form("question_form"):
#         gndr = st.radio('What is your gender:',
#                     ['Male', 'Female', 'Prefer not to say'])
#         gndr_mapping = {
#             "Male": 1,
#             "Female": 2,
#             "Prefer not to say": 6 # UPDATED GNDR FROM JSON
#         }
#         st.session_state.gndr = gndr_mapping[gndr]
#         submit = st.form_submit_button("Next")
#         if submit:
#             st.session_state.current_question += 1
#             st.experimental_rerun()

elif st.session_state.current_question == 2:
    with st.form("question_form"):
        st.session_state.sclmeet = st.slider('How often meet with friends, relatives, colleagues:', # include explanation labels
                        min_value=1, max_value=7, step=1)
        submit = st.form_submit_button("Next")
        if submit:
            st.session_state.current_question += 1
            st.experimental_rerun()

elif st.session_state.current_question == 3:
    with st.form("question_form"):
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
        st.session_state.inprdsc = inprdsc_mapping[inprdsc]
        submit = st.form_submit_button("Next")
        if submit:
            st.session_state.current_question += 1
            st.experimental_rerun()

elif st.session_state.current_question == 4:
    with st.form("question_form"):
        sclact = st.selectbox('Take part in social activites compared to others of same age:',
                            ('Much less than most', 'Less than most', 'About the same', 'More than most', 'Much more than most'))
        sclact_mapping = {
            'Much less than most': 1,
            'Less than most': 2,
            'About the same': 3,
            'More than most': 4,
            'Much more than most': 5
        }
        st.session_state.sclact = sclact_mapping[sclact]
        submit = st.form_submit_button("Next")
        if submit:
            st.session_state.current_question += 1
            st.experimental_rerun()

elif st.session_state.current_question == 5:
    with st.form("question_form"):
        st.session_state.health = st.number_input('Subjective general health:')
        submit = st.form_submit_button("Next")
        if submit:
            st.session_state.current_question += 1
            st.experimental_rerun()

elif st.session_state.current_question == 6:
    with st.form("question_form"):
        st.session_state.rlgdgr = st.number_input('How religious are you:')
        submit = st.form_submit_button("Next")
        if submit:
            st.session_state.current_question += 1
            st.experimental_rerun()

elif st.session_state.current_question == 7:
    with st.form("question_form"):
        st.session_state.dscrgrp = st.number_input('Member of a group discriminated against in this country:')
        submit = st.form_submit_button("Next")
        if submit:
            st.session_state.current_question += 1
            st.experimental_rerun()

elif st.session_state.current_question == 8:
    with st.form("question_form"):
        st.session_state.ctzcntr = st.number_input('Citizen of country:')
        submit = st.form_submit_button("Next")
        if submit:
            st.session_state.current_question += 1
            st.experimental_rerun()

elif st.session_state.current_question == 9:
    with st.form("question_form"):
        st.session_state.brncntr = st.number_input('Born in country:')
        submit = st.form_submit_button("Next")
        if submit:
            st.session_state.current_question += 1
            st.experimental_rerun()

elif st.session_state.current_question == 10:
    with st.form("question_form"):
        st.session_state.happy = st.number_input('How happy are you:')
        submit = st.form_submit_button("Next")
        if submit:
            st.session_state.current_question += 1
            st.experimental_rerun()

# display final result
elif st.session_state.current_question == 11:
    with st.form("prediction_form"):
        submit = st.form_submit_button("Submit")
        if submit:
            st.write("Thank you for completing the questionnaire!")
            st.session_state.current_question = 0 # Reset for next time

            params = dict(
                stfmjob=st.session_state.stfmjob,
                trdawrk=st.session_state.trdawrk,
                jbprtfp=st.session_state.jbprtfp,
                pfmfdjba=st.session_state.pfmfdjba,
                dcsfwrka=st.session_state.dcsfwrka,
                wrkhome=st.session_state.wrkhome,
                wrklong=st.session_state.wrklong,
                wrkresp=st.session_state.wrkresp,
                health=st.session_state.health,
                stfeco=st.session_state.stfeco,
                hhmmb=st.session_state.hhmmb,
                hincfel=st.session_state.hincfel,
                trstplc=st.session_state.trstplc,
                sclmeet=st.session_state.sclmeet,
                hlthhmp=st.session_state.hlthhmp,
                iphlppl=st.session_state.iphlppl,
                ipsuces=st.session_state.ipsuces,
                ipstrgv=st.session_state.ipstrgv,
                gndr=st.session_state.gndr,
                cntry=st.session_state.cntry,
                happy=st.session_state.happy # <- SHOULD THIS STILL BE HERE??
            )

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





# TODO PROCESS AND MAP FEATURES

# params = dict(
#     stfmjob=st.session_state.stfmjob,
#     trdawrk=st.session_state.trdawrk,
#     jbprtfp=st.session_state.jbprtfp,
#     pfmfdjba=st.session_state.pfmfdjba,
#     dcsfwrka=st.session_state.dcsfwrka,
#     wrkhome=st.session_state.wrkhome,
#     wrklong=st.session_state.wrklong,
#     wrkresp=st.session_state.wrkresp,
#     health=st.session_state.health,
#     stfeco=st.session_state.stfeco,
#     hhmmb=st.session_state.hhmmb,
#     hincfel=st.session_state.hincfel,
#     trstplc=st.session_state.trstplc,
#     sclmeet=st.session_state.sclmeet,
#     hlthhmp=st.session_state.hlthhmp,
#     iphlppl=st.session_state.iphlppl,
#     ipsuces=st.session_state.ipsuces,
#     ipstrgv=st.session_state.ipstrgv,
#     gndr=st.session_state.gndr,
#     cntry=st.session_state.cntry,
#     happy=st.session_state.happy # SHOULD THIS STILL BE HERE??
# )

# FEATURES_DICT = {
#     "gndr"   :  "Gender",
#     "cntry"  :  "Country",

#     "stfmjob":  "How satisfied are you in your main job",
#     "dcsfwrka": "Current job: can decide time start/finish work",
#     "wrkhome":  "Work from home or place of choice, how often",
#     "wrklong":  "Employees expected to work overtime, how often",
#     "wrkresp":  "Employees expected to be responsive outside working hours, how often",

#     "sclmeet":  "How often socially meet with friends, relatives or colleagues",
#     "sclact":   "Take part in social activities compared to others of same age",

#     "trdawrk":  "Too tired after work to enjoy things like doing at home, how often",
#     "jbprtfp":  "Job prevents you from giving time to partner/family, how often",
#     "pfmfdjba": "Partner/family fed up with pressure of your job, how often",

#     "health":   "Subjective general health",
#     "hlthhmp":  "Hampered in daily activities by illness/disability/infirmity/mental problem",

#     "stfeco":   "How satisfied with present state of economy in country",
#     "hhmmb":    "Number of people living regularly as member of household",
#     "hincfel":  "Feeling about household's income nowadays",

#     "iphlppl":  "Important to help people and care for others well-being",
#     "ipsuces":  "Important to be successful and that people recognise achievements",
#     "ipstrgv":  "Important that government is strong and ensures safety",
#     "trstplc":  "Trust in the police",

# #    "happy":    "Happiness"
# }
