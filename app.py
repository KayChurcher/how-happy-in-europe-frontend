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

# """
# Below is preparation for final model.
# """

# ADD TITLES AND INTRODUCTION
st.title('How Happy Are You?')
st.header('Answer the questions below to find out!')
st.subheader(" ")


# Initialize session state
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0


# Gender and Country Questions - 2 on 1 page
if st.session_state.current_question == 0:
    with st.form("question_form"):
        st.subheader(" ")

        st.markdown("##### What country do you live in?")
        cntry = st.selectbox('What country do you live in?',
                            ('AL  Albania', 'AT  Austria', 'BE  Belgium', 'BG  Bulgaria', 'CH  Switzerland', 'CY  Cyprus',
                            'CZ  Czechia', 'DE  Germany', 'DK  Denmark', 'EE  Estonia', 'ES  Spain', 'FI  Finland', 'FR  France', 'GB  United Kingdom',
                            'GE  Georgia', 'GR  Greece', 'HR  Croatia', 'HU  Hungary', 'IE  Ireland', 'IL  Israel', 'IS  Iceland',
                            'IT  Italy', 'LT  Lithuania', 'LU  Luxembourg', 'LV  Latvia', 'ME  Montenegro', 'MK  North Macedonia', 'NL  Netherlands',
                            'NO  Norway', 'PL  Poland', 'PT  Portugal', 'RO  Romania', 'RS  Serbia', 'RU  Russian Federation',
                            'SE  Sweden', 'SI  Slovenia', 'SK  Slovakia', 'TR  Turkey', 'UA  Ukraine', 'XK  Kosovo'),
                            label_visibility="collapsed")
        cntry_mapping = {
                        'AL  Albania': 'AL', 'AT  Austria': 'AT', 'BE  Belgium': 'BE', 'BG  Bulgaria': 'BG', 'CH  Switzerland': 'CH', 'CY  Cyprus': 'CY',
                        'CZ  Czechia': 'CZ', 'DE  Germany': 'DE', 'DK  Denmark': 'DK', 'EE  Estonia': 'EE', 'ES  Spain': 'ES', 'FI  Finland': 'FI', 'FR  France': 'FR', 'GB  United Kingdom': 'GB',
                        'GE  Georgia': 'GE', 'GR  Greece': 'GR', 'HR  Croatia': 'HR', 'HU  Hungary': 'HU', 'IE  Ireland': 'IE', 'IL  Israel': 'IL', 'IS  Iceland': 'IS',
                        'IT  Italy': 'IT', 'LT  Lithuania': 'LT', 'LU  Luxembourg': 'LU', 'LV  Latvia': 'LV', 'ME  Montenegro': 'ME', 'MK  North Macedonia': 'MK', 'NL  Netherlands': 'NL',
                        'NO  Norway': 'NO', 'PL  Poland': 'PL', 'PT  Portugal': 'PT', 'RO  Romania': 'RO', 'RS  Serbia': 'RS', 'RU  Russian Federation': 'RU',
                        'SE  Sweden': 'SE', 'SI  Slovenia': 'SI', 'SK  Slovakia': 'SK', 'TR  Turkey': 'TK', 'UA  Ukraine': 'UA', 'XK  Kosovo': 'XK'
                        }
        st.session_state.cntry = cntry_mapping[cntry]

        st.divider()

        st.markdown("##### What is your gender?")
        gndr = st.radio('What is your gender?',
                        ['Male', 'Female'],
                        label_visibility="collapsed")
        gndr_mapping = {
            "Male": 1,
            "Female": 2,
            }
        st.session_state.gndr = gndr_mapping[gndr]

        st.divider()

        submit = st.form_submit_button("Next")
        if submit:
            st.session_state.current_question += 1
            st.experimental_rerun()



