import requests
import logging

def get_news(country_code, api_key, base_url):
    """
    Fetches the top headlines for a given country from GNews API.
    Limits results to 6 articles to keep the UI clean.
    """
    if not api_key:
        logging.error("News API key is missing.")
        return {"error": "API key configuration error."}

    params = {
        "country": country_code,
        "apikey": api_key, # GNews uses 'apikey' in lowercase
        "max": 6,          # GNews limit parameter
        "lang": "en"       # enforce english language
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()

        data = response.json()
        articles = data.get("articles", [])
        
        processed_articles = []
        for article in articles:
            if not article.get("url"):
                continue
                
            processed_articles.append({
                "title": article.get("title") or "No Title Available",
                "description": article.get("description") or "Click to read more about this story.",
                "url": article.get("url"),
                "image": article.get("image") or "https://via.placeholder.com/400x200?text=No+Image+Available",
                "source": article.get("source", {}).get("name") or "Unknown Source"
            })

        return processed_articles
        
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err} - {response.text}")
        return {"error": "Failed to fetch news data. Please check your API key."}
    except Exception as err:
        logging.error(f"An error occurred: {err}")
        return {"error": "An unexpected error occurred while fetching news data."}
