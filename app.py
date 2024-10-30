from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
import recommendation as recommendation
import perfume_review as perfume_review
import logging

app = Flask(__name__, static_folder='frontend')

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    
    # Extract data from the frontend
    stage = data.get('stage', 'ask_occasion')
    user_message = data['message']
    occasion = data.get('occasion')
    intensity = data.get('intensity')
    eventLocation = data.get('location')
    eventDate = data.get('date')
    eventSeason = data.get('season')
    eventWeather = data.get('weather')
    gender = data.get('gender')

    logging.debug(f"Received data: {data}")
    
    # Initialize response values
    bot_message = ""
    next_stage = stage

    # Stage handling logic
    if stage == 'ask_occasion':
        if occasion in ["Party", "Professional Event", "Casual Event", "Formal Event", "Sports Event", "Romantic", "Outdoor Event", "Religious Event"]:
            bot_message = "Please select the perfume intensity."
            next_stage = 'ask_intensity'
        else:
            bot_message = "I didn't quite get that. Could you please tell me about the occasion you're attending?"
            next_stage = 'ask_occasion'
    
    elif stage == 'ask_intensity':
        if intensity in ["Light", "Moderate", "Intense"]:
            bot_message = "Please select your gender."
            next_stage = 'ask_gender'
        else:
            bot_message = "Please select the intensity from Light, Moderate, or Strong."
            next_stage = 'ask_intensity'

    elif stage == 'ask_gender':
        if gender in ["Male", "Female", "Unisex"]:
            bot_message = f"Great! I will consider that. Please provide the event location and date."
            next_stage = 'ask_location_date'
        else:
            bot_message = "Please select a gender: Male, Female, or Unisex."
            next_stage = 'ask_gender'


    elif stage == 'ask_location_date':
        logging.debug(f"User input for location and date: {user_message}")

        eventLocation, eventDate = recommendation.extract_location_and_date(user_message)

        if eventLocation and eventDate:
            logging.debug(f"Extracted location: {eventLocation}, Extracted date: {eventDate}")

            eventSeason = recommendation.get_season(eventLocation, eventDate)
            eventWeather = recommendation.get_weather(eventLocation, eventDate)

            # bot_message = f"Your event is in {eventLocation} during {eventSeason}. Please select your gender."

            features = recommendation.preprocess_input(occasion, eventSeason, eventLocation, eventDate, intensity, gender)
            recommended_perfume = recommendation.recommend_perfume(features)
            logging.debug(f"Recommended perfume: {recommended_perfume}")
            bot_message += f" We recommend you to wear: {recommended_perfume['name']}."
            next_stage = 'ask_another_recommendation'
        else:
            logging.debug("Failed to extract location or date, requesting re-entry")
            next_stage = 'ask_location_date'


    elif stage == 'ask_another_recommendation':
        if user_message.lower() == 'yes':
            bot_message = "Let's start again! Tell me about the occasion you're attending."
            next_stage = 'ask_occasion'
        else:
            bot_message = "Thank you for using FragranceFitter! Have a great day."
            next_stage = 'end'


    return jsonify({
        'bot_message': bot_message,
        'next_step': next_stage,
        'occasion': occasion,
        'intensity': intensity,
        'location': eventLocation,
        'date': eventDate,
        'season': eventSeason,
        'weather': eventWeather,
        'gender': gender,
        'recommended_perfume': recommended_perfume if 'recommended_perfume' in locals() else None
    })






@app.route('/search', methods=['POST'])
def search():
    data = request.json
    perfume_name = data['perfume_name']
    results = perfume_review.search_perfume(perfume_name)
    logging.debug(f"Search results: {results}")
    return jsonify({'results': results})

@app.route('/add_review', methods=['POST'])
def add_review():
    data = request.json
    perfume_name = data.get('perfume_name')
    user_name = data.get('user_name')
    review = data.get('review')  # Fixed key to match JavaScript
    date = data.get('date_posted', datetime.now().isoformat())  # Default to current time if not provided

    perfume_review.add_review(perfume_name, user_name, review, date)
    logging.debug(f"Review added: {perfume_name}, {user_name}, {review}, {date}")
    return jsonify({'status': 'success'})


@app.route('/recent_reviews', methods=['GET'])
def recent_reviews():
    try:
        reviews = perfume_review.get_recent_reviews()
        if reviews:
            logging.debug(f"Recent reviews: {reviews}")
            return jsonify({'reviews': reviews}), 200
        else:
            logging.warning("No reviews found.")
            return jsonify({'reviews': []}), 200
    except Exception as e:
        logging.error(f"Error retrieving reviews: {e}")
        return jsonify({'error': 'Failed to retrieve reviews'}), 500




if __name__ == "__main__":
    app.run(debug=True)



