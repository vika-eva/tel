
import requests
import os

URL_API_BANK=os.getenv('URL_API_BANK')


def load_exchange():
    try:
        response = requests.get(URL_API_BANK, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"😱 ой щось пішло не так: {e}"


def format_exchange():
    data = load_exchange()
    if isinstance(data, str):
        return data

    text = "💱 поточний курс валют:"
    for item in data:
        text += (f"""
        💎 {item.get('ccy', 'not info')}/{item.get('base_ccy', 'not info')}
                  📉 Покупка: {item.get('buy', 'not info')}
                  📈 Продажа: {item.get('sale', 'not info')}
                  """)
    return text
