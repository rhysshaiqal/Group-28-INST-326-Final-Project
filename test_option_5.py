import unittest
from unittest.mock import patch, MagicMock
import requests
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def get_coordinates(city, api_key):
    geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    response = requests.get(geocode_url)
    data = response.json()
    if data:
        return data[0]['lat'], data[0]['lon']
    else:
        print("City not found. Please check the city name.")
        return None, None

def fetch_weather_data(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,daily,current,alerts&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data['hourly']

def prepare_data_for_heatmap(hourly_data, param='humidity'):
    times = [datetime.fromtimestamp(h['dt']) for h in hourly_data]
    values = [h[param] for h in hourly_data]
    df = pd.DataFrame({
        'Time': times,
        'Hour': [t.hour for t in times],
        'Day': [t.day for t in times],
        param: values
    })
    heatmap_data = df.pivot(index="Hour", columns="Day", values=param)
    return heatmap_data

def plot_heatmap(data, title):
    plt.figure(figsize=(12, 8))
    sns.heatmap(data, annot=True, fmt=".0f", linewidths=.5, cmap='coolwarm')
    plt.title(title)
    plt.ylabel('Hour of Day')
    plt.xlabel('Day of Month')
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

    @patch('requests.get')
    def test_fetch_weather_data(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {'hourly': [{'dt': 1601510400, 'humidity': 80}]})
        hourly_data = fetch_weather_data(40.7128, -74.0060, "1c4d04f2dc3ffc15fe62bd4f1c73e19b")
        self.assertEqual(hourly_data[0]['humidity'], 80)

    def test_prepare_data_for_heatmap(self):
        hourly_data = [{'dt': 1601510400, 'humidity': 80}]
        heatmap_data = prepare_data_for_heatmap(hourly_data, 'humidity')
        self.assertIsInstance(heatmap_data, pd.DataFrame)
        self.assertEqual(heatmap_data.loc[0][1], 80)

    @patch('matplotlib.pyplot.show')
    def test_plot_heatmap(self, mock_show):
        data = pd.DataFrame({
            (1, 1): 80
        }, index=[0], columns=pd.MultiIndex.from_tuples([(1, 1)]))
        plot_heatmap(data, "Heatmap Test")
        mock_show.assert_called_once()

if __name__ == '__main__':
    unittest.main()
