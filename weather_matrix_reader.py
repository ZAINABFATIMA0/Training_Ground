import calendar
import os

from parse_weather_data import WeatherParser
from weather_calculation import WeatherCalculations


class WeatherDataReader:

    def __init__(self, directory):
        self.directory = directory
        self.parser = WeatherParser()
        self.file_path = os.path.join(self.directory, "Murree_weather_{year}_{month}.txt")

    def read_weather_matrix(self, file_path):
        try:
            if os.path.exists(file_path):
                weather_readings = self.parser.parse_weather_file(file_path)
                for reading in weather_readings:
                    self.weather_stats.update_calculations(reading)
            else:
                self.weather_stats = None
                print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
      
    def read_monthly_readings(self, year, month):
        self.weather_stats = WeatherCalculations()
        self.read_weather_matrix(self.file_path.format(year=year,month=calendar.month_abbr[month]))
        return self.weather_stats
        
    def read_monthly_column_readings(self, year, month):
        self.weather_stats = WeatherCalculations()
        return self.parser.parse_weather_file(self.file_path.format(year=year,month=calendar.month_abbr[month]))
    
    def read_yearly_data(self, year):
        self.weather_stats = WeatherCalculations() 
        for month in calendar.month_abbr:
            if month == "":
                continue
            self.read_weather_matrix(self.file_path.format(year=year,month=month))
        return self.weather_stats
