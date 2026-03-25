import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class."""
    
    # Secret Key for Flask sessions (if needed, but good practice to include)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key-for-dev')
    
    # API Keys
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
    
    # Base URLs for external APIs
    WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    NEWS_BASE_URL = "https://gnews.io/api/v4/top-headlines"
