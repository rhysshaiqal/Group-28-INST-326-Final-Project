import plotly.graph_objects as go
import argparse

# Sample weather data
data = [
    {"dt_txt": "2024-04-01 00:00:00", "main": {"temp": 288.15}},
    {"dt_txt": "2024-04-01 03:00:00", "main": {"temp": 287.10}},
    {"dt_txt": "2024-04-01 06:00:00", "main": {"temp": 285.17}},
    {"dt_txt": "2024-04-01 09:00:00", "main": {"temp": 284.15}},
    {"dt_txt": "2024-04-01 12:00:00", "main": {"temp": 286.15}},
    {"dt_txt": "2024-04-01 15:00:00", "main": {"temp": 289.15}},
    {"dt_txt": "2024-04-01 18:00:00", "main": {"temp": 290.15}},
    {"dt_txt": "2024-04-01 21:00:00", "main": {"temp": 289.10}}
]

# Function to plot temperature using Plotly
def plot_temperature(data):
    temperatures = [datapoint['main']['temp'] for datapoint in data]
    timestamps = [datapoint['dt_txt'] for datapoint in data]
    
    # Create the plot
    fig = go.Figure(data=go.Scatter(x=timestamps, y=temperatures, mode='lines+markers', name='Temperature'))
    fig.update_layout(title='Temperature Over Time',
                      xaxis_title='Time',
                      yaxis_title='Temperature (Kelvin)',
                      template='plotly_dark')
    fig.show()

# Define the function to parse command-line arguments (optional in this context)
def parse_arguments():
    parser = argparse.ArgumentParser(description='Plot Sample Weather Data')
    args = parser.parse_args()
    return args

# Main function to control the workflow
def main():
    args = parse_arguments()
    plot_temperature(data)

# Check if the script is run as the main program
if __name__ == "__main__":
    main()