# Job Questions - 5 on 1 page
elif st.session_state.current_question == 1:
    with st.form("question_form"):

        if "disabled" not in st.session_state:
            st.session_state.disabled = False

        # def switchToggle():
        #     if st.session_state.disabled == False:
        #         st.session_state.disabled = True
        #     else:
        #         st.session_state.disabled = False

        # 1 job satisfaction
        pnts_on = st.toggle('Prefer not to say', key="disabled")

        stfmjob = st.select_slider(
                    'How satisfied are you in your main job?',
                    options=['Extremely dissatisfied', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Extremely satisfied'],
                    disabled=st.session_state.disabled)
        stfmjob_mapping = {
            "Extremely dissatisfied": 0,
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "Extremely satisfied": 10,
            "Prefer not to say": 66    # add toggle with prefer not to say option?
            }


        if pnts_on:
            st.session_state.stfmjob = stfmjob_mapping[pnts_on]
            #stfmjob.session_state.disabled
            #stfmjob = st.select_slider(disabled=st.session_state.disabled) # visibility of stfmjob = off
        else:
            st.session_state.stfmjob = stfmjob_mapping[stfmjob]




        # 2 job start/finish
        dcsfwrka = st.selectbox(
                    'In your current job can you decide the start and/or finish time of your work?',
                    options=["Not at all", "To some extent", "Completely", "Prefer not to say"])
        dcsfwrka_mapping = {
            "Not at all": 1,
            "To some extent": 2,
            "Completely": 3,
            "Prefer not to say": 6
        }
        st.session_state.dcsfwrka = dcsfwrka_mapping[dcsfwrka]

        # 3 work from home
        wrkhome = st.selectbox(
                    'How often do you work from home or from a place of your choice?',
                    options=["Every day", "Several times a week", "Several times a month", "Once a month", "Less often", "Never", "Prefer not to say"])
        wrkhome_mapping = {
            "Every day": 1,
            "Several times a week": 2,
            "Several times a month": 3,
            "Once a month": 4,
            "Less often": 5,
            "Never": 6,
            "Prefer not to say": 66
        }
        st.session_state.wrkhome = wrkhome_mapping[wrkhome]

        # 4 work after hours
        wrklong = st.selectbox(
                    'How often are employees expected to work overtime?',
                    options=["Every day", "Several times a week", "Several times a month", "Once a month", "Less often", "Never", "I don't work in an organisation", "Prefer not to say"])
        wrklong_mapping = {
            "Every day": 1,
            "Several times a week": 2,
            "Several times a month": 3,
            "Once a month": 4,
            "Less often": 5,
            "Never": 6,
            "I don't work in an organisation": 55,
            "Prefer not to say": 66
        }
        st.session_state.wrklong = wrklong_mapping[wrklong]

        # 5 contact after work hours
        wrkresp = st.selectbox(
                    'How often are employees expected to work overtime?',
                    options=["Every day", "Several times a week", "Several times a month", "Once a month", "Less often", "Never", "Prefer not to say"])
        wrkresp_mapping = {
            "Every day": 1,
            "Several times a week": 2,
            "Several times a month": 3,
            "Once a month": 4,
            "Less often": 5,
            "Never": 6,
            "Prefer not to say": 66
        }
        st.session_state.wrkresp = wrkresp_mapping[wrkresp]

        submit = st.form_submit_button("Next")
        back = st.form_submit_button("Previous")
        if back:
            st.session_state.current_question -= 1
            st.experimental_rerun()
        if submit:
            st.session_state.current_question += 1
            st.experimental_rerun()



# Social Questions - 2 on 1 page
elif st.session_state.current_question == 2:
    with st.form("question_form"):

        # 1 Socially meet
        sclmeet = st.selectbox(
                        'How often do you meet with friends, relatives or colleagues?',
                        options=["Every day", "Several times a week", "Several times a month", "Once a month", "Less often", "Never", "Prefer not to say"])
        sclmeet_mapping = {
            "Every day": 7,
            "Several times a week": 6,
            "Once a week": 5,
            "Several times a month": 4,
            "Once a month": 3,
            "Less often": 2,
            "Never": 1
        }
        st.session_state.sclmeet = sclmeet_mapping[sclmeet]

        # 2 Social Activities
        sclact = st.select_slider(
                        'How often do you take part in social activities compared to others your age?',
                        options=["Much less than most", "Less than most", "About the same", "More than most", "Much more than most"])
        sclact_mapping = {
            "Much less than most": 1,
            "Less than most": 2,
            "About the same": 3,
            "More than most": 4,
            "Much more than most": 5
        }
        st.session_state.sclact = sclact_mapping[sclact]

        submit = st.form_submit_button("Next")
        back = st.form_submit_button("Previous")
        if back:
            st.session_state.current_question -= 1
            st.experimental_rerun()
        if submit:
            st.session_state.current_question += 1
            st.experimental_rerun()



# Job Affecting Social Life Questions - 3 on 1 page
elif st.session_state.current_question == 3:
    with st.form("question_form"):

        # 1 Job affecting home
        trdawrk = st.selectbox('How often are you too tired after work to enjoy doing things at home?',
                            ("Never", "Hardly ever", "Sometimes", "Often", "Always", "Prefer not to say",))
        trdawrk_mapping = {
            "Never": 1,
            "Hardly ever": 2,
            "Sometimes": 3,
            "Often": 4,
            "Always": 5,
            "Prefer not to say": 6
        }
        st.session_state.trdawrk = trdawrk_mapping[trdawrk]

        # 2 Job affecting family
        jbprtfp = st.selectbox('How often does your job prevent you from giving time to your partner/family?',
                            ("Never", "Hardly ever", "Sometimes", "Often", "Always", "I don't have a partner/family", "Prefer not to say",))
        jbprtfp_mapping = {
            "Never": 1,
            "Hardly ever": 2,
            "Sometimes": 3,
            "Often": 4,
            "Always": 5,
            "I don't have a partner/family": 6,
            "Prefer not to say": 66
        }
        st.session_state.jbprtfp = jbprtfp_mapping[jbprtfp]

        # 3 Family dislike your job
        pfmfdjba = st.selectbox('How often is your partner/family fed up with the pressure of your job?',
                            ("Never", "Hardly ever", "Sometimes", "Often", "Always", "Prefer not to say",))
        pfmfdjba_mapping = {
            "Never": 1,
            "Hardly ever": 2,
            "Sometimes": 3,
            "Often": 4,
            "Always": 5,
            "Prefer not to say": 6
        }
        st.session_state.pfmfdjba = pfmfdjba_mapping[pfmfdjba]


        submit = st.form_submit_button("Next")
        back = st.form_submit_button("Previous")
        if back:
            st.session_state.current_question -= 1
            st.experimental_rerun()
        if submit:
            st.session_state.current_question += 1
            st.experimental_rerun()



# Health Questions - 2 on 1 page
elif st.session_state.current_question == 4:
    with st.form("question_form"):

        # 1 General Health
        health = st.radio('How would you describe your subjective general health?', # MAYBE SELECT_SLIDER
                           ["Very good", "Good", "Fair", "Bad", "Very bad"],
                           horizontal=True)
        health_mapping = {
            "Very good": 1,
            "Good": 2,
            "Fair": 3,
            "Bad": 4,
            "Very bad": 5
        }
        st.session_state.health = health_mapping[health]

        # 2 health affecting life
        hlthhmp = st.radio('Are you hampered in daily activities by illness/disability/infirmity/mental problem?',
                            ["Yes a lot", "Yes to some extent", "No"],
                            horizontal=True)
        hlthhmp_mapping = {
            "Yes a lot": 1,
            "Yes to some extent": 2,
            "No": 3
        }
        st.session_state.hlthhmp = hlthhmp_mapping[hlthhmp]


        submit = st.form_submit_button("Next")
        back = st.form_submit_button("Previous")
        if back:
            st.session_state.current_question -= 1
            st.experimental_rerun()
        if submit:
            st.session_state.current_question += 1
            st.experimental_rerun()



# Household and Income Questions - 3 on 1 page
elif st.session_state.current_question == 5:
    with st.form("question_form"):

        # 1 Number of people in household
        st.session_state.hhmmb = st.number_input('How many people do you have in your household?',
                                                 min_value=1, max_value=None, value='min', step=1)

        # 2 Household income
        hincfel = st.radio("How do you feel about your household's current income?", # MAYBE SELECT_SLIDER
                           ["Living comfortably on present income", "Coping on present income", "Difficult on present income", "Very difficult on present income"],
                           horizontal=True)
        hincfel_mapping = {
            "Living comfortably on present income": 1,
            "Coping on present income": 2,
            "Difficult on present income": 3,
            "Very difficult on present income": 4
        }
        st.session_state.hincfel = hincfel_mapping[hincfel]

        # 3 Country economy
        stfeco = st.select_slider(
                    "How satisfied are you with the present state of your country's economy?",
                    options=['Extremely dissatisfied', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Extremely satisfied'],
                    )
        stfeco_mapping = {
            "Extremely dissatisfied": 0,
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "Extremely satisfied": 10,
            }
        st.session_state.stfeco = stfeco_mapping[stfeco]

        submit = st.form_submit_button("Next")
        back = st.form_submit_button("Previous")
        if back:
            st.session_state.current_question -= 1
            st.experimental_rerun()
        if submit:
            st.session_state.current_question += 1
            st.experimental_rerun()


#     "ipsuces":  "Important to be successful and that people recognise achievements",
#     "iphlppl":  "Important to help people and care for others well-being",
#     "ipstrgv":  "Important that government is strong and ensures safety",
#     "trstplc":  "Trust in the police",

# Societal Values Questions - 4 on 1 page
elif st.session_state.current_question == 6:
    with st.form("question_form"):
        st.session_state.rlgdgr = st.number_input('How religious are you:')

        submit = st.form_submit_button("Next")
        back = st.form_submit_button("Previous")
        if back:
            st.session_state.current_question -= 1
            st.experimental_rerun()
        if submit:
            st.session_state.current_question += 1
            st.experimental_rerun()


# TODO MAKE START PAGE / WELCOME PAGE BEFORE QUESTIONNAIRE

# TODO change text size of questions - make subtitles?

# TODO SWAP ASC/DESC ORDER OF SOME QUESTIONS

# TODO MAKE TOGGLE WORK

# TODO place previous and next buttons better on page

# Final Page
# TODO INPLEMENT PROGRESS BAR - for loading response
#      FIRST TIME SLOW BC IT'S IMPLEMENTING THE CONTAINER
# TODO collapse / hide submit button after submitting

# change order of params dict


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
            )


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

# happy=st.session_state.happy # <- SHOULD THIS STILL BE HERE??
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

#     "hhmmb":    "Number of people living regularly as member of household",
#     "hincfel":  "Feeling about household's income nowadays",
#     "stfeco":   "How satisfied with present state of economy in country",

#     "ipsuces":  "Important to be successful and that people recognise achievements",
#     "iphlppl":  "Important to help people and care for others well-being",
#     "ipstrgv":  "Important that government is strong and ensures safety",
#     "trstplc":  "Trust in the police",

# #    "happy":    "Happiness"
# }


# FEATURES_DICT = {
#     "cntry",
#     "gndr",

#     "stfmjob",
#     "dcsfwrka",
#     "wrkhome",
#     "wrklong",
#     "wrkresp",

#     "sclmeet",
#     "sclact",

#     "trdawrk",
#     "jbprtfp",
#     "pfmfdjba",

#     "health",
#     "hlthhmp",

#     "hhmmb",
#     "hincfel",
#     "stfeco",

#     "ipsuces",
#     "iphlppl",
#     "ipstrgv",
#     "trstplc",

# }
