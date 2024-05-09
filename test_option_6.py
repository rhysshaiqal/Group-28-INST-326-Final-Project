import unittest
from unittest.mock import patch, MagicMock
import requests
import plotly.graph_objects as go
from datetime import datetime, timedelta

def get_coordinates(city, api_key):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    if data:
        return data[0]['lat'], data[0]['lon']
    else:
        print("City not found. Please check the city name.")
        return None, None

def fetch_weather_alerts(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,daily&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    return data.get('alerts', [])

def plot_alerts_on_timeline(alerts):
    if not alerts:
        print("No alerts to display.")
        return

    fig = go.Figure()
    for alert in alerts:
        start_time = datetime.fromtimestamp(alert['start'])
        end_time = datetime.fromtimestamp(alert['end'])
        duration = end_time - start_time
        duration_str = str(duration)[:-3]
        fig.add_trace(go.Scatter(
            x=[start_time, end_time],
            y=[alert['event'], alert['event']],
            mode='lines+markers+text',
            name=alert['sender_name'],
            text=[None, f"{duration_str} hrs"],
            textposition="top right",
            hoverinfo="text",
            hovertext=f"{alert['description']}<br>From: {start_time}<br>To: {end_time}<br>Duration: {duration_str} hrs"
        ))

    fig.update_layout(
        title="Weather Alerts Timeline",
        xaxis_title="Time",
        yaxis_title="Alert Type",
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            type="date"
        )
    )
    fig.show()

class TestWeatherAlertFunctions(unittest.TestCase):
    @patch('requests.get')
    def test_get_coordinates(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: [{'lat': 40.7128, 'lon': -74.0060}])
        lat, lon = get_coordinates("New York", "1c4d04f2dc3ffc15fe62bd4f1c73e19b")
        self.assertEqual((lat, lon), (40.7128, -74.0060))
        mock_get.return_value = MagicMock(status_code=404, json=lambda: {})
        lat, lon = get_coordinates("Unknown City", "1c4d04f2dc3ffc15fe62bd4f1c73e19b")
        self.assertIsNone(lat)

    @patch('requests.get')
    def test_fetch_weather_alerts(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {'alerts': [{'start': 1601510400, 'end': 1601596800, 'event': 'Rain', 'description': 'Heavy rain', 'sender_name': 'Weather Center'}]})
        alerts = fetch_weather_alerts(40.7128, -74.0060, "1c4d04f2dc3ffc15fe62bd4f1c73e19b")
        self.assertIsInstance(alerts, list)
        self.assertEqual(alerts[0]['event'], 'Rain')

    @patch('plotly.graph_objects.Figure.show')
    def test_plot_alerts_on_timeline(self, mock_show):
        alerts = [{'start': 1601510400, 'end': 1601596800, 'event': 'Rain', 'description': 'Heavy rain', 'sender_name': 'Weather Center'}]
        plot_alerts_on_timeline(alerts)
        mock_show.assert_called_once()

if __name__ == '__main__':
    unittest.main()
