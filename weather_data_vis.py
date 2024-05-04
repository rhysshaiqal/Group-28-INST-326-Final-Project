def main_menu():
    print("Select the type of weather visualization:")
    print("1. Current Weather and Map")
    print("2. Historical Temperature Trends")
    print("3. Forecast Precipitation and Events")
    print("4. Wind Speed and Direction")
    print("5. Heatmap of Weather Parameter")
    print("6. Weather Alerts Timeline")
    print("7. Historical Temperature Data")
    print("8. Precipitation Data Analysis")
    print("9. Climate Comparison Across Cities")
    print("10. Temperature and Precipitation Overview")
    print("11. Extreme Weather Analysis")
    print("12. Monthly Precipitation Overview")
    print("13. Statistical Analysis of Weather Data")
    print("14. Weather Conditions During Solar Eclipse")

    choice = int(input("Enter your choice (1-14): "))
    return choice

def run_selected_option(choice):
    if choice == 1:

        import requests
        import pyfiglet
        from simple_chalk import chalk
        import folium

        API_KEY = "1c4d04f2dc3ffc15fe62bd4f1c73e19b"
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

        WEATHER_ICONS = {
            "01d": "☀️", "02d": "⛅️", "03d": "☁️", "04d": "☁️",
            "09d": "🌧", "10d": "🌦", "11d": "⛈", "13d": "🌨", "50d": "🌫",
            "01n": "🌙", "02n": "☁️", "03n": "☁️", "04n": "☁️",
            "09n": "🌧", "10n": "🌦", "11n": "⛈", "13n": "🌨", "50n": "🌫",
        }

        def get_coordinates(city, api_key):
            geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
            response = requests.get(geocoding_url)
            data = response.json()
            if data:
                return data[0]['lat'], data[0]['lon']
            else:
                return None, None

        def create_weather_map(lat, lon, city, description, temperature):
            map = folium.Map(location=[lat, lon], zoom_start=12, tiles='OpenStreetMap')
            tooltip_text = f"Current weather in {city}: {description}, {temperature}°C"
            folium.Marker(
                [lat, lon], 
                popup=f"Weather location: {city}",
                tooltip=tooltip_text,  # Adding tooltip text
                icon=folium.Icon(color='red')
            ).add_to(map)
            map.save(f"{city}_WeatherMap.html")

        # Get user input for the city
        city = input("Enter the city to check the weather for: ")

        # Construct API URL with query parameters
        url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"

        # Make API request and parse response
        response = requests.get(url)
        if response.status_code != 200:
            print(chalk.red("Error: Unable to retrieve weather information."))
        else:
            data = response.json()
            lat, lon = get_coordinates(city, API_KEY)

            temperature = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            description = data["weather"][0]["description"]
            icon = data["weather"][0]["icon"]
            weather_icon = WEATHER_ICONS.get(icon, "")

            output = f"{pyfiglet.figlet_format(data['name'])}\n"
            output += f"{weather_icon} {description}\n"
            output += f"Temperature: {temperature}°C\n"
            output += f"Feels like: {feels_like}°C\n"

            print(chalk.green(output))

            if lat and lon:
                create_weather_map(lat, lon, city, description, temperature)
                print(chalk.blue(f"Interactive map saved as {city}_WeatherMap.html"))
        
        
    elif choice == 2:

        import requests
        import matplotlib.pyplot as plt
        from datetime import datetime, timedelta, timezone
        import matplotlib.dates as mdates

        def get_coordinates(city, api_key):
            """Get latitude and longitude for a given city using OpenWeatherMap's Geocoding API."""
            geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
            response = requests.get(geocode_url)
            data = response.json()
            if data:
                return data[0]['lat'], data[0]['lon']
            else:
                return None, None

        def kelvin_to_fahrenheit(kelvin_temp):
            """Converts Kelvin temperature to Fahrenheit."""
            return (kelvin_temp - 273.15) * 9/5 + 32

        def fetch_weather_data(lat, lon, num_days, api_key):
            """Fetches historical weather data using the OpenWeatherMap One Call API."""
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
            """Plots temperature trends."""
            if not temps:
                print("Temperature data is empty.")
                return
            
            plt.figure(figsize=(12, 6))
            plt.plot(dates, temps, marker='o', linestyle='-', color='mediumvioletred', markersize=8)

            # Formatting the date to make it more readable
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
            plt.gcf().autofmt_xdate()  # Rotation
            
            plt.title('Daily Temperature Trends in Fahrenheit', fontsize=14, fontweight='bold')
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Temperature (°F)', fontsize=12)
            plt.grid(True, linestyle='--', linewidth=0.5)
            plt.fill_between(dates, temps, color="lavender", alpha=0.3)  # Fill under line
            
            plt.show()

        # User inputs
        city = input("Enter the city name: ")
        num_days = int(input("Enter the number of days to fetch data for: "))
        api_key = '1c4d04f2dc3ffc15fe62bd4f1c73e19b'  # Replace with your API key

        # Fetch coordinates for the city
        lat, lon = get_coordinates(city, api_key)
        if lat is None or lon is None:
            print("City not found.")
        else:
            # Fetch and plot data
            dates, temps = fetch_weather_data(lat, lon, num_days, api_key)
            plot_temperature_trends(dates, temps)

    
    elif choice == 3:
        import requests
        import matplotlib.pyplot as plt
        from datetime import datetime
        import matplotlib.dates as mdates

        def get_coordinates(city, api_key):
            """Get latitude and longitude for a given city using OpenWeatherMap's Geocoding API."""
            geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
            response = requests.get(geocode_url)
            data = response.json()
            if data:
                return data[0]['lat'], data[0]['lon']
            else:
                print("City not found. Please check the city name.")
                return None, None

        def fetch_weather_data(lat, lon, num_days, api_key):
            """Fetches forecast weather data using the OpenWeatherMap One Call API."""
            url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,current,alerts&appid={api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            return data['daily'][:num_days]  # Return only the number of days requested by the user

        def plot_precipitation_and_events(daily_data):
            """Plots precipitation and weather events."""
            dates = [datetime.fromtimestamp(day['dt']) for day in daily_data]
            precipitation = [day['pop'] * 100 for day in daily_data]  # Probability of precipitation in %
            weather_conditions = [day['weather'][0]['main'] for day in daily_data]

            fig, ax1 = plt.subplots(figsize=(12, 7))

            # Bar chart for precipitation
            colors = ['skyblue' if cond in ['Rain', 'Snow', 'Thunderstorm'] else 'grey' for cond in weather_conditions]
            bars = ax1.bar(dates, precipitation, color=colors, label='Probability of Precipitation (%)', alpha=0.6)
            ax1.set_xlabel('Date')
            ax1.set_ylabel('Probability of Precipitation (%)')
            ax1.tick_params(axis='y')

            # Twin axis for weather events
            ax2 = ax1.twinx()
            weather_events = ['Rain', 'Snow', 'Thunderstorm']
            events = [100 if event in weather_events else 0 for event in weather_conditions]
            ax2.plot(dates, events, 'rD-', label='Significant Weather Events', markersize=8)
            ax2.set_ylim(0, 110)
            ax2.set_ylabel('Weather Events', color='red')
            ax2.tick_params(axis='y', labelcolor='red')

            # Adding annotations for significant weather events
            for i, txt in enumerate(weather_conditions):
                if txt in weather_events:
                    ax2.annotate(txt, (dates[i], events[i]), textcoords="offset points", xytext=(0,10), ha='center')

            # Formatting the date to make it more readable
            ax1.xaxis.set_major_locator(mdates.DayLocator())
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            fig.autofmt_xdate()

            plt.title('Precipitation and Weather Events Over Time', fontsize=16, fontweight='bold')
            fig.tight_layout()
            plt.legend(loc="upper left", bbox_to_anchor=(0,1.12), ncol=2)
            plt.show()

        # User input for city and number of days
        city = input("Enter the city name: ")
        num_days = int(input("Enter the number of days for the forecast (up to 8): "))
        api_key = '1c4d04f2dc3ffc15fe62bd4f1c73e19b'  # Replace with your API key

        # Validate number of days
        if num_days < 1 or num_days > 8:
            print("Invalid number of days. The number must be between 1 and 8.")
        else:
            # Fetch coordinates for the city
            lat, lon = get_coordinates(city, api_key)
            if lat is not None and lon is not None:
                # Fetch and plot data
                daily_data = fetch_weather_data(lat, lon, num_days, api_key)
                plot_precipitation_and_events(daily_data)


    elif choice == 4 :

        import requests
        import matplotlib.pyplot as plt
        import numpy as np
        from datetime import datetime

        def get_coordinates(city, api_key):
            """Get latitude and longitude for a given city using OpenWeatherMap's Geocoding API."""
            geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
            response = requests.get(geocode_url)
            data = response.json()
            if data:
                return data[0]['lat'], data[0]['lon']
            else:
                print("City not found. Please check the city name.")
                return None, None

        def fetch_weather_data(lat, lon, num_days, api_key):
            """Fetches forecast weather data using the OpenWeatherMap One Call API."""
            url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,current,alerts&appid={api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            return data['daily'][:num_days]  # Return only the number of days requested by the user

        def plot_wind_speed_and_direction(daily_data):
            """Plots wind speed and direction on a polar chart."""
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, polar=True)
            
            wind_speeds = [day['wind_speed'] for day in daily_data]
            wind_directions = [np.deg2rad(day['wind_deg']) for day in daily_data]  # Convert degrees to radians for the plot
            dates = [datetime.fromtimestamp(day['dt']).strftime('%Y-%m-%d') for day in daily_data]

            # Create bars for wind speeds
            bars = ax.bar(wind_directions, wind_speeds, width=0.1, bottom=0.1, alpha=0.65, color='b', edgecolor='black')

            # Set descriptions and layout adjustments
            ax.set_theta_zero_location('N')  # Set the direction of "0" degrees to the top of the chart
            ax.set_theta_direction(-1)  # Set the direction of increases in angles clockwise
            ax.set_title('Wind Speed and Direction Over Time', va='bottom', fontsize=15)
            ax.set_xlabel('Direction (Degrees)')
            ax.set_ylabel('Wind Speed (m/s)', labelpad=20)
            plt.legend(['Wind Speed (m/s)'], loc="upper right", frameon=False)

            # Annotate each bar with the date for clarity
            for i, bar in enumerate(bars):
                rotation = np.rad2deg(wind_directions[i])
                alignment = 'left' if 0 <= rotation <= 180 else 'right'
                ax.text(wind_directions[i], wind_speeds[i] + 0.5, dates[i], color='red', ha=alignment, va='bottom')

            plt.show()

        # User input for city and number of days
        city = input("Enter the city name: ")
        num_days = int(input("Enter the number of days for the forecast (up to 8): "))
        api_key = '1c4d04f2dc3ffc15fe62bd4f1c73e19b'  # Replace with your API key

        # Validate number of days
        if num_days < 1 or num_days > 8:
            print("Invalid number of days. The number must be between 1 and 8.")
        else:
            # Fetch coordinates for the city
            lat, lon = get_coordinates(city, api_key)
            if lat is not None and lon is not None:
                # Fetch and plot data
                daily_data = fetch_weather_data(lat, lon, num_days, api_key)
                plot_wind_speed_and_direction(daily_data)

    elif choice == 5 :

        import requests
        import seaborn as sns
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
        from datetime import datetime, timedelta

        def get_coordinates(city, api_key):
            """Get latitude and longitude for a given city using OpenWeatherMap's Geocoding API."""
            geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
            response = requests.get(geocode_url)
            data = response.json()
            if data:
                return data[0]['lat'], data[0]['lon']
            else:
                print("City not found. Please check the city name.")
                return None, None

        def fetch_weather_data(lat, lon, api_key):
            """Fetches hourly weather data using the OpenWeatherMap One Call API."""
            url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,daily,current,alerts&appid={api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            return data['hourly']

        def prepare_data_for_heatmap(hourly_data, param='humidity'):
            """Extracts and prepares data for heatmap generation."""
            # Extract relevant data
            times = [datetime.fromtimestamp(h['dt']) for h in hourly_data]
            values = [h[param] for h in hourly_data]

            # Create DataFrame
            df = pd.DataFrame({
                'Time': times,
                'Hour': [t.hour for t in times],
                'Day': [t.day for t in times],
                param: values
            })
            
            # Pivot for heatmap
            heatmap_data = df.pivot(index="Hour", columns="Day", values=param)
            return heatmap_data

            
            # Pivot for heatmap
            heatmap_data = df.pivot("Hour", "Day", param)
            return heatmap_data

        def plot_heatmap(data, title):
            """Plots a heatmap of the given data."""
            plt.figure(figsize=(12, 8))
            sns.heatmap(data, annot=True, fmt=".0f", linewidths=.5, cmap='coolwarm')
            plt.title(title)
            plt.ylabel('Hour of Day')
            plt.xlabel('Day of Month')
            plt.show()

        # User inputs
        city = input("Enter the city name: ")
        api_key = '1c4d04f2dc3ffc15fe62bd4f1c73e19b'  # Replace with your actual OpenWeatherMap API key
        parameter = input("Enter the parameter to visualize (e.g., humidity, uvi): ")

        # Fetch coordinates for the city
        lat, lon = get_coordinates(city, api_key)
        if lat is not None and lon is not None:
            # Fetch weather data
            hourly_data = fetch_weather_data(lat, lon, api_key)
            # Prepare data for the heatmap
            heatmap_data = prepare_data_for_heatmap(hourly_data, parameter)
            # Plot the heatmap
            plot_heatmap(heatmap_data, f"Heatmap of {parameter.capitalize()} for {city}")
        else:
            print("Failed to retrieve weather data.")

    elif choice == 6 :

        import requests
        import plotly.graph_objects as go
        from datetime import datetime, timedelta

        def get_coordinates(city, api_key):
            """Get latitude and longitude for a given city using OpenWeatherMap's Geocoding API."""
            url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
            response = requests.get(url)
            data = response.json()
            if data:
                return data[0]['lat'], data[0]['lon']
            else:
                print("City not found. Please check the city name.")
                return None, None

        def fetch_weather_alerts(lat, lon, api_key):
            """Fetches weather alerts for a specific location."""
            url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,daily&appid={api_key}"
            response = requests.get(url)
            data = response.json()
            return data.get('alerts', [])

        def plot_alerts_on_timeline(alerts):
            """Creates an interactive timeline of weather alerts using Plotly."""
            if not alerts:
                print("No alerts to display.")
                return

            fig = go.Figure()

            for alert in alerts:
                start_time = datetime.fromtimestamp(alert['start'])
                end_time = datetime.fromtimestamp(alert['end'])
                duration = end_time - start_time
                duration_str = str(duration)[:-3]  # Convert duration to string and remove seconds
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

        # Main execution
        city = input("Enter the city name: ")
        api_key = '1c4d04f2dc3ffc15fe62bd4f1c73e19b' 
        lat, lon = get_coordinates(city, api_key)
        if lat and lon:
            alerts = fetch_weather_alerts(lat, lon, api_key)
            plot_alerts_on_timeline(alerts)
        else:
            print("Failed to retrieve coordinates or weather alerts.")

    elif choice == 7 :

        import requests
        import pandas as pd
        from meteostat import Point, Daily
        import matplotlib.pyplot as plt
        from datetime import datetime

        def get_coordinates(city_name, api_key):
            """Get latitude and longitude for the given city using OpenWeatherMap's Geocoding API."""
            url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
            response = requests.get(url)
            data = response.json()
            if data:
                lat = data[0]['lat']
                lon = data[0]['lon']
                return lat, lon
            else:
                print("City not found. Please check the city name.")
                return None, None

        def fetch_historical_data(lat, lon, start_date, end_date):
            """Fetch historical weather data for a given location and time range."""
            location = Point(lat, lon)
            data = Daily(location, start=start_date, end=end_date)
            data = data.fetch()
            return data

        def visualize_temperature_trends(data):
            """Visualize temperature trends."""
            plt.figure(figsize=(10, 5))
            plt.plot(data.index, data['tavg'], label='Average Daily Temperature', color='tomato')
            plt.title('Daily Temperature Trends')
            plt.xlabel('Date')
            plt.ylabel('Temperature (°C)')
            plt.grid(True)
            plt.legend()
            plt.show()

        def main():
            # User inputs
            api_key = '1c4d04f2dc3ffc15fe62bd4f1c73e19b' # Replace with your OpenWeatherMap API key
            city_name = input("Enter the city name: ")
            start_year = int(input("Enter the start year (YYYY): "))
            end_year = int(input("Enter the end year (YYYY): "))
            
            # Get coordinates
            lat, lon = get_coordinates(city_name, api_key)
            if lat is not None and lon is not None:
                start = datetime(start_year, 1, 1)
                end = datetime(end_year, 12, 31)
                
                # Fetch data
                try:
                    historical_data = fetch_historical_data(lat, lon, start, end)
                    if not historical_data.empty:
                        visualize_temperature_trends(historical_data)
                    else:
                        print("No data available for this location and time period.")
                except Exception as e:
                    print("An error occurred while fetching the data:", e)
            else:
                print("Error retrieving location data.")

        if __name__ == "__main__":
            main()

    elif choice == 8 :

        import requests
        import matplotlib.pyplot as plt
        from meteostat import Point, Daily
        from datetime import datetime
        import pandas as pd

        def get_coordinates(city_name, api_key):
            """Fetch latitude and longitude for the given city using OpenWeatherMap's Geocoding API."""
            url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
            response = requests.get(url)
            data = response.json()
            if data:
                lat = data[0]['lat']
                lon = data[0]['lon']
                return lat, lon
            else:
                print("City not found. Please check the city name.")
                return None, None

        def fetch_precipitation_data(lat, lon, start_date, end_date):
            """Fetch daily precipitation data from Meteostat."""
            location = Point(lat, lon)
            data = Daily(location, start=start_date, end=end_date)
            data = data.fetch()
            return data['prcp']

        def plot_daily_precipitation(data, city_name, year):
            """Plot daily precipitation."""
            plt.figure(figsize=(10, 5))
            data.plot()
            plt.title(f'Daily Precipitation in {city_name} for {year}')
            plt.xlabel('Date')
            plt.ylabel('Precipitation (mm)')
            plt.grid(True)
            plt.show()

        def plot_cumulative_precipitation(data, city_name, year):
            """Plot cumulative precipitation."""
            cumulative_prcp = data.cumsum()
            plt.figure(figsize=(10, 5))
            cumulative_prcp.plot()
            plt.title(f'Cumulative Precipitation in {city_name} for {year}')
            plt.xlabel('Date')
            plt.ylabel('Cumulative Precipitation (mm)')
            plt.grid(True)
            plt.show()

        def main():
            city_name = input("Enter the city name: ")
            api_key = '1c4d04f2dc3ffc15fe62bd4f1c73e19b'
            year = int(input("Enter the year for the precipitation data: "))

            # Get coordinates
            lat, lon = get_coordinates(city_name, api_key)
            if lat is not None and lon is not None:
                # Define the time period
                start_date = datetime(year, 1, 1)
                end_date = datetime(year, 12, 31)

                # Fetch precipitation data
                precipitation_data = fetch_precipitation_data(lat, lon, start_date, end_date)
                
                # Plot daily and cumulative precipitation
                plot_daily_precipitation(precipitation_data, city_name, year)
                plot_cumulative_precipitation(precipitation_data, city_name, year)
            else:
                print("Error retrieving geographic data.")

        if __name__ == "__main__":
            main()

    elif choice == 9 :

        from datetime import datetime
        from meteostat import Point, Daily
        import matplotlib.pyplot as plt
        import requests
        import pandas as pd

        def get_coordinates(city, api_key):
            """ Retrieve geographic coordinates from OpenWeatherMap API based on city name. """
            url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
            response = requests.get(url)
            data = response.json()
            if not data:
                print(f"City not found: {city}. Please check the city name.")
                return None, None
            return data[0]['lat'], data[0]['lon']

        def get_weather_data(lat, lon, start, end):
            """ Retrieve historical weather data using Meteostat. """
            # Create a point for Meteostat
            location = Point(lat, lon)
            
            # Fetch daily historical data from Meteostat
            data = Daily(location, start, end)
            data = data.fetch()
            
            return data

        # User inputs
        api_key = '1c4d04f2dc3ffc15fe62bd4f1c73e19b'  # Your API key
        cities = input("Enter city names separated by comma: ").split(',')
        start = datetime(2020, 1, 1)
        end = datetime(2020, 12, 31)

        # Plot setup
        plt.figure(figsize=(14, 7))

        # Process each city
        for city in cities:
            city = city.strip()
            lat, lon = get_coordinates(city, api_key)
            if lat is not None and lon is not None:
                data = get_weather_data(lat, lon, start, end)
                if not data.empty:
                    plt.plot(data.index, data['tavg'], label=f"Average Temp in {city} (°C)")
                    plt.plot(data.index, data['prcp'], label=f"Precipitation in {city} (mm)", linestyle='--')

        # Finalize plot
        plt.title('Climate Comparison Across Cities (2020)')
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C) / Precipitation (mm)')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        
    elif choice == 10 :

        import requests
        import pandas as pd
        import matplotlib.pyplot as plt
        from datetime import datetime
        from meteostat import Point, Daily

        def get_coordinates(city, api_key):
            """Retrieve latitude and longitude for a city using the OpenWeatherMap Geocoding API."""
            geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
            response = requests.get(geocode_url)
            data = response.json()
            if not data:
                print(f"City not found: {city}. Please check the city name.")
                return None, None
            return data[0]['lat'], data[0]['lon']

        def fetch_weather_data(lat, lon, start, end):
            """Retrieve weather data using Meteostat."""
            location = Point(lat, lon)
            data = Daily(location, start, end)
            data = data.fetch()
            return data

        def plot_temperature_precipitation(data):
            """Plot daily average, min, and max temperatures and precipitation."""
            fig, ax1 = plt.subplots(figsize=(14, 6))
            
            # Plot temperature data
            data['tavg'].plot(ax=ax1, color='tab:red', label='Avg Temp (°C)')
            data['tmin'].plot(ax=ax1, color='tab:blue', label='Min Temp (°C)', linestyle='--')
            data['tmax'].plot(ax=ax1, color='tab:green', label='Max Temp (°C)', linestyle='--')
            ax1.set_ylabel('Temperature (°C)')
            ax1.legend(loc='upper left')
            ax1.set_title('Daily Temperature and Precipitation')

            # Plot precipitation on the same chart with a secondary y-axis
            ax2 = ax1.twinx()
            data['prcp'].plot(ax=ax2, color='tab:blue', label='Precipitation (mm)', linestyle=':')
            ax2.set_ylabel('Precipitation (mm)')
            ax2.legend(loc='upper right')

            plt.show()

        # Main
        api_key = '1c4d04f2dc3ffc15fe62bd4f1c73e19b'  # Replace with your actual API key
        city = input("Enter the city name: ")
        start_date = input("Enter the start date (YYYY-MM-DD): ")
        end_date = input("Enter the end date (YYYY-MM-DD): ")

        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')

        lat, lon = get_coordinates(city, api_key)
        if lat is not None and lon is not None:
            data = fetch_weather_data(lat, lon, start, end)
            if not data.empty:
                plot_temperature_precipitation(data)
            else:
                print("No data available for the specified location and time.")
        else:
            print("Error retrieving location data.")

    elif choice == 11:

        import requests
        import pandas as pd
        import matplotlib.pyplot as plt
        from datetime import datetime
        from meteostat import Point, Daily

        def get_coordinates(city, api_key):
            """Retrieve latitude and longitude for a city using the OpenWeatherMap Geocoding API."""
            geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
            response = requests.get(geocode_url)
            data = response.json()
            if not data:
                print(f"City not found: {city}. Please check the city name.")
                return None, None
            return data[0]['lat'], data[0]['lon']

        def fetch_weather_data(lat, lon, start, end):
            """Retrieve historical weather data using Meteostat."""
            location = Point(lat, lon)
            data = Daily(location, start, end)
            data = data.fetch()
            return data

        def analyze_extreme_weather(data):
            """Analyze and plot extreme weather conditions."""
            if 'prcp' in data.columns and 'tmax' in data.columns:
                # Define thresholds for 'extreme' conditions
                high_temp_threshold = data['tmax'].quantile(0.90)  # 90th percentile as extreme heat
                heavy_rain_threshold = data['prcp'].quantile(0.90)  # 90th percentile as heavy rain
                
                # Filter data for extreme weather events
                extreme_heat = data[data['tmax'] >= high_temp_threshold]
                heavy_rain = data[data['prcp'] >= heavy_rain_threshold]

                # Plotting
                plt.figure(figsize=(12, 6))
                plt.scatter(extreme_heat.index, extreme_heat['tmax'], color='red', label='Extreme Heat')
                plt.scatter(heavy_rain.index, heavy_rain['prcp'], color='blue', label='Heavy Rainfall')
                plt.legend()
                plt.title('Extreme Weather Events Analysis')
                plt.xlabel('Date')
                plt.ylabel('Temperature (°C) / Precipitation (mm)')
                plt.show()
                
                # Correlation plot (optional, if needed)
                if 'pres' in data.columns and 'rhum' in data.columns:
                    fig, ax1 = plt.subplots()
                    color = 'tab:red'
                    ax1.set_xlabel('Date')
                    ax1.set_ylabel('Pressure (hPa)', color=color)
                    ax1.plot(data.index, data['pres'], color=color)
                    ax1.tick_params(axis='y', labelcolor=color)

                    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
                    color = 'tab:blue'
                    ax2.set_ylabel('Relative Humidity (%)', color=color)
                    ax2.plot(data.index, data['rhum'], color=color)
                    ax2.tick_params(axis='y', labelcolor=color)

                    plt.title('Environmental Factors Correlation with Extreme Events')
                    plt.show()

            else:
                print("Required data columns for extreme events analysis are missing.")

        # Main
        api_key = '1c4d04f2dc3ffc15fe62bd4f1c73e19b'   # Replace with your actual API key
        city = input("Enter the city name: ")
        start_date = input("Enter the start date (YYYY-MM-DD): ")
        end_date = input("Enter the end date (YYYY-MM-DD): ")

        lat, lon = get_coordinates(city, api_key)
        if lat is not None and lon is not None:
            data = fetch_weather_data(lat, lon, datetime.strptime(start_date, '%Y-%m-%d'), datetime.strptime(end_date, '%Y-%m-%d'))
            if not data.empty:
                analyze_extreme_weather(data)
            else:
                print("No data available for the specified location and time.")
        else:
            print("Error retrieving location data.")
            
    elif choice == 12 :

        import glob
        import matplotlib.pyplot as plt
        import urllib.request
        import xarray as xr

        for yr in range(2011,2015): # note that in python, the end range is not inclusive. So, in this case data for 2015 is not downloaded.
            url = f'https://downloads.psl.noaa.gov/Datasets/cpc_us_precip/RT/precip.V1.0.{yr}.nc'
            savename = url.split('/')[-1]
            urllib.request.urlretrieve(url,savename)

        ds2011 = xr.open_dataset('precip.V1.0.2011.nc')
        ds2012 = xr.open_dataset('precip.V1.0.2012.nc')

        ds2011_2012 = xr.concat([ds2011,ds2012], dim='time')

        ds2011_2014 = xr.open_mfdataset('precip.V1.0.*.nc', concat_dim='time', combine='nested')
        # Or, you can use the following command to do the same thing:
        # ds2011_2014 = xr.open_mfdataset('precip*.nc', combine='by_coords')

        # The great thing about groupby is that you do not need to worry about the leap years or 
        # number of days in each month.
        # In addition, xarray is label-aware and when you pass the plot function, it understands that you want to
        # make a spatial plot and finds the lat and lon values and the appropriate title and labels.
        ds2012_mon = ds2012.groupby('time.month').sum()
        ds2012_mon.precip[0,:,:].plot(cmap='jet', vmax=300)

        import calendar # We'll use this library to easily add month name to subplot titles.

        # First, We will develop a land mask data array that we can use to mask out the nan values:
        landmask = ds2012.precip.sum(dim='time')>0

        fig = plt.figure(figsize=[12,8], facecolor='w')
        plt.subplots_adjust(bottom=0.15, top=0.96, left=0.04, right=0.99, 
                            wspace=0.2, hspace=0.27) # wspace and hspace adjust the horizontal and vertical spaces, respectively.
        nrows = 3
        ncols = 4
        for i in range(1, 13):
            plt.subplot(nrows, ncols, i)
            dataplot = ds2012_mon.precip[i-1, :, :].where(landmask) # Remember that in Python, the data index starts at 0, but the subplot index start at 1.
            p = plt.pcolormesh(ds2012_mon.lon, ds2012_mon.lat, dataplot,
                        vmax = 400, vmin = 0, cmap = 'nipy_spectral_r',
                        ) 
            plt.xlim([233,295])
            plt.ylim([25,50])
            plt.title(calendar.month_name[dataplot.month.values], fontsize = 13, 
                    fontweight = 'bold', color = 'b')
            plt.xticks(fontsize = 11)
            plt.yticks(fontsize = 11)
            if i % ncols == 1: # Add ylabel for the very left subplots
                plt.ylabel('Latitude', fontsize = 11, fontweight = 'bold')
            if i > ncols*(nrows-1): # Add xlabel for the bottom row subplots
                plt.xlabel('Longitude', fontsize = 11, fontweight = 'bold')

        # Add a colorbar at the bottom:
        cax = fig.add_axes([0.25, 0.06, 0.5, 0.018])
        cb = plt.colorbar(cax=cax, orientation='horizontal', extend = 'max',)
        cb.ax.tick_params(labelsize=11)
        cb.set_label(label='Precipitation (mm)', color = 'k', size=14)

        # Now we can save a high resolution (300dpi) version of the figure:
        plt.savefig('Fig_prec_cpc_mon_2012.png', format = 'png', dpi = 300)

    elif choice == 13 :

        import numpy
        import scipy.stats
        import pandas
        import matplotlib.pyplot as plt

        # Download and import weather data
        data = pandas.read_csv("https://risk-engineering.org/static/data/TLS-weather-data-2013.csv")

        # Data consistency checks
        assert(0 < len(data) <= 365)
        for index, day in data.iterrows():
            assert(day["Max TemperatureC"] >= day["Mean TemperatureC"] >= day["Min TemperatureC"])
            assert(day["Max Wind SpeedKm/h"] >= day["Mean Wind SpeedKm/h"] >= 0)
            assert(360 >= day["WindDirDegrees"] >= 0)

        # Functions
        def FahrenheitToCelsius(F): 
            return (F - 32) * 5 / 9.0

        # Analysis
        print("Lowest temperature measured in 2013:", data["Min TemperatureC"].min())

        plt.plot(data["Mean TemperatureC"])
        plt.ylabel("Mean daily temperature (°C)")
        plt.show()

        plt.scatter(data["Max TemperatureC"], data["Mean Sea Level PressurehPa"])
        plt.show()

        plt.scatter(data["Mean TemperatureC"], data["Mean Sea Level PressurehPa"])
        plt.show()

        plt.scatter(data["Mean VisibilityKm"], data["Mean Sea Level PressurehPa"])
        plt.show()

        data.plot(x="Mean VisibilityKm", y="Mean Wind SpeedKm/h", kind="scatter")
        plt.show()

        data.plot(x="Mean Sea Level PressurehPa", y="Precipitationmm", kind="scatter")
        plt.show()

        data.plot(x="Mean TemperatureC", y="Dew PointC", kind="scatter")
        plt.show()

        # Probability distribution fitting
        obs = scipy.stats.norm(loc=10, scale=2).rvs(1000)
        print("Fitted normal distribution parameters:", scipy.stats.norm.fit(obs))

        wind = data["Mean Wind SpeedKm/h"]
        shape, loc, scale = scipy.stats.lognorm.fit(wind, floc=0)
        print("Fitted lognormal distribution parameters:", shape, loc, scale)

        mu, sigma = scipy.stats.norm.fit(wind)
        print("Kolmogorov-Smirnov test for normal distribution fit:", scipy.stats.kstest(wind, "norm"))

        fitted = scipy.stats.lognorm(shape, loc, scale)
        print("Kolmogorov-Smirnov test for lognormal distribution fit:", scipy.stats.kstest(wind, "lognorm", (shape, loc, scale)))

        p0, p1, p2 = scipy.stats.weibull_min.fit(wind, floc=0)
        print("Kolmogorov-Smirnov test for Weibull distribution fit:", scipy.stats.kstest(wind, "weibull_min", args=(p0, p1, p2)))
        

    elif choice == 14 :

        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        import numpy as np
        from datetime import datetime, timedelta

        # Read .txt file
        file_directory = "C:/Users/rhyss/Documents/Python/"  # Base file directory location
        file_name = 'kestrel_20170821_eclipse.txt'

        try:
            times, wind_speed, temperature, dew_point, pressure, altitude = np.loadtxt(
            file_directory + file_name, skiprows=4, comments='#', delimiter=',', usecols=range(6), unpack=True)


            # Convert integer time values from seconds to datetime
            origin = datetime(2000, 1, 1, 0, 0)  # Time is recorded in seconds elapsed since this date
            datetime_values = [origin + timedelta(seconds=time_sec) for time_sec in times]

            # Create figure and plot variables
            fig, ax = plt.subplots(figsize=(12, 7))

            # Plotting data
            ax.plot(datetime_values, temperature, '-', label='Temperature', color='r')
            ax.plot(datetime_values, dew_point, '-', label='Dewpoint', color='g')
            ax2 = ax.twinx()
            ax2.plot(datetime_values, pressure, '-', label='Station Pressure', color='b')

            # Plot eclipse intervals
            ax.axvspan(datetime(2017, 8, 21, 13, 4, 32), datetime(2017, 8, 21, 15, 58, 59), color='k', alpha=0.1)  # Partial eclipse
            ax.axvspan(datetime(2017, 8, 21, 14, 33, 10), datetime(2017, 8, 21, 14, 35, 40), color='k', alpha=0.4)  # Total eclipse

            # Format labels for legend
            labels = ['Temperature', 'Dewpoint', 'Station Pressure', 'Partial Eclipse', 'Total Eclipse']

            # Set nice date formatting for x-axis
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

            # Set remaining plot info
            ax.set_title('Meteorogram for Eclipse Day (21 August 2017)')
            ax.set_ylabel(r'Temperature / Dewpoint ($^\circ$F)')
            ax2.set_ylabel('Station Pressure (hPa)')
            ax.set_xlabel('Time (EDT)')
            ax.legend(labels, loc='upper left')

            # Save plot
            plt.savefig(file_directory + 'eclipse_meteorogram.png', bbox_inches='tight')

            plt.show()

        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found in directory '{file_directory}'.")



    else:
        print("Invalid choice. Please enter a number between 1 and 14.")

if __name__ == "__main__":
    user_choice = main_menu()
    run_selected_option(user_choice)
