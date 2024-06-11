import argparse

from weather_data_reader import WeatherDataReader
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
        weather_report.generate_yearly_report(yearly_calculations)

    if args.a:
        year, month = map(int, args.a.split('/'))
        print(f"Reading data for {year}/{month}:")
        monthly_calculations = data_reader.read_monthly_readings(year, month)
        weather_report.generate_monthly_report(monthly_calculations)

    if args.c:
        year, month = map(int, args.c.split('/'))
        print(f"Reading columnar data for {year}/{month}:")
        monthly_readings = data_reader.read_monthly_column_readings(year, month)
        weather_report.generate_monthly_bar_chart(monthly_readings, combined=True)

if __name__ == "__main__":
    main()
