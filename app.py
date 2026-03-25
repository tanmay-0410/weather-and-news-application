from flask import Flask, render_template, jsonify
from config import Config
from services.weather_service import get_weather
from services.news_service import get_news
import os

app = Flask(__name__)
app.config.from_object(Config)

# --- ROUTES FOR PAGES ---

@app.route('/')
def index():
    """Renders the home/landing page."""
    return render_template('index.html')

@app.route('/weather')
def weather_page():
    """Renders the weather search page."""
    return render_template('weather.html')

@app.route('/news')
def news_page():
    """Renders the news search page."""
    return render_template('news.html')

# --- API ENDPOINTS ---

@app.route('/api/weather/<city>')
def api_get_weather(city):
    """
    Endpoint for frontend to fetch weather data.
    """
    weather_data = get_weather(
        city_name=city, 
        api_key=app.config['WEATHER_API_KEY'], 
        base_url=app.config['WEATHER_BASE_URL']
    )
    
    # Check if the service returned an error dictionary
    if "error" in weather_data:
        return jsonify(weather_data), 400
        
    return jsonify(weather_data)

@app.route('/api/news/<country_code>')
def api_get_news(country_code):
    """
    Endpoint for frontend to fetch news data based on country code.
    """
    news_data = get_news(
        country_code=country_code, 
        api_key=app.config['NEWS_API_KEY'], 
        base_url=app.config['NEWS_BASE_URL']
    )
    
    # Check if the service returned an error dictionary
    if isinstance(news_data, dict) and "error" in news_data:
        return jsonify(news_data), 400
        
    return jsonify(news_data)

if __name__ == '__main__':
    # Run the app in debug mode
    app.run(debug=True, host='0.0.0.0', port=5000)
