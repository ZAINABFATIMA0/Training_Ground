import argparse

from weather_matrix_reader import WeatherDataReader
from weather_report import WeatherReport

def main():
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
        if month < 1 or month > 12:
            print("Error: Month index is out of range. Please provide a month number between 1 and 12.")
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
        if month < 1 or month > 12:
            print("Error: Month index is out of range. Please provide a month number between 1 and 12.")
        else:
            print(f"Drawing temperature bar charts for {year}/{month}:")
            try:
                monthly_readings = data_reader.read_monthly_column_readings(year, month)
                weather_report.generate_monthly_bar_chart(monthly_readings, combined_bar_charts=True)
            except IndexError as e:
                print(f"Error reading data: {e}")


if __name__ == "__main__":
    main()
