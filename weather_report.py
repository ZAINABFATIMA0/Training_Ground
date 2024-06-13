from datetime import datetime
from enum import Enum


class Color(Enum):
    RED = "\033[31m"
    BLUE = "\033[34m"
    RESET = "\033[0m"


class WeatherReport:
    """
    A class to generate weather reports and visualizations.
    """

    def generate_yearly_report(self, weather_stats):
        """
        Generate a yearly weather report based on provided statistics.

        Args:
            weather_stats (WeatherCalculations): Instance of WeatherCalculations containing yearly weather statistics.
        """
        if (weather_stats.highest_temperature_record and weather_stats.lowest_temperature_record 
            and weather_stats.highest_humidity_record):
            
            print(f"Highest: {weather_stats.highest_temperature_record.max_temperature}C on "
                  f"{weather_stats.highest_temperature_record.observation_date}")
            print(f"Lowest: {weather_stats.lowest_temperature_record.min_temperature}C on "
                  f"{weather_stats.lowest_temperature_record.observation_date}")
            print(f"Humidity: {weather_stats.highest_humidity_record.max_humidity}% on "
                  f"{weather_stats.highest_humidity_record.observation_date}" + "\n")
        else:
            print("No data available for the specified year.")

    def generate_monthly_report(self, weather_stats):
        """
        Generate a monthly weather report based on provided statistics.

        Args:
            weather_stats (WeatherCalculations): Instance of WeatherCalculations containing monthly weather statistics.
        """
        if not weather_stats:
            return
        
        avg_max_temperature, avg_min_temperature, avg_mean_humidity = weather_stats.compute_averages()

        if avg_max_temperature is None:
            print("No data available for the specified month.")
        else:
            print(f"Highest Average Temperature: {avg_max_temperature:.2f}C")
            print(f"Lowest Average Temperature: {avg_min_temperature:.2f}C")
            print(f"Average Mean Humidity: {avg_mean_humidity:.2f}%" + "\n")
            
    def generate_monthly_bar_chart(self, monthly_temperature_readings, combined_bar_charts):
        """
        Generate a monthly bar chart based on daily temperature readings.

        Args:
            monthly_temperature_readings (list): List of WeatherReading objects representing daily temperature readings.
            combined_bar_charts (bool): Flag indicating whether to combine high and low temperature bars.

        """
        if not monthly_temperature_readings:
            return
        
        for single_day_reading in monthly_temperature_readings:
            day = datetime.strptime(single_day_reading.observation_date, "%Y-%m-%d").day

            high_temperature_bar = (
                f"{Color.RED.value}{'+' * round(single_day_reading.max_temperature)}"
                f"{Color.RESET.value}"
            )
            low_temperature_bar = (
                f"{Color.BLUE.value}{'+' * round(single_day_reading.min_temperature)}"
                f"{Color.RESET.value}"
            )
            if combined_bar_charts:
                print(f"{day:02d} {low_temperature_bar} {high_temperature_bar} "
                      f"{single_day_reading.min_temperature}C - {single_day_reading.max_temperature}C")
            else:
                print(f"{day} {high_temperature_bar} {single_day_reading.max_temperature}C")
                print(f"{day} {low_temperature_bar} {single_day_reading.min_temperature}C")
