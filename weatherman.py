import argparse
import calendar
from datetime import datetime
import os


RED = "\033[31m"
BLUE = "\033[34m"
RESET = "\033[0m"


class WeatherReading:

    def __init__(self, observation_date, max_temp, min_temp, max_humidity, mean_humidity):
        self.date = observation_date
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity

    def __repr__(self):
        return (f"WeatherReading(date={self.date}, max_temp={self.max_temp}, min_temp={self.min_temp}, "
                f"max_humidity={self.max_humidity}, mean_humidity={self.mean_humidity})")

    
def parse_weather_file(file_path):
    readings = []
    try:
        with open(file_path, 'r') as file:
            header = next(file).strip().split(',')
            required_fields = ["PKT", "Max TemperatureC", "Min TemperatureC", "Max Humidity", " Mean Humidity"]
            field_indices = {field: header.index(field) for field in required_fields}
            
            for line in file:
                parts = line.strip().split(',')
                try:
                    selected_fields = {field: parts[field_indices[field]] for field in required_fields}
                except IndexError:
                    continue
                
                if '' in selected_fields.values():
                    continue

                obs_date = selected_fields["PKT"]
                max_temp = float(selected_fields["Max TemperatureC"])
                min_temp = float(selected_fields["Min TemperatureC"])
                max_humidity = float(selected_fields["Max Humidity"])
                mean_humidity = float(selected_fields[" Mean Humidity"])
                reading = WeatherReading(obs_date, max_temp, min_temp, max_humidity, mean_humidity)
                readings.append(reading)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return readings


class WeatherCalculations:

    def __init__(self):
        self.highest_temp = None
        self.lowest_temp = None
        self.highest_humidity = None
        self.total_max_temp = 0
        self.total_min_temp = 0
        self.total_mean_humidity = 0
        self.num_readings = 0

    def update(self, reading):
        if self.num_readings == 0:
            self.highest_temp = self.lowest_temp = self.highest_humidity = reading
        else:
            if reading.max_temp > self.highest_temp.max_temp:
                self.highest_temp = reading
            if reading.min_temp < self.lowest_temp.min_temp:
                self.lowest_temp = reading
            if reading.max_humidity > self.highest_humidity.max_humidity:
                self.highest_humidity = reading

        self.total_max_temp += reading.max_temp
        self.total_min_temp += reading.min_temp
        self.total_mean_humidity += reading.mean_humidity
        self.num_readings += 1

    def compute_averages(self):
        if self.num_readings == 0:
            return None, None, None
        avg_max_temp = self.total_max_temp / self.num_readings
        avg_min_temp = self.total_min_temp / self.num_readings
        avg_mean_humidity = self.total_mean_humidity / self.num_readings
        return avg_max_temp, avg_min_temp, avg_mean_humidity
    

def read_yearly_data(directory, year):
    calculations = WeatherCalculations()
    for month in calendar.month_abbr:
        if month == "":
            continue
        file_path = os.path.join(directory, f"Murree_weather_{year}_{month}.txt")
        readings = parse_weather_file(file_path)
        for reading in readings:
            calculations.update(reading)
    return calculations


def generate_yearly_report(calculations):
    if calculations.highest_temp and calculations.lowest_temp and calculations.highest_humidity:
        print(f"Highest: {calculations.highest_temp.max_temp}C on {calculations.highest_temp.date}")
        print(f"Lowest: {calculations.lowest_temp.min_temp}C on {calculations.lowest_temp.date}")
        print(f"Humidity: {calculations.highest_humidity.max_humidity}% on {calculations.highest_humidity.date}")


def read_monthly_data(directory, year, month):
    calculations = WeatherCalculations()
    month_name = datetime(year, month, 1).strftime('%b')
    file_path = os.path.join(directory, f"Murree_weather_{year}_{month_name}.txt")
    readings = parse_weather_file(file_path)
    for reading in readings:
        calculations.update(reading)
    return calculations


def generate_monthly_report(calculations):
    avg_max_temp, avg_min_temp, avg_mean_humidity = calculations.compute_averages()
    print(f"Highest Average Temperature: {avg_max_temp:.0f}C")
    print(f"Lowest Average Temperature: {avg_min_temp:.0f}C")
    print(f"Average Mean Humidity: {avg_mean_humidity:.0f}%")


def read_monthly_column_data(directory, year, month):
    month_name = datetime(year, month, 1).strftime("%b")
    file_path = os.path.join(directory, f"Murree_weather_{year}_{month_name}.txt")
    readings = parse_weather_file(file_path)
    return readings


def generate_monthly_bar_chart(readings, combined):
    if readings:
        month_name = datetime.strptime(readings[0].date, "%Y-%m-%d").strftime("%B %Y")
        print(f"{month_name}")
        for reading in readings:
            day = datetime.strptime(reading.date, "%Y-%m-%d").day
            high_bar = f"{RED}{'+' * round(reading.max_temp)}{RESET}"
            low_bar = f"{BLUE}{'+' * round(reading.min_temp)}{RESET}"

            if combined:
                print(f"{day:02d} {low_bar} {high_bar} {reading.min_temp}C - {reading.max_temp}C")
            else:
                print(f"{day} {high_bar} {reading.max_temp}C")
                print(f"{day} {low_bar} {reading.min_temp}C")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=str)
    parser.add_argument("-e", type=int)
    parser.add_argument("-a", type=str)
    parser.add_argument("-c", type=str)

    args = parser.parse_args()

    if args.e:
        year = args.e
        print(f"Reading all files for the year {year}:")
        yearly_calculations = read_yearly_data(args.directory, year)
        generate_yearly_report(yearly_calculations)

    if args.a:
        year, month = map(int, args.a.split('/'))
        print(f"Reading data for {year}/{month}:")
        monthly_calculations = read_monthly_data(args.directory, year, month)
        generate_monthly_report(monthly_calculations)

    if args.c:
        year, month = map(int, args.c.split('/'))
        print(f"Reading columnar data for {year}/{month}:")
        monthly_readings = read_monthly_column_data(args.directory, year, month)
        generate_monthly_bar_chart(monthly_readings, combined=False)

if __name__ == "__main__":
    main()