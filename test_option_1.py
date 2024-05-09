import unittest
from unittest.mock import patch, MagicMock

# Importing from your specific module
from weather_data_vis import get_coordinates, create_weather_map, fetch_weather_data, plot_temperature_trends

class TestWeatherTool(unittest.TestCase):
    def test_get_coordinates_success(self):
        # Test successful retrieval of coordinates
        with patch('weather_data_vis.requests.get') as mocked_get:
            # Mock the API response
            mocked_get.return_value.status_code = 200
            mocked_get.return_value.json.return_value = [{'lat': 40.7128, 'lon': -74.0060}]
            
            lat, lon = get_coordinates('New York', 'fake_api_key')
            self.assertEqual(lat, 40.7128)
            self.assertEqual(lon, -74.0060)

    def test_get_coordinates_failure(self):
        # Test failure to retrieve coordinates
        with patch('weather_data_vis.requests.get') as mocked_get:
            mocked_get.return_value.status_code = 404
            mocked_get.return_value.json.return_value = []
            
            lat, lon = get_coordinates('InvalidCity', 'fake_api_key')
            self.assertIsNone(lat)
            self.assertIsNone(lon)

    def test_create_weather_map(self):
        # Test creation of weather map HTML file
        lat, lon = 40.7128, -74.0060
        city = "New York"
        description = "clear sky"
        temperature = 25
        with patch('weather_data_vis.folium.Map') as mocked_map:
            mocked_map.return_value.save = MagicMock()
            create_weather_map(lat, lon, city, description, temperature)
            mocked_map.return_value.save.assert_called_once_with(f"{city}_WeatherMap.html")

    def test_fetch_weather_data(self):
        # Test fetching weather data
        with patch('weather_data_vis.requests.get') as mocked_get:
            mocked_get.return_value.status_code = 200
            mocked_get.return_value.json.return_value = {
                "daily": [{"temp": 280, "dt": 1609515600}]
            }
            
            result = fetch_weather_data(40.7128, -74.0060, 1, 'fake_api_key')
            self.assertIsInstance(result, list)
            self.assertEqual(result[0]['temp'], 280)

    def test_plot_temperature_trends(self):
        # Test plotting function does not raise errors
        with patch('weather_data_vis.plt.show'):
            dates = [1609515600, 1609602000]
            temps = [280, 285]
            try:
                plot_temperature_trends(dates, temps)
                self.assertTrue(True)
            except Exception as e:
                self.fail(f"plot_temperature_trends raised an exception {e}")

# Running tests
if __name__ == "__main__":
    unittest.main()
