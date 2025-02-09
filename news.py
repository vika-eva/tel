from bs4 import BeautifulSoup
import random
import requests

JOKE_URL = "https://tourbaza.com.ua/smishni-anekdoty/"


def get_random_joke():
    try:
        response = requests.get(JOKE_URL, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        jokes = [p.text.strip() for p in soup.find_all("p") if len(p.text.strip()) > 20]
        if jokes:
            return random.choice(jokes)
        else:
            return "❌ Анекдоти не знайдені."

    except requests.exceptions.RequestException as e:
        return f"❌ Помилка отримання анекдотів: {e}"