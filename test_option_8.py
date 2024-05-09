import unittest
from unittest.mock import patch, MagicMock
import requests
import matplotlib.pyplot as plt
from meteostat import Point, Daily
from datetime import datetime
import pandas as pd

def get_coordinates(city_name, api_key):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    if data:
        return data[0]['lat'], data[0]['lon']
    else:
        print("City not found. Please check the city name.")
        return None, None

def fetch_precipitation_data(lat, lon, start_date, end_date):
    location = Point(lat, lon)
    data = Daily(location, start=start_date, end=end_date)
    data = data.fetch()
    return data['prcp']

def plot_daily_precipitation(data, city_name, year):
    plt.figure(figsize=(10, 5))
    data.plot()
    plt.title(f'Daily Precipitation in {city_name} for {year}')
    plt.xlabel('Date')
    plt.ylabel('Precipitation (mm)')
    plt.grid(True)
    plt.show()

def plot_cumulative_precipitation(data, city_name, year):
    cumulative_prcp = data.cumsum()
    plt.figure(figsize=(10, 5))
    cumulative_prcp.plot()
    plt.title(f'Cumulative Precipitation in {city_name} for {year}')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Precipitation (mm)')
    plt.grid(True)
    plt.show()

class TestWeatherData(unittest.TestCase):
    @patch('requests.get')
    def test_get_coordinates(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: [{'lat': 40.7128, 'lon': -74.0060}])
        lat, lon = get_coordinates("New York", "1c4d04f2dc3ffc15fe62bd4f1c73e19b")
        self.assertEqual((lat, lon), (40.7128, -74.0060))
        mock_get.return_value = MagicMock(status_code=404, json=lambda: {})
        lat, lon = get_coordinates("Unknown City", "1c4d04f2dc3ffc15fe62bd4f1c73e19b")
        self.assertIsNone(lat)

    @patch('meteostat.Daily.fetch')
    def test_fetch_precipitation_data(self, mock_fetch):
        mock_fetch.return_value = pd.Series([0, 5, 10], index=pd.to_datetime(['2021-01-01', '2021-01-02', '2021-01-03']))
        prcp_data = fetch_precipitation_data(40.7128, -74.0060, datetime(2021, 1, 1), datetime(2021, 1, 3))
        self.assertEqual(list(prcp_data), [0, 5, 10])

    @patch('matplotlib.pyplot.show')
    def test_plot_functions(self, mock_show):
        prcp_data = pd.Series([0, 5, 10], index=pd.to_datetime(['2021-01-01', '2021-01-02', '2021-01-03']))
        plot_daily_precipitation(prcp_data, "New York", 2021)
        plot_cumulative_precipitation(prcp_data, "New York", 2021)
        self.assertEqual(mock_show.call_count, 2)

if __name__ == "__main__":
    unittest.main()
