from weather_reading import WeatherReading


class WeatherParser:
    def parse_weather_file(self, file_path):
        weather_readings = []
        try:
            with open(file_path, 'r') as weather_file:
                header = [item.strip() for item in next(weather_file).strip().split(',')]
                alternative_keys = [("PKT", "PKST"), "Max TemperatureC", "Min TemperatureC", "Max Humidity", "Mean Humidity"]
                actual_keys = {}
                for key in alternative_keys:
                    if isinstance(key, tuple):
                        for value in key:
                            if value in header:
                                actual_keys[key] = value
                                break
                        else:
                            raise ValueError(f"None of the alternative keys {key} found in the header")
                    else:
                        if key not in header:
                            raise ValueError(f"Required field {key} not found in the header")
                        actual_keys[key] = key

                field_indices = {actual_keys[key]: header.index(actual_keys[key]) for key in actual_keys}

                for weather_record in weather_file:
                    parts = weather_record.strip().split(',')
                    try:
                        selected_fields = {actual_keys[key]: parts[field_indices[actual_keys[key]]] for key in actual_keys}
                    except IndexError:
                        continue

                    if '' in selected_fields.values():
                        continue

                    obs_date = selected_fields[actual_keys[("PKT", "PKST")]]
                    max_temp = float(selected_fields["Max TemperatureC"])
                    min_temp = float(selected_fields["Min TemperatureC"])
                    max_humidity = float(selected_fields["Max Humidity"])
                    mean_humidity = float(selected_fields["Mean Humidity"])
                    reading = WeatherReading(obs_date, max_temp, min_temp, max_humidity, mean_humidity)
                    weather_readings.append(reading)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except ValueError as e:
            print(e)
        return weather_readings
