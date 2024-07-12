import requests
import streamlit as st

import plotly.express as px
import pandas as pd


api_key = st.secrets["wakatime_api_key"]


WAKA_TIME_URL = 'https://wakatime.com/api/v1/'
SUMMARY_ENDPOINT = 'users/current/summaries'
INSIGHTS_ENDPOINT = 'users/current/insights/weekdays/last_year'
LANGUAGES_ENDPOINT = 'users/current/insights/languages/all_time'
ALL_TIME_ENDPOINT = 'users/current/all_time_since_today'


start_date = '2024-07-01'
end_date = '2024-07-07'
params = {
    'start': start_date,
    'end': end_date
}


insights_resp = requests.get(
    WAKA_TIME_URL + INSIGHTS_ENDPOINT,
    headers={'Authorization': f'Basic {api_key}'})

languages_resp = requests.get(
    WAKA_TIME_URL + LANGUAGES_ENDPOINT, headers={'Authorization': f'Basic {api_key}'})

summary_resp = requests.get(
    WAKA_TIME_URL + SUMMARY_ENDPOINT,
    params=params,
    headers={'Authorization': f'Basic {api_key}'})

all_time_resp = requests.get(
    WAKA_TIME_URL + ALL_TIME_ENDPOINT, headers={'Authorization': f'Basic {api_key}'})


if all_time_resp.status_code == 200:
    all_time_data = all_time_resp.json()['data']

    total_seconds = all_time_data['total_seconds']
    total_hours = total_seconds / 3600

    range_start_date = all_time_data['range']['start_date']
    range_end_date = all_time_data['range']['end_date']


    text_total_time = all_time_data['text']

    st.title('WakaTime All-Time Insights')

    st.subheader(f'Total Time Spent since {range_start_date} 🕒')
    st.write(f"Total time: **{text_total_time}** ({total_hours:.2f} hours)")


else:
    st.error(f'Failed to retrieve data: {
             all_time_resp.status_code} - {all_time_resp.text}')

if insights_resp.status_code == 200 and languages_resp.status_code == 200:
    insights_data = insights_resp.json()['data']['weekdays']
    languages_data = languages_resp.json()['data']['languages']


    weekdays, categories, averages, totals = [], [], [], []

    for day in insights_data:
        day_name = day['name']
        for category in day['categories']:
            if(category['name'] == 'Coding' or category['name'] == 'Browsing'):
                weekdays.append(day_name)
                categories.append(category['name'])
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

    languages, total_hours = [], []

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


# if summary_resp.status_code == 200:
#     summary_data = summary_resp.json()['data']
#     st.title('WakaTime Data Summary')
#     st.write(f"Data from {start_date} to {end_date}")

#     # Process projects data to find top 5 projects
#     all_projects = []

#     for day_data in summary_data:
#         for project in day_data['projects']:
#             all_projects.append(
#                 {'name': project['name'], 'total_seconds': project['total_seconds']})

#     df_projects = pd.DataFrame(all_projects)
#     df_projects = df_projects.groupby('name', as_index=False).sum()
#     df_projects = df_projects.sort_values(
#         by='total_seconds', ascending=False).head(5)
#     df_projects['total_hours'] = df_projects['total_seconds'] / \
#         3600  # convert seconds to hours

#     st.header('Top 5 Projects by Time Spent')
#     fig = px.bar(df_projects, x='name', y='total_hours',
#                  title='Top 5 Projects by Time Spent')
#     st.plotly_chart(fig)

#     all_files = []

