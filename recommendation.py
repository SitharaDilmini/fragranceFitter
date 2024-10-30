import joblib
import pandas as pd
import requests
import spacy
import sqlite3
from datetime import datetime, timedelta
from dateutil import parser, relativedelta
import re
import weather_and_season as ws
import logging

# Load the model and encoders
model = joblib.load('model/perfume_recommender_model.pkl')
encoders = {}
for col in ['Occasion', 'Intensity', 'Gender', 'Name', 'Season', 'Weather']:
    encoders[col] = joblib.load(f'label_encoders/{col}_encoder.pkl')

nlp = spacy.load("en_core_web_sm")

API_KEY = '8d1fe096d184452c3c21749ec4bd295e'  

def get_user_input(prompt):
    return input(prompt).strip().lower()

def extract_occasion(occasion_info):
    doc = nlp(occasion_info)
    occasion = None

    # Define a list of common occasions with their categories
    occasion_keywords = {
        'Party': ['Party'],
        'Professional Event': ['Professional Event'],
        'Casual Event': ['Casual Event'],
        'Formal Event': ['Formal Event'],
        'Sports Event': ['Sports Event'],
        'Romantic': ['Date', 'Romantic'],
        'Outdoor Event': ['Outdoor Event'],
        'Religious Event': ['Religious Event'],  
    }

    # Helper function to categorize the occasion
    def categorize_occasion(keywords, occasion_info):
        for category, values in keywords.items():
            for value in values:
                if value in occasion_info:
                    return category
        return None

    # Check for NER event labels
    for ent in doc.ents:
        if ent.label_ == 'EVENT':
            occasion = categorize_occasion(occasion_keywords, ent.text)
            if occasion:
                return occasion

    # Check for keyword matches if NER doesn't find anything
    if not occasion:
        occasion = categorize_occasion(occasion_keywords, occasion_info)
    
    return occasion

def extract_intensity(user_message):
    intensities = {
        "light": ["Light", "low", "mild", "soft", "gentle", "subtle", "little"],
        "moderate": ["Moderate", "medium", "average", "normal", "balanced", "modest", "neutral"],
        "intense": ["Strong", "intense", "heavy", "powerful", "rich", "bold", "loud", "high"]
    }
    user_message = user_message.lower()
    for key, synonyms in intensities.items():
        for synonym in synonyms:
            if synonym in user_message:
                return key

def extract_location_and_date(location_and_date):
    doc = nlp(location_and_date)
    location = None
    date = None
    for ent in doc.ents:
        logging.debug(f"Entity found: {ent.text}, Label: {ent.label_}")
        if ent.label_ in ['GPE', 'LOC']:
            location = ent.text
        if ent.label_ == 'DATE':
            date = ent.text

    if date:
        try:
            date_obj = parser.parse(date, fuzzy=True)
        except Exception as e:
            logging.debug(f"Date parsing error: {e}")
            # Handle relative dates like "tomorrow", "next Friday", "in two weeks"
            today = datetime.today()
            if "tomorrow" in date.lower():
                date_obj = today + timedelta(days=1)
            elif "next" in date.lower():
                date_obj = today + relativedelta.relativedelta(weekday=parser.parse(date).weekday())
            elif "in" in date.lower():
                num_days = int([int(s) for s in date.split() if s.isdigit()][0])
                date_obj = today + timedelta(days=num_days)
            else:
                date_obj = today
        date = date_obj.strftime('%Y-%m-%d')

    logging.debug(f"Extracted location: {location}, date: {date}")
    return location, date

def get_season(location, date):
    season = ws.predict_season(location, date)
    return season
    
def get_weather(location, date):
    try:
        weather = ws.predict_weather(location, date)
        logging.debug(f"Predicted weather: {weather}")
        
    except Exception as e:
        logging.warning(f"Error fetching weather data: {e}")
        weather = None
    return weather


def extract_gender(user_message):
    genders = {
        "male": ["male", "men", "boy"],
        "female": ["female", "women", "girl"],
        "unisex": ["unisex", "both", "everyone"]
    }

    user_message = user_message.lower()

    for key, synonyms in genders.items():
        for synonym in synonyms:
            # Use regular expression to match whole words
            if re.search(r'\b' + re.escape(synonym) + r'\b', user_message):
                return key
    return None


def preprocess_input(occasion, season, location, date, intensity, gender):
    # Get the weather directly from the get_weather function
    weather = get_weather(location, date)
    logging.debug(f"Preprocessed weather: {weather}")
    occasion = extract_occasion(occasion)
    logging.debug(f"Preprocessed occasion: {occasion}")
    
    def safe_transform(encoder, value, category):
        logging.debug(f"Transforming value '{value}' for category '{category}'")
        if value is None:
            logging.warning(f"Value for category '{category}' is None. Using default value.")
            return encoder.transform([encoder.classes_[0]])[0]
        if value in encoder.classes_:
            return encoder.transform([value])[0]
        else:
            logging.warning(f"'{value}' is an unseen label for the category '{category}'. Using default value.")
            return encoder.transform([encoder.classes_[0]])[0]

    occasion_enc = safe_transform(encoders['Occasion'], occasion, 'Occasion')
    season_enc = safe_transform(encoders['Season'], season, 'Season')
    weather_enc = safe_transform(encoders['Weather'], weather, 'Weather')
    intensity_enc = safe_transform(encoders['Intensity'], intensity, 'Intensity')
    gender_enc = safe_transform(encoders['Gender'], gender, 'Gender')
    
    logging.debug(f"Encoded values - Occasion: {occasion_enc}, Season: {season_enc}, Weather: {weather_enc}, Intensity: {intensity_enc}, Gender: {gender_enc}")

    return pd.DataFrame([[occasion_enc, season_enc, weather_enc, intensity_enc, gender_enc]], columns=['Occasion', 'Season', 'Weather', 'Intensity', 'Gender'])



def recommend_perfume(features):
    prediction = model.predict(features)
    perfume_name = encoders['Name'].inverse_transform(prediction)[0]
    
    # Query the database for the perfume details
    conn = sqlite3.connect('fragranceFitter.db')
    c = conn.cursor()
    c.execute('SELECT name, brand, description, image_url FROM perfumes WHERE name = ?', (perfume_name,))
    result = c.fetchone()
    conn.close()
    
    if result:
        perfume_details = {
            'name': result[0],
            'brand': result[1],
            'description': result[2],
            'image_url': result[3]
        }
        return perfume_details
    else:
        return {'name': perfume_name, 'brand': '', 'description': 'Details not found', 'image_url': ''}


