import requests

class WeatherService:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_weather(self, location):
        url = f'https://api.weatherapi.com/v1/current.json?key={self.api_key}&q={location}'
        response = requests.get(url)
        data = response.json()
        return data['current']['temp_c']