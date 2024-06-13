import csv
from weather_reading import WeatherReading


class WeatherParser:
    """A class to parse weather data from a CSV file and create WeatherReading objects."""

    selected_weather_attributes = {}

    def parse_weather_file(self, file_path):
        """
        Parse a weather CSV file and return a list of WeatherReading objects.

        Args:
            file_path (str): Path to the weather CSV file.

        Returns:
            list: A list of WeatherReading objects created from the parsed data.

        Raises:
            FileNotFoundError: If the specified file_path does not exist.
            ValueError: If there are issues with reading or parsing the file.
        """
        weather_readings = []

        try:
            with open(file_path, 'r') as weather_file:
                weather_file = csv.reader(weather_file)
                weather_readings = self.assign_values(weather_file)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            raise
        except ValueError as e:
            print(e)
            raise
        
        return weather_readings

    def read_header(self, weather_file):
        """
        Read and validate the header of the weather CSV file.

        Args:
            weather_file: CSV reader object for the weather file.

        Returns:
            dict: A dictionary mapping selected weather attributes to their indices in the file.

        Raises:
            ValueError: If required weather attributes are missing in the header.
        """
        header = [header.strip() for header in next(weather_file)]
        alternative_weather_attributes = [
            ("PKT", "PKST"), "Max TemperatureC", "Min TemperatureC", "Max Humidity", "Mean Humidity"
        ]

        for weather_attribute in alternative_weather_attributes:
            if isinstance(weather_attribute, tuple):
                for selected_attribute in weather_attribute:
                    if selected_attribute not in header:
                        continue
                    elif selected_attribute in header:
                        self.selected_weather_attributes[weather_attribute] = selected_attribute
                    else:
                        raise ValueError(
                            f"None of the alternative weather attributes {weather_attribute} found in the header"
                        )
            else:
                if weather_attribute not in header:
                    raise ValueError(f"Required attribute {weather_attribute} not found in the header")
                self.selected_weather_attributes[weather_attribute] = weather_attribute

        weather_field_indices = {
            self.selected_weather_attributes[key]: header.index(self.selected_weather_attributes[key])
            for key in self.selected_weather_attributes
        }

        return weather_field_indices

    def assign_values(self, weather_file):
        """
        Assign values from the weather CSV file to WeatherReading objects.

        Args:
            weather_file (csv.reader): CSV reader object for the weather file.

        Returns:
            list: A list of WeatherReading objects created from the parsed data.
        """
        weather_readings = []
        weather_field_indices = self.read_header(weather_file)
        next(weather_file) 

        for weather_record in weather_file:
            try:
                selected_fields = {
                    self.selected_weather_attributes[key]: weather_record[weather_field_indices[self.selected_weather_attributes[key]]]
                    for key in self.selected_weather_attributes
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
            
            weather_reading = WeatherReading(
                observation_date, max_temperature, min_temperature, max_humidity, mean_humidity
            )
            weather_readings.append(weather_reading)

        return weather_readings
