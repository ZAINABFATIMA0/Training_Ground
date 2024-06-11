import csv
from weather_reading import WeatherReading


class WeatherParser:

    actual_keys = {}

    def parse_weather_file(self, file_path):
        try:
            with open(file_path, 'r') as weather_file:
                csv_weather_file = csv.reader(weather_file)
                weather_readings = self.assign_values(csv_weather_file)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except ValueError as e:
            print(e)
        return weather_readings

    def read_header(self, csv_weather_file):
        header = [header.strip() for header in next(csv_weather_file)]
        alternative_keys = [("PKT", "PKST"), "Max TemperatureC", "Min TemperatureC", "Max Humidity", "Mean Humidity"]

        for key in alternative_keys:
            if isinstance(key, tuple):
                for value in key:
                    if value not in header:
                        continue
                    elif(value in header):
                        self.actual_keys[key] = value
                    else:
                        raise ValueError(f"None of the alternative keys {key} found in the header")
            else:
                if key not in header:
                    raise ValueError(f"Required field {key} not found in the header")
                self.actual_keys[key] = key

        field_indices = {self.actual_keys[key]: header.index(self.actual_keys[key]) for key in self.actual_keys}
        return field_indices
        
    def assign_values(self, csv_weather_file):
        weather_reading = []
        field_indices = self.read_header(csv_weather_file)
        next(csv_weather_file) 
        for weather_record in csv_weather_file:
            try:
                selected_fields = {self.actual_keys[key]: weather_record[field_indices[self.actual_keys[key]]] for key in self.actual_keys}
            except IndexError:
                continue
            if '' in selected_fields.values():
                continue
            obs_date = selected_fields[self.actual_keys[("PKT", "PKST")]]
            max_temp = float(selected_fields["Max TemperatureC"])
            min_temp = float(selected_fields["Min TemperatureC"])
            max_humidity = float(selected_fields["Max Humidity"])
            mean_humidity = float(selected_fields["Mean Humidity"])
            weatherreadings = WeatherReading(obs_date, max_temp, min_temp, max_humidity, mean_humidity)
            weather_reading.append(weatherreadings)
        return(weather_reading)
