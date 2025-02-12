import os
import requests

NASA_API_KEY = os.getenv('NASA_API_KEY')
NASA_API_URL = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"

def get_nasa_photo():
    try:
        response = requests.get(NASA_API_URL, timeout=10)
        data = response.json()
        title = data.get("title")
        image_url = data.get("hdurl") or data.get("url")

        if image_url and (image_url.endswith(".jpg") or image_url.endswith(".png")):
            return "image", title, image_url
        else:
            return "video", title, image_url

    except requests.exceptions.RequestException as e:
        return "error", f"❌ Помилка отримання фото: {e}", None
