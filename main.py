"""
Weather Notifier

Author: Alan
Date: September 22nd 2024

Sends an SMS if it's going to rain near your area.
"""

import requests
from twilio.rest import Client

# Twilio account data
account_sid = "your sid"
auth_token = "your auth token"
TWILIO_PHONE = "your account phone"

# Phone you are going to send the message to
YOUR_PHONE = "your phone number"

# Open Weather API Key
API_KEY = "your api key from open weather"

# Open Weather URL
url = "https://api.openweathermap.org/data/2.5/forecast"

# Open Weather API parameters
parameters = {
    "lat": "your lat coords",
    "lon": "your long coords",
    "appid": API_KEY,
    "cnt": 4,
}

def will_rain():
    """
    Uses the Open Weather API to get forecast data to see if it's going to rain
    :return: True if it's going to rain, False if not
    """

    # Makes a request to Open Weather API
    response = requests.get(url=url, params=parameters)

    # Raises an exception if the API is not found
    response.raise_for_status()

    # Stores the data
    weather_data = response.json()

    # For each weather list in the weather data, we will get the weather id
    for weather in weather_data["list"]:
        weather_id = weather["weather"][0]["id"]

        # Based on Open Weather API, codes from 200 to 700 require umbrella for several reasons:
        # sunny, raining, snowing, etc, then return true
        if int(weather_id) < 700:
            return True

    return False

def send_message():
    """
    Uses the twilio library to send a message via SMS
    :return:
    """

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="It's going to rain, please bring an umbrella. ☂️",
        from_=TWILIO_PHONE,
        to=YOUR_PHONE,
    )

if will_rain():
    send_message()
