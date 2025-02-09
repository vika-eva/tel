import os
import requests

NASA_API_KEY = os.getenv('NASA_API_KEY')
NASA_API_URL = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"

def get_nasa_photo():
    try:
        response = requests.get(NASA_API_URL, timeout=5)
        data = response.json()
        title = data.get("title")
        image_url = data.get("hdurl") or data.get("url")
        return title, image_url

    except requests.exceptions.RequestException as e:
        return f"шось пішло не так {e}"