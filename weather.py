import os

from aiogram.client.session import aiohttp

class WeatherGet:
    def __init__(self, json_data):
        self.temp = 0
        self.wind = 0
        self.humidity = 0
        self.status = ""
        self.__parse_from_json(json_data)

    def __parse_from_json(self, json_data):
        current_weather = json_data.get("current", {})
        self.temp = current_weather.get("temp_c")
        self.wind = current_weather.get("wind_kph")
        self.status = current_weather.get("condition", {}).get("text")
        self.humidity = current_weather.get("humidity")

    def as_text(self):
        return (f"""
                Weather:
                Status: {self.status}
                Temperature: {self.temp} ℃
                Humidity: {self.humidity} %
                Wind: {self.wind} Km/h
                """)

class Weather:
    def __init__(self):
        self.base_url = "http://api.weatherapi.com/v1"
        self.token = os.getenv('WEATHER_TOKEN')

    async def get_current(self, city):
        url = self.base_url + '/current.json'
        params = [("key", self.token), ("q", city)]
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=params) as resp:
                resp.raise_for_status()
                weather_json = await resp.json()
                return WeatherGet(weather_json)