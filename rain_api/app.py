import streamlit as st
import requests
import math

API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(page_title="Rain Prediction App", layout="wide")

st.title("Rainfall Prediction System")
st.markdown("Enter today's weather data to predict if it will rain tomorrow.")

with st.form("prediction_form"):

    st.subheader("Temperature")

    '''
    ['WindGustSpeed', 'Pressure_mean', 'Pressure_diff',
       'WindSpeed_mean', 'WindSpeed_diff', 'Cloud_mean', 'Cloud_diff', 'Month',
       'WindDir9am_angle', 'WindDir3pm_angle', 'WindGustDir_angle',
       'ClimateZone'],
    '''

    col1, col2, col3 = st.columns(3)
    with col1:
        min_temp = st.number_input("Min Temp", value=15.0) # remain same
        max_temp = st.number_input("Max Temp", value=25.0) # remain same
        
        # Calculating temperature range & difference
        temp_range = max_temp - min_temp
        temp_diff = abs(max_temp - min_temp)

    with col2:
        humidity_9am = st.number_input("Humidity 9am", value=60.0)
        humidity_3pm = st.number_input("Humidity 3pm", value=50.0)

        # Calculating Humidity mean and difference
        humidity_mean = (humidity_9am + humidity_3pm) / 2
        humidity_diff = abs(humidity_9am - humidity_3pm)
        

    st.subheader("Rain & Evaporation")

    col1, col2 = st.columns(2)
    with col1:
        rainfall = st.number_input("Rainfall", value=0.0)
        evaporation = st.number_input("Evaporation", value=5.0)

    with col2:
        sunshine = st.number_input("Sunshine", value=8.0)
        # month = st.sidebar("Month", 1, 6, 12)
        # st.form_submit_button()

    st.subheader("Wind")

    col1, col2, col3 = st.columns(3)
    with col1:
        wind_speed_9am = st.number_input("Wind Speed 9am", value=9.0)
        wind_speed_3pm = st.number_input("Wind Speed 3pm", value=15.0)


        # Calculating wind speed at 9am and 3pm
        wind_speed_mean = (wind_speed_9am + wind_speed_3pm) / 2
        wind_speed_diff = abs(wind_speed_9am - wind_speed_3pm)

    with col2:
        wind_gust_speed = st.number_input("Wind Gust Speed", value=30.0)
        wind_gust_dir = st.number_input("Wind Gust Dir Angle", value=200.0)

    with col3:
        wind_dir_9am = st.number_input("Wind Dir 9am Angle", value=120.0)
        wind_dir_3pm = st.number_input("Wind Dir 3pm Angle", value=150.0)

    st.subheader("Pressure")

    col1, col2 = st.columns(2)
    with col1:
        pressure_mean = st.number_input("Pressure Mean", value=1015.0)

    with col2:
        pressure_diff = st.number_input("Pressure Diff", value=3.0)

    st.subheader("Humidity & Cloud")

    col1, col2 = st.columns(2)
    with col1:
        pass

    with col2:
        cloud_mean = st.number_input("Cloud Mean", value=5.0)
        cloud_diff = st.number_input("Cloud Diff", value=2.0)

    st.subheader("Other")

    climate_zone = st.number_input("Climate Zone (Encoded)", value=1.0)

    submitted = st.form_submit_button("Predict")

if submitted:

    features = [
        min_temp, max_temp, rainfall, evaporation, sunshine,
        wind_gust_speed, pressure_mean, pressure_diff,
        wind_speed_mean, wind_speed_diff, humidity_mean, humidity_diff,
        cloud_mean, cloud_diff, temp_range, temp_diff, month,
        wind_dir_9am, wind_dir_3pm, wind_gust_dir,
        climate_zone
    ]

    response = requests.post(API_URL, json={"features": features})

    if response.status_code == 200:
        result = response.json()
        prob = result["probability"]
        prediction = result["prediction"]

        st.subheader("Prediction Result")

        if prediction == 1:
            st.error(f"Rain Expected Tomorrow\nProbability: {prob}")
        else:
            st.success(f"No Rain Expected\nProbability: {prob}")

    else:
        st.error("API Error. Make sure FastAPI server is running.")
