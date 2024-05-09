import unittest
from unittest.mock import patch, MagicMock
import requests
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def get_coordinates(city, api_key):
    geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    response = requests.get(geocode_url)
    data = response.json()
    if data:
        return data[0]['lat'], data[0]['lon']
    else:
        print("City not found. Please check the city name.")
        return None, None

def fetch_weather_data(lat, lon, num_days, api_key):
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,current,alerts&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data['daily'][:num_days]

def plot_wind_speed_and_direction(daily_data):
    if not daily_data:
        print("No data available to plot.")
        return
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, polar=True)
    wind_speeds = [day['wind_speed'] for day in daily_data]
    wind_directions = [np.deg2rad(day['wind_deg']) for day in daily_data]
    dates = [datetime.fromtimestamp(day['dt']).strftime('%Y-%m-%d') for day in daily_data]
    bars = ax.bar(wind_directions, wind_speeds, width=0.1, bottom=0.1, alpha=0.65, color='b', edgecolor='black')
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_title('Wind Speed and Direction Over Time', va='bottom', fontsize=15)
    plt.legend(['Wind Speed (m/s)'], loc="upper right", frameon=False)
    plt.show()

class TestWeatherFunctions(unittest.TestCase):
    @patch('requests.get')
    def test_get_coordinates(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: [{'lat': 40.7128, 'lon': -74.0060}])
        lat, lon = get_coordinates("New York", "1c4d04f2dc3ffc15fe62bd4f1c73e19b")
        self.assertEqual((lat, lon), (40.7128, -74.0060))
        mock_get.return_value = MagicMock(status_code=404, json=lambda: {})
        lat, lon = get_coordinates("Unknown City", "1c4d04f2dc3ffc15fe62bd4f1c73e19b")
        self.assertIsNone(lat)
        self.assertIsNone(lon)

    @patch('requests.get')
    def test_fetch_weather_data(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {'daily': [{'dt': 1601510400, 'pop': 0.3, 'weather': [{'main': 'Rain'}], 'wind_speed': 5, 'wind_deg': 270}]})
        daily_data = fetch_weather_data(40.7128, -74.0060, 1, "1c4d04f2dc3ffc15fe62bd4f1c73e19b")
        self.assertEqual(len(daily_data), 1)
        self.assertEqual(daily_data[0]['pop'], 0.3)

    @patch('matplotlib.pyplot.show')
    def test_plot_wind_speed_and_direction(self, mock_show):
        daily_data = [{'dt': 1601510400, 'pop': 0.3, 'weather': [{'main': 'Rain'}], 'wind_speed': 5, 'wind_deg': 270}]
        plot_wind_speed_and_direction(daily_data)
        mock_show.assert_called_once()

if __name__ == '__main__':
    unittest.main()
