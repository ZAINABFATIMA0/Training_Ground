import os
import argparse
from datetime import datetime


RED = "\033[31m"
BLUE = "\033[34m"
RESET = "\033[0m"


class WeatherReading:
    def __init__(self, date, max_temp, min_temp, max_humidity, mean_humidity):
        self.date = date
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity

    def __repr__(self):
        return (f"WeatherReading(date={self.date}, max_temp={self.max_temp}, "
                f"min_temp={self.min_temp}, max_humidity={self.max_humidity}, "
                f"mean_humidity={self.mean_humidity})")


def parse_weather_file(file_path):
    readings = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()[1:]  
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) < 9 or '' in (parts[1], parts[3], parts[7], parts[8]):
                    continue  
                date = parts[0]
                max_temp = int(parts[1])
                min_temp = int(parts[3])
                max_humidity = int(parts[7])
                mean_humidity = int(parts[8])
                reading = WeatherReading(date, max_temp, min_temp, max_humidity, mean_humidity)
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
        if self.highest_temp is None or reading.max_temp > self.highest_temp.max_temp:
            self.highest_temp = reading
        if self.lowest_temp is None or reading.min_temp < self.lowest_temp.min_temp:
            self.lowest_temp = reading
        if self.highest_humidity is None or reading.max_humidity > self.highest_humidity.max_humidity:
            self.highest_humidity = reading

        self.total_max_temp += reading.max_temp
        self.total_min_temp += reading.min_temp
        self.total_mean_humidity += reading.mean_humidity
        self.num_readings += 1

    def compute_averages(self):
        avg_max_temp = self.total_max_temp / self.num_readings
        avg_min_temp = self.total_min_temp / self.num_readings
        avg_mean_humidity = self.total_mean_humidity / self.num_readings
        return avg_max_temp, avg_min_temp, avg_mean_humidity
    

#Yearly data manipulation and report

def read_yearly_data(directory, year):
    calculations = WeatherCalculations()
    for month in range(1, 13):
        month_name = datetime(year, month, 1).strftime('%b')
        file_path = os.path.join(directory, f"Murree_weather_{year}_{month_name}.txt")
        readings = parse_weather_file(file_path)
        for reading in readings:
            calculations.update(reading)
    return calculations

def generate_yearly_report(calculations):
    if calculations.highest_temp and calculations.lowest_temp and calculations.highest_humidity:
        print(f"Highest: {calculations.highest_temp.max_temp}C on {calculations.highest_temp.date}")
        print(f"Lowest: {calculations.lowest_temp.min_temp}C on {calculations.lowest_temp.date}")
        print(f"Humidity: {calculations.highest_humidity.max_humidity}% on {calculations.highest_humidity.date}")

#Monthly data reading and manipulation

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
    print(f"Highest Average: {avg_max_temp:.0f}C")
    print(f"Lowest Average: {avg_min_temp:.0f}C")
    print(f"Average Mean Humidity: {avg_mean_humidity:.0f}%")


#Monthly data for bar graphs

def read_monthly_column_data(directory, year, month):
    month_name = datetime(year, month, 1).strftime('%b')
    file_path = os.path.join(directory, f"Murree_weather_{year}_{month_name}.txt")
    readings = parse_weather_file(file_path)
    return readings

def generate_monthly_bar_chart(readings, combined):
    if readings:
        month_name = datetime.strptime(readings[0].date, '%Y-%m-%d').strftime('%B %Y')
        print(f"{month_name}")
        for reading in readings:
            day = datetime.strptime(reading.date, '%Y-%m-%d').day
            high_bar = RED + '+' * reading.max_temp + RESET
            low_bar = BLUE + '+' * reading.min_temp + RESET
            if combined:
                print(f"{day:02d} {low_bar} {high_bar} {reading.min_temp}C - {reading.max_temp}C")
            else:
                print(f"{day} {high_bar} {reading.max_temp}C")
                print(f"{day} {low_bar} {reading.min_temp}C")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=str)
    parser.add_argument('-e', type=int)
    parser.add_argument('-a', type=str)
    parser.add_argument('-c', type=str)

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