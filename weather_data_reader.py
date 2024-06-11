import calendar
import os

from parse_weather_data import WeatherParser
from weather_calculation import WeatherCalculations


class WeatherDataReader:

    def __init__(self, directory):
        self.directory = directory
        self.parser = WeatherParser()
        self.weather_stats = WeatherCalculations()
        self.file_path = os.path.join(self.directory, "Murree_weather_{year}_{month}.txt")

    def _read_data(self, file_path):
        weather_readings = self.parser.parse_weather_file(file_path)
        for reading in weather_readings:
            self.weather_stats.update_calculations(reading)
    
    def read_monthly_readings(self, year, month):
        self._read_data(self.file_path.format(year=year,month=calendar.month_abbr[month]))
        return self.weather_stats

    def read_monthly_column_readings(self, year, month):
        return self.parser.parse_weather_file(self.file_path.format(year=year,month=calendar.month_abbr[month]))
    
    def read_yearly_data(self, year):
        for month in calendar.month_abbr:
            if month == "":
                continue
            self._read_data(self.file_path.format(year=year,month=month))
        return self.weather_stats
