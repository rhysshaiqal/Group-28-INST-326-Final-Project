Function main_menu()
This function displays a list of visualization and analysis options to the user and retrieves their choice. It ensures that the user's input is directed towards the appropriate function for the selected operation.

Function run_selected_option(choice)
This function determines the action based on the user's choice. It uses conditional statements (if-elif) to match the user's choice with the corresponding data retrieval and visualization logic. Here's a detailed breakdown of what each choice does:

Current Weather and Map: Fetches current weather data using OpenWeatherMap API for a specified city and displays it alongside a weather icon. It also generates an interactive map showing the location with weather details using the Folium library.

Daily Temperature Trends: Retrieves historical temperature data for a specified number of past days using OpenWeatherMap's historical weather API, converts temperatures from Kelvin to Fahrenheit, and plots the temperature trends over the specified days.

Forecast Precipitation and Events: Displays forecast data including precipitation probabilities and significant weather events (like rain or snow) using a dual-axis plot to differentiate between precipitation and other weather events over a given number of days.

Wind Speed and Direction: Plots wind speed and direction data on a polar chart, providing visual insights into wind patterns over a specified forecast period.

Heatmap of Weather Parameter: Creates a heatmap for specified weather parameters (like humidity or UV index) using hourly forecast data, which helps in understanding the variations throughout the days.

Weather Alerts Timeline: Displays weather alerts in an interactive timeline format using Plotly, making it easier to visualize the duration and details of various alerts.

Historical Temperature Data: Fetches and visualizes historical temperature data over a range of years using the Meteostat library, which is useful for long-term climate study.

Precipitation Data Analysis: Analyzes precipitation data over a specified year and provides both daily and cumulative precipitation plots.

Climate Comparison Across Cities: Compares climate data like average temperature and precipitation across multiple cities for a specified year, helping in comparative climate studies.

Temperature and Precipitation Overview: Fetches and plots temperature and precipitation data for a specified period using Meteostat to provide a comprehensive overview of weather patterns.

Extreme Weather Analysis: Analyzes and visualizes extreme weather conditions based on historical data, identifying days with extreme temperatures or precipitation.

Monthly Precipitation Overview: Uses NOAA's precipitation datasets to display monthly precipitation over several years, providing insights into seasonal patterns.

Statistical Analysis of Weather Data: Performs statistical analysis on weather data, fitting various distributions to the data and testing these fits, useful for statistical modeling of weather phenomena.

Weather Conditions During Solar Eclipse: Analyzes and visualizes meteorological conditions during a solar eclipse, showing changes in temperature, dew point, and pressure throughout the event.
