from datetime import datetime

RED = "\033[31m"
BLUE = "\033[34m"
RESET = "\033[0m"


class WeatherReport:
    
    def generate_yearly_report(self, weather_stats):
        if weather_stats.highest_temp and weather_stats.lowest_temp and weather_stats.highest_humidity:
            print(f"Highest: {weather_stats.highest_temp.max_temp}C on {weather_stats.highest_temp.observation_date}")
            print(f"Lowest: {weather_stats.lowest_temp.min_temp}C on {weather_stats.lowest_temp.observation_date}")
            print(f"Humidity: {weather_stats.highest_humidity.max_humidity}% on {weather_stats.highest_humidity.observation_date}")

    def generate_monthly_report(self, weather_stats):
        avg_max_temp, avg_min_temp, avg_mean_humidity = weather_stats.compute_averages()
        print(f"Highest Average Temperature: {avg_max_temp:.0f}C")
        print(f"Lowest Average Temperature: {avg_min_temp:.0f}C")
        print(f"Average Mean Humidity: {avg_mean_humidity:.0f}%")

    def generate_monthly_bar_chart(self, readings, combined):
        if not readings:
            return
        month_name = datetime.strptime(readings[0].observation_date, "%Y-%m-%d").strftime("%B %Y")
        print(f"{month_name}")
        for reading in readings:
            day = datetime.strptime(reading.observation_date, "%Y-%m-%d").day
            high_bar = f"{RED}{'+' * round(reading.max_temp)}{RESET}"
            low_bar = f"{BLUE}{'+' * round(reading.min_temp)}{RESET}"

            if combined:
                print(f"{day:02d} {low_bar} {high_bar} {reading.min_temp}C - {reading.max_temp}C")
            else:
                print(f"{day} {high_bar} {reading.max_temp}C")
                print(f"{day} {low_bar} {reading.min_temp}C")
