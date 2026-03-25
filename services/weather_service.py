import requests
import logging

def get_weather(city_name, api_key, base_url):
    """
    Fetches weather data for a given city from OpenWeatherMap API.
    Converts temperature to Celsius automatically using units=metric.
    """
    if not api_key:
        logging.error("Weather API key is missing.")
        return {"error": "API key configuration error."}

    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric" # This ensures temperature is in Celsius
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() # Raise an exception for HTTP errors
        
        data = response.json()
        
        # Parse out only the necessary data to send to frontend
        weather_info = {
            "city": data.get("name"),
            "temperature": round(data["main"]["temp"]),
            "condition": data["weather"][0]["main"],
            "description": data["weather"][0]["description"].title(),
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "icon": data["weather"][0]["icon"]
        }
        
        return weather_info
        
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            return {"error": "City not found. Please try another one."}
        logging.error(f"HTTP error occurred: {http_err}")
        return {"error": "Failed to fetch weather data."}
    except Exception as err:
        logging.error(f"An error occurred: {err}")
        return {"error": "An unexpected error occurred while fetching weather data."}
