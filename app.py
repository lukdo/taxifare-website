# import streamlit as st

# '''
# # TaxiFareModel front
# '''

# st.markdown('''
# Remember that there are several ways to output content into your web page...

# Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
# ''')

# '''
# ## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

# 1. Let's ask for:
# - date and time
# - pickup longitude
# - pickup latitude
# - dropoff longitude
# - dropoff latitude
# - passenger count
# '''

# '''
# ## Once we have these, let's call our API in order to retrieve a prediction

# See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

# 🤔 How could we call our API ? Off course... The `requests` package 💡
# '''

# url = 'https://taxifare.lewagon.ai/predict'

# if url == 'https://taxifare.lewagon.ai/predict':

#     st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

# '''

# 2. Let's build a dictionary containing the parameters for our API...

# 3. Let's call our API using the `requests` package...

# 4. Let's retrieve the prediction from the **JSON** returned by the API...

# ## Finally, we can display the prediction to the user
# '''



import streamlit as st
import requests
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Taxi Fare Predictoooor", page_icon="🚕")

st.title("🚕 TaxiFareModel VROUM VROOOOUM 🤑🤑")

st.markdown(
    """
This page lets you enter the details of a taxi ride and get a predicted price
from a **prediction API**.

You can plug in **your own API** (from the previous unit) or use the
Le Wagon demo API.
"""
)

# === 1. API URL =================================================================
default_url = "https://taxifare.lewagon.ai/predict"

api_url = st.text_input(
    "Prediction API URL",
    value=default_url,
    help="Use your own API endpoint if you have one, or keep the Le Wagon demo URL.",
)

if api_url == default_url:
    st.info("Using the Le Wagon demo API. Replace the URL if you deployed your own API.")


# === 2. Ride parameters =========================================================
st.header("1️⃣ Choose the ride parameters")

col_date, col_time = st.columns(2)
with col_date:
    pickup_date = st.date_input("Pickup date")
with col_time:
    pickup_time = st.time_input("Pickup time")

# Combine date + time into a string for the API
pickup_datetime = datetime.combine(pickup_date, pickup_time)
pickup_datetime_str = pickup_datetime.strftime("%Y-%m-%d %H:%M:%S")

col1, col2 = st.columns(2)
with col1:
    pickup_longitude = st.number_input("Pickup longitude", value=-73.985428)
    pickup_latitude = st.number_input("Pickup latitude", value=40.748817)
with col2:
    dropoff_longitude = st.number_input("Dropoff longitude", value=-73.985428)
    dropoff_latitude = st.number_input("Dropoff latitude", value=40.748817)

passenger_count = st.number_input(
    "Passenger count",
    min_value=1,
    max_value=8,
    value=1,
    step=1,
)


# === 3. Show a small map (optional) =============================================
with st.expander("🔍 Show pickup & dropoff on a map"):
    df_map = pd.DataFrame(
        [
            {"lat": pickup_latitude, "lon": pickup_longitude, "type": "pickup"},
            {"lat": dropoff_latitude, "lon": dropoff_longitude, "type": "dropoff"},
        ]
    )
    st.map(df_map[["lat", "lon"]])


# === 4. Call the API and display result ========================================
st.header("2️⃣ Get the predicted fare")

if st.button("Predict fare 🚀"):
    # 2. Build the params dictionary expected by the API
    params = {
        "pickup_datetime": pickup_datetime_str,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": int(passenger_count),
    }

    st.write("Sending the following parameters to the API:")
    st.json(params)

    try:
        # 3. Call the API
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()

        # 4. Retrieve prediction from JSON
        data = response.json()

        # Different APIs might use different keys; try a few common ones
        prediction = (
            data.get("fare_amount")
            or data.get("fare")
            or data.get("prediction")
            or data.get("result")
        )

        st.subheader("Prediction result")
        if prediction is not None:
            st.success(f"💰 Predicted fare: **{prediction:.2f} USD**")
        else:
            st.warning("API responded but I couldn't find the prediction key in the JSON.")
            st.json(data)

    except requests.exceptions.RequestException as e:
        st.error(f"Error while calling the API: {e}")


    st.json(data)
