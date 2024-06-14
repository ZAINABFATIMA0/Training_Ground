import argparse
import re

from weather_matrix_reader import WeatherDataReader
from weather_report import WeatherReport

def validate_month(month):
    month = f"{month:02d}"
    month_validity_check = re.match(r"^(0[1-9]|1[0-2])$", month)
    return month_validity_check

def main():
    """
    Main function to handle command-line arguments and generate weather reports accordingly.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=str)
    parser.add_argument("-e", type=int)
    parser.add_argument("-a", type=str)
    parser.add_argument("-c", type=str)

    args = parser.parse_args()
    weather_report = WeatherReport()
    data_reader = WeatherDataReader(args.directory)

    if args.e:
        year = args.e
        print(f"Reading all files for the year {year}:")
        yearly_calculations = data_reader.read_yearly_data(year)
        if yearly_calculations is not None:
            weather_report.generate_yearly_report(yearly_calculations)
        else:
            print("No data available for the specified year.")

    if args.a:
        year, month = map(int, args.a.split('/'))
        if not validate_month(month):
            print(f"Error: Month index is out of range for argument 'a'. "
                  f"Please provide a month number between 1 and 12.")
        else:
            print(f"Reading data for {year}/{month}:")
            try:
                monthly_calculations = data_reader.read_monthly_readings(year, month)
                if monthly_calculations is not None:
                    weather_report.generate_monthly_report(monthly_calculations)
                else:
                    print("No data available for the specified month.")
            except IndexError as e:
                print(f"Error reading data: {e}")

    if args.c:
        year, month = map(int, args.c.split('/'))
        if not validate_month(month):
            print(f"Error: Month index is out of range for argument 'c'. "
                  f"Please provide a month number between 1 and 12.")
        else:
            print(f"Drawing temperature bar charts for {year}/{month}:")
            try:
                monthly_readings = data_reader.read_monthly_column_readings(year, month)
                weather_report.generate_monthly_bar_chart(monthly_readings, combined_bar_charts = True)
            except IndexError as e:
                print(f"Error reading data: {e}")

if __name__ == "__main__":
    main()
