import csv
from weather_reading import WeatherReading


class WeatherParser:

    selected_weather_attributes = {}

    def parse_weather_file(self, file_path):
        weather_readings = []  

        try:
            with open(file_path, 'r') as weather_file:
                weather_file = csv.reader(weather_file)
                weather_readings = self.assign_values(weather_file)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except ValueError as e:
            print(e)
        return weather_readings

    def read_header(self, weather_file):
        header = [header.strip() for header in next(weather_file)]
        alternative_weather_attributes = [
            ("PKT", "PKST"), "Max TemperatureC", "Min TemperatureC", "Max Humidity", "Mean Humidity"
            ]

        for weather_attribute in alternative_weather_attributes:
            if isinstance(weather_attribute, tuple):
                for selected_attribute in weather_attribute:
                    if selected_attribute not in header:
                        continue
                    elif(selected_attribute in header):
                        self.selected_weather_attributes[weather_attribute] = selected_attribute
                    else:
                        raise ValueError(
                            f"None of the alternative weather attributes {weather_attribute} found in the header"
                        )
            else:
                if weather_attribute not in header:
                    raise ValueError(f"Required attribue {weather_attribute} not found in the header")
                self.selected_weather_attributes[weather_attribute] = weather_attribute

        weather_field_indices = {
            self.selected_weather_attributes[key]: header.index(self.selected_weather_attributes[key])
            for key in self.selected_weather_attributes
        }

        return weather_field_indices
        
    def assign_values(self, weather_file):
        weather_reading = []
        weather_field_indices = self.read_header(weather_file)
        next(weather_file) 

        for weather_record in weather_file:
            try:
                selected_fields = {
                    self.selected_weather_attributes[key]: weather_record[weather_field_indices
                    [self.selected_weather_attributes[key]]] for key in self.selected_weather_attributes
                }
            except IndexError:
                continue
            if '' in selected_fields.values():
                continue
            
            observation_date = selected_fields[self.selected_weather_attributes[("PKT", "PKST")]]
            max_temperature = float(selected_fields["Max TemperatureC"])
            min_temperature = float(selected_fields["Min TemperatureC"])
            max_humidity = float(selected_fields["Max Humidity"])
            mean_humidity = float(selected_fields["Mean Humidity"])
            weatherreadings = WeatherReading(
                observation_date, max_temperature, min_temperature, max_humidity, mean_humidity
            )
            weather_reading.append(weatherreadings)

        return(weather_reading)
