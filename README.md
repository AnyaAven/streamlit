# See your Wakatime stats
1. **Clone the Repository:**

    ```sh
    git clone https://github.com/AnyaAven/streamlit
    cd wakatime-insights-streamlit
    ```
2. **Install Dependencies:**

    ```sh
    pip install -r requirements.txt
    ```


3. **Set Up Environment Variables:**
Create a `secrets.toml` file in the `.streamlit` directory and add your WakaTime API key:

    ```.streamlit/secrets.toml
    WAKATIME_API_KEY = "your_wakatime_api_key"
    ```

## Running the App

To run the Streamlit app, use the following command:

```sh
streamlit run wakatime.py
```
