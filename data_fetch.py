import requests

def fetch_weather_data(api_key, location):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={location}"
    response = requests.get(complete_url)
    return response.json()