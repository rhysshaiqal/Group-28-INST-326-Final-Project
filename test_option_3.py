import unittest
from unittest.mock import patch, MagicMock
import requests
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

def get_coordinates(city, api_key='1c4d04f2dc3ffc15fe62bd4f1c73e19b'):
    geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    response = requests.get(geocode_url)
    data = response.json()
    if data:
        return data[0]['lat'], data[0]['lon']
    else:
        print("City not found. Please check the city name.")
        return None, None

def fetch_weather_data(lat, lon, num_days, api_key='1c4d04f2dc3ffc15fe62bd4f1c73e19b'):
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,current,alerts&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data['daily'][:num_days]

def plot_precipitation_and_events(daily_data):
    if not daily_data:
        print("No data available to plot.")
        return
    dates = [datetime.fromtimestamp(day['dt']) for day in daily_data]
    precipitation = [day['pop'] * 100 for day in daily_data]
    weather_conditions = [day['weather'][0]['main'] for day in daily_data]
    fig, ax1 = plt.subplots(figsize=(12, 7))
    colors = ['skyblue' if cond in ['Rain', 'Snow', 'Thunderstorm'] else 'grey' for cond in weather_conditions]
    bars = ax1.bar(dates, precipitation, color=colors, alpha=0.6)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Probability of Precipitation (%)')
    ax2 = ax1.twinx()
    events = [100 if event in ['Rain', 'Snow', 'Thunderstorm'] else 0 for event in weather_conditions]
    ax2.plot(dates, events, 'rD-', markersize=8)
    ax2.set_ylim(0, 110)
    ax2.set_ylabel('Weather Events', color='red')
    ax1.xaxis.set_major_locator(mdates.DayLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    plt.title('Precipitation and Weather Events Over Time')
    fig.tight_layout()
    plt.show()

class TestWeatherApp(unittest.TestCase):
    @patch('requests.get')
    def test_get_coordinates(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: [{'lat': 40.7128, 'lon': -74.0060}])
        lat, lon = get_coordinates("New York")
        self.assertEqual((lat, lon), (40.7128, -74.0060))
        mock_get.return_value = MagicMock(status_code=404, json=lambda: {})
        lat, lon = get_coordinates("Unknown City")
        self.assertIsNone(lat)
        self.assertIsNone(lon)

    @patch('requests.get')
    def test_fetch_weather_data(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {'daily': [{'dt': 1601510400, 'pop': 0.3, 'weather': [{'main': 'Rain'}]}]})
        daily_data = fetch_weather_data(40.7128, -74.0060, 1)
        self.assertEqual(len(daily_data), 1)
        self.assertEqual(daily_data[0]['pop'], 0.3)

    @patch('matplotlib.pyplot.show')
    def test_plot_precipitation_and_events(self, mock_show):
        daily_data = [{'dt': 1601510400, 'pop': 0.3, 'weather': [{'main': 'Rain'}]}]
        plot_precipitation_and_events(daily_data)
        mock_show.assert_called_once()

if __name__ == '__main__':
    unittest.main()
