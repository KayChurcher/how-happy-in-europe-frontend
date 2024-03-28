import os
import streamlit as st
import requests
import pandas as pd
#### ARTHUR's MODIFICATIONS####
import time
#### END ARTHUR's MODIFICATIONS####

# Define the base URI of the API

if 'API_URI' in os.environ:
    BASE_URI = st.secrets[os.environ.get('API_URI')]
else:
    BASE_URI = st.secrets['cloud_api_uri']
# Add a '/' at the end if it's not there
BASE_URI = BASE_URI if BASE_URI.endswith('/') else BASE_URI + '/'
# Define the url to be used by requests.get to get a prediction (adapt if needed)
url = BASE_URI + 'predict'



# ADD TITLES AND INTRODUCTION
st.title('How Happy Are You?')
st.header('Answer the questions below to find out!')
st.subheader(" ")


# Initialize session state
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0



# Start Page
if st.session_state.current_question == 0:
    with st.form("question_form"):

        submit = st.form_submit_button("Start Questionnaire")
        if submit:
            st.session_state.current_question += 1
            st.experimental_rerun()


# Gender and Country Questions - 2 on 1 page
if st.session_state.current_question == 1:
    with st.form("question_form"):
        st.subheader(" ")

        # 1 Country
        st.markdown("##### What country do you live in?")
        cntry = st.selectbox('What country do you live in?',
                            ('BE  Belgium', 'BG  Bulgaria',
                            'CH  Switzerland', 'CZ	Czechia',
                            'EE  Estonia', 'FI  Finland',
                            'FR  France', 'GB  United Kingdom',
                            'GR  Greece', 'HR  Croatia',
                            'HU  Hungary', 'IE  Ireland',
                            'IS  Iceland', 'IT  Italy',
                            'LT  Lithuania', 'ME  Montenegro',
                            'MK  North Macedonia', 'NL  Netherlands',
                            'NO  Norway', 'PT  Portugal',
                            'SI  Slovenia', 'SK  Slovakia'),
                            label_visibility="collapsed")
        cntry_mapping = {
                        'BE  Belgium': 'BE', 'BG  Bulgaria': 'BG',
                        'CH  Switzerland': 'CH', 'CZ  Czechia': 'CZ',
                        'EE  Estonia': 'EE', 'FI  Finland': 'FI',
                        'FR  France': 'FR', 'GB  United Kingdom': 'GB',
                        'GR  Greece': 'GR', 'HR  Croatia': 'HR',
                        'HU  Hungary': 'HU', 'IE  Ireland': 'IE',
                        'IS  Iceland': 'IS', 'IT  Italy': 'IT',
                        'LT  Lithuania': 'LT', 'ME  Montenegro': 'ME',
                        'MK  North Macedonia': 'MK', 'NL  Netherlands': 'NL',
                        'NO  Norway': 'NO', 'PT  Portugal': 'PT',
                        'SI  Slovenia': 'SI', 'SK  Slovakia': 'SK'
                        }
        st.session_state.cntry = cntry_mapping[cntry]

        st.divider()

        # 2 Gender
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
elif st.session_state.current_question == 2:
    with st.form("question_form"):
        st.subheader(" ")

        if "disabled" not in st.session_state:
            st.session_state.disabled = False

        # 1 job satisfaction
        st.markdown("##### How satisfied are you in your main job?")
        st.markdown(" ")

        pnts_on = st.toggle('Prefer not to say', key="disabled")

        st.markdown(" ")

        stfmjob = st.select_slider(
                    'How satisfied are you in your main job?',
                    options=['Extremely dissatisfied', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Extremely satisfied'],
                    disabled=st.session_state.disabled,
                    label_visibility="collapsed")
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
            st.session_state.stfmjob = 66
        else:
            st.session_state.stfmjob = stfmjob_mapping[stfmjob]

        st.divider()

        # 2 job start/finish
        st.markdown(" ")
        st.markdown("##### In your current job can you decide the start and/or finish time of your work?")
        dcsfwrka = st.selectbox(
                    'In your current job can you decide the start and/or finish time of your work?',
                    options=["Not at all", "To some extent", "Completely", "Prefer not to say"],
                    label_visibility="collapsed")
        dcsfwrka_mapping = {
            "Not at all": 1,
            "To some extent": 2,
            "Completely": 3,
            "Prefer not to say": 6
        }
        st.session_state.dcsfwrka = dcsfwrka_mapping[dcsfwrka]

        st.divider()

        # 3 work from home
        st.markdown(" ")
        st.markdown("##### How often do you work from home or from a place of your choice?")
        wrkhome = st.selectbox(
                    'How often do you work from home or from a place of your choice?',
                    options=["Never", "Less often", "Once a month", "Several times a month", "Several times a week", "Every day", "Prefer not to say"],
                    label_visibility="collapsed")
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

        st.divider()

        # 4 work after hours
        st.markdown(" ")
        st.markdown("##### How often are employees expected to work overtime?")
        wrklong = st.selectbox(
                    'How often are employees expected to work overtime?',
                    options=["Never", "Less often", "Once a month", "Several times a month", "Several times a week", "Every day", "I don't work in an organisation", "Prefer not to say"],
                    label_visibility="collapsed")
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

        st.divider()

        # 5 contact after work hours
        st.markdown(" ")
        st.markdown("##### How often are employees expected to be responsive outside working hours?")
        wrkresp = st.selectbox(
                    'How often are employees expected to be responsive outside working hours?',
                    options=["Never", "Less often", "Once a month", "Several times a month", "Several times a week", "Every day", "Prefer not to say"],
                    label_visibility="collapsed")
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

        st.divider()

        submit = st.form_submit_button("Next")
        back = st.form_submit_button("Previous")
        if back:
            st.session_state.current_question -= 1
            st.experimental_rerun()
        if submit:
            st.session_state.current_question += 1
            st.experimental_rerun()


# Social Questions - 2 on 1 page
elif st.session_state.current_question == 3:
    with st.form("question_form"):
        st.subheader(" ")

        # 1 Socially meet
        st.markdown("##### How often do you meet with friends, relatives or colleagues?")
        st.markdown(" ")
        sclmeet = st.select_slider(
                        'How often do you meet with friends, relatives or colleagues?',
                        options=["Never", "Less often", "Once a month", "Several times a month", "Several times a week", "Every day"],
                        label_visibility="collapsed")
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

        st.divider()

        # 2 Social Activities
        st.markdown(" ")
        st.markdown("##### How often do you take part in social activities compared to others your age?")
        st.markdown(" ")
        sclact = st.select_slider(
                        'How often do you take part in social activities compared to others your age?',
                        options=["Much less than most", "Less than most", "About the same", "More than most", "Much more than most"],
                        label_visibility="collapsed")
        sclact_mapping = {
            "Much less than most": 1,
            "Less than most": 2,
            "About the same": 3,
            "More than most": 4,
            "Much more than most": 5
        }
        st.session_state.sclact = sclact_mapping[sclact]

        st.divider()

        submit = st.form_submit_button("Next")
        back = st.form_submit_button("Previous")
        if back:
            st.session_state.current_question -= 1
            st.experimental_rerun()
        if submit:
            st.session_state.current_question += 1
            st.experimental_rerun()


# Job Affecting Social Life Questions - 3 on 1 page
elif st.session_state.current_question == 4:
    with st.form("question_form"):
        st.subheader(" ")

        # 1 Job affecting home
        st.markdown("##### How often are you too tired after work to enjoy doing things at home?")
        trdawrk = st.selectbox('How often are you too tired after work to enjoy doing things at home?',
                            ("Never", "Hardly ever", "Sometimes", "Often", "Always", "Prefer not to say"),
                            label_visibility="collapsed")
        trdawrk_mapping = {
            "Never": 1,
            "Hardly ever": 2,
            "Sometimes": 3,
            "Often": 4,
            "Always": 5,
            "Prefer not to say": 6
        }
        st.session_state.trdawrk = trdawrk_mapping[trdawrk]

        st.divider()

        # 2 Job affecting family
        st.markdown("##### How often does your job prevent you from giving time to your partner/family?")
        jbprtfp = st.selectbox('How often does your job prevent you from giving time to your partner/family?',
                                ("Never", "Hardly ever", "Sometimes", "Often", "Always", "I don't have a partner/family", "Prefer not to say"),
                                label_visibility="collapsed")
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

        st.divider()

        # 3 Family dislike your job
        st.markdown("##### How often is your partner/family fed up with the pressure of your job?")
        pfmfdjba = st.selectbox('How often is your partner/family fed up with the pressure of your job?',
                            ("Never", "Hardly ever", "Sometimes", "Often", "Always", "Prefer not to say"),
                            label_visibility="collapsed")
        pfmfdjba_mapping = {
            "Never": 1,
            "Hardly ever": 2,
            "Sometimes": 3,
            "Often": 4,
            "Always": 5,
            "Prefer not to say": 6
        }
        st.session_state.pfmfdjba = pfmfdjba_mapping[pfmfdjba]

        st.divider()


        submit = st.form_submit_button("Next")
        back = st.form_submit_button("Previous")
        if back:
            st.session_state.current_question -= 1
            st.experimental_rerun()
        if submit:
            st.session_state.current_question += 1
            st.experimental_rerun()


# Health Questions - 2 on 1 page
elif st.session_state.current_question == 5:
    with st.form("question_form"):
        st.subheader(" ")

        # 1 General Health
        st.markdown("##### How would you describe your subjective general health?")
        st.markdown(" ")
        health = st.radio('How would you describe your subjective general health?', # MAYBE SELECT_SLIDER
                           ["Very bad", "Bad", "Fair", "Good", "Very good"],
                           horizontal=True,
                           label_visibility="collapsed")
        health_mapping = {
            "Very good": 1,
            "Good": 2,
            "Fair": 3,
            "Bad": 4,
            "Very bad": 5
        }
        st.session_state.health = health_mapping[health]

        st.divider()

        # 2 health affecting life
        st.markdown("##### Are you hampered in daily activities by illness/disability/infirmity/mental problem?")
        st.markdown(" ")
        hlthhmp = st.radio('Are you hampered in daily activities by illness/disability/infirmity/mental problem?',
                            ["No", "Yes to some extent", "Yes a lot"],
                            horizontal=True,
                            label_visibility="collapsed")
        hlthhmp_mapping = {
            "Yes a lot": 1,
            "Yes to some extent": 2,
            "No": 3
        }
        st.session_state.hlthhmp = hlthhmp_mapping[hlthhmp]

        st.divider()


        submit = st.form_submit_button("Next")
        back = st.form_submit_button("Previous")
        if back:
            st.session_state.current_question -= 1
            st.experimental_rerun()
        if submit:
            st.session_state.current_question += 1
            st.experimental_rerun()


# Household and Income Questions - 3 on 1 page
elif st.session_state.current_question == 6:
    with st.form("question_form"):
        st.subheader(" ")

        # 1 Number of people in household
        st.markdown("##### How many people do you have in your household?")
        st.session_state.hhmmb = st.number_input('How many people do you have in your household?',
                                                 min_value=1, max_value=None, value='min', step=1,
                                                 label_visibility="collapsed")

        st.divider()

        # 2 Household income
        st.markdown("##### How do you feel about your household's current income?")
        st.markdown(" ")
        hincfel = st.select_slider("How do you feel about your household's current income?",
                           ["Very difficult on present income", "Difficult on present income", "Coping on present income", "Living comfortably on present income"],
                           label_visibility="collapsed")
        hincfel_mapping = {
            "Living comfortably on present income": 1,
            "Coping on present income": 2,
            "Difficult on present income": 3,
            "Very difficult on present income": 4
        }
        st.session_state.hincfel = hincfel_mapping[hincfel]

        st.divider()

        # 3 Country economy
        st.markdown("##### How satisfied are you with the present state of your country's economy?")
        st.markdown(" ")
        stfeco = st.select_slider(
                    "How satisfied are you with the present state of your country's economy?",
                    options=['Extremely dissatisfied', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Extremely satisfied'],
                    label_visibility="collapsed")
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

        st.divider()

        submit = st.form_submit_button("Next")
        back = st.form_submit_button("Previous")
        if back:
            st.session_state.current_question -= 1
            st.experimental_rerun()
        if submit:
            st.session_state.current_question += 1
            st.experimental_rerun()


# Societal Values Questions - 4 on 1 page
elif st.session_state.current_question == 7:
    with st.form("question_form"):
        st.subheader(" ")

        # 1 Success
        st.markdown("##### How much do you identify with this statement:")
        st.markdown("##### 'It is important to be successful and for people to recognise my acheivements.' ")
        st.markdown(" ")
        ipsuces = st.select_slider(
                                "How much do you identify with the statement; it is important to be successful and that people recognise my acheivements?",
                                options=["Not like me at all", "Not like me", "A little like me", "Somewhat like me", "Like me", "Very much like me"],
                                label_visibility="collapsed")
        ipsuces_mapping = {
            "Very much like me": 1,
            "Like me": 2,
            "Somewhat like me": 3,
            "A little like me": 4,
            "Not like me": 5,
            "Not like me at all": 6
        }
        st.session_state.ipsuces = ipsuces_mapping[ipsuces]

        st.divider()

        # 2 Help others
        st.markdown("##### How much do you identify with this statement:")
        st.markdown("##### 'It is important to help others and care for their wellbeing.' ")
        st.markdown(" ")
        iphlppl = st.select_slider(
                                "How much do you identify with the statement; it is important to help others and care for their welbeing?",
                                options=["Not like me at all", "Not like me", "A little like me", "Somewhat like me", "Like me", "Very much like me"],
                                label_visibility="collapsed")
        iphlppl_mapping = {
            "Very much like me": 1,
            "Like me": 2,
            "Somewhat like me": 3,
            "A little like me": 4,
            "Not like me": 5,
            "Not like me at all": 6
        }
        st.session_state.iphlppl = iphlppl_mapping[iphlppl]

        st.divider()

        # 3 Government help
        st.markdown("##### How much do you identify with this statement:")
        st.markdown("##### 'It is important that the government is strong and ensures safety.' ")
        st.markdown(" ")
        ipstrgv = st.select_slider(
                                "It is important that the government is strong and ensures safety.",
                                options=["Not like me at all", "Not like me", "A little like me", "Somewhat like me", "Like me", "Very much like me"],
                                label_visibility="collapsed")
        ipstrgv_mapping = {
            "Very much like me": 1,
            "Like me": 2,
            "Somewhat like me": 3,
            "A little like me": 4,
            "Not like me": 5,
            "Not like me at all": 6
        }
        st.session_state.ipstrgv = ipstrgv_mapping[ipstrgv]

        st.divider()

        # 4 Police trust
        st.markdown("##### How much trust do you have in the Police?")
        st.markdown(" ")
        trstplc = st.select_slider(
                                "It is important that the government is strong and ensures safety.",
                                options=["No trust at all", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Complete trust"],
                                label_visibility="collapsed")
        trstplc_mapping = {
            "No trust at all": 0,
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "Complete trust": 10
        }
        st.session_state.trstplc = trstplc_mapping[trstplc]

        st.divider()

        submit = st.form_submit_button("Next")
        back = st.form_submit_button("Previous")
        if back:
            st.session_state.current_question -= 1
            st.experimental_rerun()
        if submit:
            st.session_state.current_question += 1
            st.experimental_rerun()



# display final result
elif st.session_state.current_question == 8:
    with st.form("prediction_form"):
        submit = st.form_submit_button("Submit your Answers")
        if submit:
            st.write("Thank you for completing the questionnaire!")
            st.session_state.current_question = 0 # Reset for next time

            params = dict(
                cntry=st.session_state.cntry,
                gndr=st.session_state.gndr,
                stfmjob=st.session_state.stfmjob,
                dcsfwrka=st.session_state.dcsfwrka,
                wrkhome=st.session_state.wrkhome,
                wrklong=st.session_state.wrklong,
                wrkresp=st.session_state.wrkresp,
                sclmeet=st.session_state.sclmeet,
                sclact=st.session_state.sclact,
                trdawrk=st.session_state.trdawrk,
                jbprtfp=st.session_state.jbprtfp,
                pfmfdjba=st.session_state.pfmfdjba,
                health=st.session_state.health,
                hlthhmp=st.session_state.hlthhmp,
                hhmmb=st.session_state.hhmmb,
                hincfel=st.session_state.hincfel,
                stfeco=st.session_state.stfeco,
                ipsuces=st.session_state.ipsuces,
                iphlppl=st.session_state.iphlppl,
                ipstrgv=st.session_state.ipstrgv,
                trstplc=st.session_state.trstplc,
            )


            response = requests.get(url, params=params)

            prediction = response.json()

            #### ARTHUR's MODIFICATIONS####

            progress_text = "Prediction in progress. Please wait."
            my_bar = st.progress(0, text=progress_text)

            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=progress_text)
            time.sleep(1)
            my_bar.empty()

            #### END ARTHUR's MODIFICATIONS####

            pred = prediction#['happy'] # STATE OF HAPPINESS

            # st.text(pred)

            # Use markdown with HTML tags to increase the size
            st.markdown(f'<h2 style="font-size:2em;color:black;">{pred}</h2>', unsafe_allow_html=True)
