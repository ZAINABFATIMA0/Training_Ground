import calendar
import os

from parse_weather_data import WeatherParser
from weather_calculation import WeatherCalculations


class WeatherDataReader:
    
    def __init__(self, directory):
        self.directory = directory
        self.parser = WeatherParser()
        self.weather_stats = WeatherCalculations()

    def _get_monthly_file_path(self, year, month):
        if isinstance(month, str):
            month = list(calendar.month_abbr).index(month.capitalize())
        return os.path.join(self.directory, f"Murree_weather_{year}_{calendar.month_abbr[month]}.txt")

    def _read_data(self, file_path):
        weather_readings = self.parser.parse_weather_file(file_path)
        for reading in weather_readings:
            self.weather_stats.update_calculations(reading)
    
    def read_monthly_data(self, year, month):
        file_path = self._get_monthly_file_path(year, month)
        self._read_data(file_path)
        return self.weather_stats

    def read_monthly_column_data(self, year, month):
        file_path = self._get_monthly_file_path(year, month)
        return self.parser.parse_weather_file(file_path)
    
    def read_yearly_data(self, year):
        for month in calendar.month_abbr:
            if month == "":
                continue
            file_path = self._get_monthly_file_path(year, month)
            self._read_data(file_path)
        return self.weather_stats



