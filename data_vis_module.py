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


import matplotlib.pyplot as plt

def plot_temperature(data):
    temperatures = [datapoint['main']['temp'] for datapoint in data]
    timestamps = [datapoint['dt_txt'] for datapoint in data]
    
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, temperatures, marker='o', linestyle='-', color='blue')
    plt.title('Temperature Over Time')
    plt.xlabel('Time')
    plt.ylabel('Temperature (K)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()