import requests
import streamlit as st

# Get the API key from the environment variable
api_key = st.secrets["wakatime_api_key"]

# Define the endpoint you want to access
endpoint = 'https://wakatime.com/api/v1/users/current/summaries'

# Define the parameters for the request
start_date = '2024-07-01'
end_date = '2024-07-07'
params = {
    'start': start_date,
    'end': end_date
}

# Make the GET request with the API key for authentication
response = requests.get(
    endpoint,
    params=params,
    headers={'Authorization': f'Basic {api_key}'})

# Check the response status
if response.status_code == 200:
    data = response.json()
    st.title('WakaTime Data Summary')
    st.write(f"Data from {start_date} to {end_date}")

    # Display the data in Streamlit
    for summary in data['data']:
        st.subheader(summary['range']['text'])
        st.write(f"Total time: {summary['grand_total']['text']}")
        for project in summary['projects']:
            st.write(f"Project: {project['name']}, Time: {project['text']}")
else:
    st.error(f'Failed to retrieve data: {
             response.status_code} - {response.text}')
