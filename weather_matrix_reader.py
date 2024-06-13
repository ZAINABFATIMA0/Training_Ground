import calendar
import os

from parse_weather_data import WeatherParser
from weather_calculation import WeatherCalculations


class WeatherDataReader:
    """
    A class to read and process weather data from files.
    
    Attributes:
        directory (str): Directory path where weather data files are located.
        parser (WeatherParser): Instance of WeatherParser used to parse weather data files.
        file_path (str): Template file path for weather data files.
        weather_stats (WeatherCalculations or None): Instance of WeatherCalculations storing weather statistics.
    """

    def __init__(self, directory):
        """
        Initialize the WeatherDataReader with a directory path.

        Args:
            directory (str): Directory path containing weather data files.
        """
        self.directory = directory
        self.parser = WeatherParser()
        self.file_path = os.path.join(self.directory, "Murree_weather_{year}_{month}.txt")

    def read_weather_matrix(self, file_path):
        """
        Read and process weather data from a specific file.

        Args:
            file_path (str): Path to the weather data file to be read.
        """
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
        """
        Read and process weather data for a specific month of a year.

        Args:
            year (int): Year of the weather data to be read.
            month (int): Month (as integer) of the weather data to be read.

        Returns:
            WeatherCalculations or None: Instance of WeatherCalculations with calculated statistics for the month.
        """
        self.weather_stats = WeatherCalculations()
        self.read_weather_matrix(self.file_path.format(year=year, month=calendar.month_abbr[month]))
        return self.weather_stats
        
    def read_monthly_column_readings(self, year, month):
        """
        Read weather data for a specific month and not perform any calculations.

        Args:
            year (int): Year of the weather data to be read.
            month (int): Month (as integer) of the weather data to be read.

        Returns:
            list: List of WeatherReading objects parsed from the file.
        """
        return self.parser.parse_weather_file(self.file_path.format(year=year, month=calendar.month_abbr[month]))
    
    def read_yearly_data(self, year):
        """
        Read and process weather data for the entire year.

        Args:
            year (int): Year of the weather data to be read.

        Returns:
            WeatherCalculations or None: Instance of WeatherCalculations with calculated statistics for the year.
        """
        self.weather_stats = WeatherCalculations() 
        for month in calendar.month_abbr:
            if month == "":
                continue
            self.read_weather_matrix(self.file_path.format(year=year, month=month))
        return self.weather_stats
