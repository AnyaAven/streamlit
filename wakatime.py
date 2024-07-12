import requests
import streamlit as st

import plotly.express as px
import pandas as pd


api_key = st.secrets["wakatime_api_key"]


WAKA_TIME_URL = 'https://wakatime.com/api/v1/'
SUMMARY_ENDPOINT = 'users/current/summaries'
INSIGHTS_ENDPOINT = 'users/current/insights/weekdays/last_year'
LANGUAGES_ENDPOINT = 'users/current/insights/languages/all_time'

start_date = '2024-07-01'
end_date = '2024-07-07'
params = {
    'start': start_date,
    'end': end_date
}


insights_resp = requests.get(
    WAKA_TIME_URL + INSIGHTS_ENDPOINT,
    headers={'Authorization': f'Basic {api_key}'})

languages_response = requests.get(
    WAKA_TIME_URL + LANGUAGES_ENDPOINT, headers={'Authorization': f'Basic {api_key}'})

if insights_resp.status_code == 200:
    data = insights_resp.json()['data']['weekdays']

    st.title('WakaTime All-Time Insights')

    weekdays = []
    categories = []
    averages = []
    totals = []

    for day in data:
        day_name = day['name']
        for category in day['categories']:
            weekdays.append(day_name)
            categories.append(category['name'])
            # convert seconds to hours
            averages.append(category['average'] / 3600)
            totals.append(category['total'] / 3600)  # convert seconds to hours

    df = pd.DataFrame({
        'Weekday': weekdays,
        'Category': categories,
        'Average Hours': averages,
        'Total Hours': totals
    })

    st.header('Average Hours by Category')
    fig = px.bar(df, x='Weekday', y='Average Hours', color='Category', barmode='group',
                 title='Average Hours by Category for Each Weekday')
    st.plotly_chart(fig)

    languages_data = languages_response.json()['data']['languages']
    languages = []
    total_hours = []

    for language in languages_data:

        languages.append(language['name'])
        total_hours.append(language['total_seconds'] / 3600)

    df_languages = pd.DataFrame({
        'Language': languages,
        'Total Hours': total_hours
    })

    # Display the languages data in Streamlit
    st.header('Total Time Spent on Each Language')
    fig = px.pie(df_languages, values='Total Hours',
                 names='Language', title='Total Time Spent on Each Language')
    st.plotly_chart(fig)

else:
    st.error(f'Failed to retrieve data: {
             insights_resp.status_code} - {insights_resp.text}')

summary_resp = requests.get(
    WAKA_TIME_URL + SUMMARY_ENDPOINT,
    params=params,
    headers={'Authorization': f'Basic {api_key}'})


if summary_resp.status_code == 200:
    data = summary_resp.json()
    st.title('WakaTime Data Summary')
    st.write(f"Data from {start_date} to {end_date}")

    for summary_resp in data['data']:
        st.subheader(summary_resp['range']['text'])
        st.write(f"Total time: {summary_resp['grand_total']['text']}")
        for project in summary_resp['projects']:
            st.write(f"Project: {project['name']}, Time: {project['text']}")
else:
    st.error(f'Failed to retrieve data: {
             summary_resp.status_code} - {summary_resp.text}')
