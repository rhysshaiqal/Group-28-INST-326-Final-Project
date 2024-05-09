import unittest
from unittest.mock import patch, MagicMock
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone
import matplotlib.dates as mdates

def get_coordinates(city, api_key):
    geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    response = requests.get(geocode_url)
    data = response.json()
    if data:
        return data[0]['lat'], data[0]['lon']
    else:
        return None, None

def kelvin_to_fahrenheit(kelvin_temp):
    return (kelvin_temp - 273.15) * 9/5 + 32

def fetch_weather_data(lat, lon, num_days, api_key):
    current_time = datetime.now(timezone.utc)
    temps, dates = [], []
    for i in range(num_days):
        dt = current_time - timedelta(days=i)
        timestamp = int(datetime.timestamp(dt))
        url = f'https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={timestamp}&appid={api_key}'
        response = requests.get(url)
        data = response.json()
        if 'data' in data and len(data['data']) > 0:
            day_data = data['data'][0]
            fahrenheit_temp = kelvin_to_fahrenheit(day_data['temp'])
            temps.append(fahrenheit_temp)
            dates.append(dt)
    return dates, temps

def plot_temperature_trends(dates, temps):
    if not temps:
        print("Temperature data is empty.")
        return
    plt.figure(figsize=(12, 6))
    plt.plot(dates, temps, marker='o', linestyle='-', color='mediumvioletred', markersize=8)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.gcf().autofmt_xdate()
    plt.title('Daily Temperature Trends in Fahrenheit', fontsize=14, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Temperature (°F)', fontsize=12)
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.fill_between(dates, temps, color="lavender", alpha=0.3)
    plt.show()

class TestWeatherFunctions(unittest.TestCase):
    @patch('requests.get')
    def test_get_coordinates(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: [{'lat': 40.7128, 'lon': -74.0060}])
        lat, lon = get_coordinates("New York", '1c4d04f2dc3ffc15fe62bd4f1c73e19b')
        self.assertEqual((lat, lon), (40.7128, -74.0060))

    def test_kelvin_to_fahrenheit(self):
        self.assertEqual(kelvin_to_fahrenheit(273.15), 32)

    @patch('requests.get')
    def test_fetch_weather_data(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {'data': [{'temp': 295}]})
        dates, temps = fetch_weather_data(40.7128, -74.0060, 1, '1c4d04f2dc3ffc15fe62bd4f1c73e19b')
        self.assertEqual(len(dates), 1)
        self.assertEqual(temps[0], 71.33000000000004)  

    @patch('matplotlib.pyplot.show')
    def test_plot_temperature_trends_with_no_data(self, mock_show):
        plot_temperature_trends([], [])
        mock_show.assert_not_called()

if __name__ == '__main__':
    unittest.main()
