import requests
from datetime import datetime, timedelta
from dateutil import parser
import logging

API_KEY = '82d4befc110b4a21bd123921241107'

# Function to get the 15-day weather forecast
def get_15_day_forecast(location):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={location}&days=15"
    response = requests.get(url)
    data = response.json()

    # Check if the API returned an error
    if 'error' in data:
        print(f"Error: {data['error']['message']}")
        return None

    return data['forecast']['forecastday']

# Function to check if a location is in the tropics
def is_tropical(latitude):
    return -30 <= latitude <= 30

# Function to get latitude and longitude of the location
def get_lat_lon(location):
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location}"
    response = requests.get(url)
    data = response.json()

    # Check if the API returned an error
    if 'error' in data:
        print(f"Error: {data['error']['message']}")
        return None, None

    lat = data['location']['lat']
    lon = data['location']['lon']
    return lat, lon

# Function to determine the season based on latitude, hemisphere, and month
def determine_season(latitude, month):
    if latitude >= 60 or latitude <= -60:
        # Arctic and Antarctic regions
        return 'polar day' if month in [4, 5, 6, 7, 8, 9] else 'polar night'
    elif 30 <= latitude < 60 or -60 < latitude <= -30:
        # Mid-latitudes
        if latitude >= 0:  # Northern Hemisphere
            if month in [12, 1, 2]:
                return 'winter'
            elif month in [3, 4, 5]:
                return 'spring'
            elif month in [6, 7, 8]:
                return 'summer'
            else:
                return 'autumn'
        else:  # Southern Hemisphere
            if month in [12, 1, 2]:
                return 'summer'
            elif month in [3, 4, 5]:
                return 'autumn'
            elif month in [6, 7, 8]:
                return 'winter'
            else:
                return 'spring'
    else:
        # Tropics
        return 'wet season' if month in [5, 6, 7, 8, 9, 10] else 'dry season'

# Function to predict season
def predict_season(location, date):
    try:
        date_obj = parser.parse(date)
    except:
        return "Invalid date format."

    lat, lon = get_lat_lon(location)
    if lat is None:
        return "Invalid location."

    if is_tropical(lat):
        return "tropical"

    season = determine_season(lat, date_obj.month)
    return season

# Function to categorize weather conditions
def categorize_weather(condition):
    condition = condition.lower()
    if any(keyword in condition for keyword in ["sunny", "clear"]):
        return "sunny"
    elif any(keyword in condition for keyword in ["cloudy", "overcast"]):
        return "rainy"
    elif any(keyword in condition for keyword in ["rain", "showers", "drizzle"]):
        return "rainy"
    elif any(keyword in condition for keyword in ["storm", "thunder", "lightning"]):
        return "stormy"
    elif any(keyword in condition for keyword in ["snow", "sleet", "blizzard"]):
        return "snowy"
    elif any(keyword in condition for keyword in ["fog", "mist"]):
        return "foggy"
    else:
        return "unknown"


def predict_weather(location, date):
    try:
        date_obj = parser.parse(date)
    except Exception as e:
        logging.debug(f"Invalid date format: {e}")
        return "Invalid date format."

    forecast_data = get_15_day_forecast(location)
    if forecast_data is None:
        logging.debug("Unable to fetch weather data.")
        return "Unable to fetch weather data."

    # Check if the requested date is within the forecast range
    for day in forecast_data:
        forecast_date = parser.parse(day['date'])
        if forecast_date.date() == date_obj.date():
            condition = day['day']['condition']['text']
            categorized_condition = categorize_weather(condition)
            logging.debug(f"Weather on {date}: {condition}, categorized as {categorized_condition}")
            return categorized_condition

    # If the date is outside the 15-day forecast range, use the latest available forecast
    latest_forecast = forecast_data[-1]
    condition = latest_forecast['day']['condition']['text']
    categorized_condition = categorize_weather(condition)
    logging.debug(f"Weather on {date}: {condition}, categorized as {categorized_condition}")
    return categorized_condition
