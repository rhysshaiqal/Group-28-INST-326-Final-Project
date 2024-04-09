import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Real-Time Weather Data Visualization Tool')
    parser.add_argument('--location', type=str, help='Location to fetch weather for')
    args = parser.parse_args()
    return args