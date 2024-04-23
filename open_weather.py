import requests
import argparse
from pyfiglet import figlet_format
from simple_chalk import green, red

# Constants for OpenWeatherMap API access
API_KEY = "1c4d04f2dc3ffc15fe62bd4f1c73e19b"
API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Weather icons mapped to API icon codes
ICON_MAP = {
    "01d": "☀", "02d": "🌤", "03d": "☁", "04d": "☁",
    "09d": "🌧", "10d": "🌦", "11d": "🌩", "13d": "❄",
    "50d": "🌫", "01n": "🌑", "02n": "🌥", "03n": "☁",
    "04n": "☁", "09n": "🌧", "10n": "🌦", "11n": "🌩",
    "13n": "❄", "50n": "🌫"
}

# Command-line argument setup
arg_parser = argparse.ArgumentParser(description="Fetch and display weather information for a specific location.")
arg_parser.add_argument("location", help="Specify the city or country for weather details.")
args = arg_parser.parse_args()

# API request setup
request_url = f"{API_BASE_URL}?q={args.location}&appid={API_KEY}&units=metric"

# Performing the API request
response = requests.get(request_url)
if response.status_code != 200:
    print(red("Error: Could not retrieve weather data."))
    exit()

weather_data = response.json()

# Extracting necessary data from the response
temperature = weather_data["main"]["temp"]
feels_like = weather_data["main"]["feels_like"]
weather_desc = weather_data["weather"][0]["description"]
weather_icon_code = weather_data["weather"][0]["icon"]
city_name = weather_data["name"]
country_code = weather_data["sys"]["country"]

# Displaying the result
icon_display = ICON_MAP.get(weather_icon_code, "")
display_output = f"{figlet_format(city_name)}, {country_code}\n"
display_output += f"{icon_display} {weather_desc}\n"
display_output += f"Temperature: {temperature}°C\n"
display_output += f"Feels like: {feels_like}°C\n"

print(green(display_output))
