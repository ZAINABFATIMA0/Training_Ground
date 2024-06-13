class WeatherCalculations:

    def update_calculations(self, weather_metrix):

        if not hasattr(self, "num_readings"):
            self.highest_temperature_record = self.lowest_temperature_record = self.highest_humidity_record = weather_metrix
            self.total_max_temperature = weather_metrix.max_temperature
            self.total_min_temperature = weather_metrix.min_temperature
            self.total_mean_humidity = weather_metrix.mean_humidity
            self.num_readings = 1
        else:
            self.highest_temperature_record = max(
                self.highest_temperature_record, weather_metrix, key=lambda x: x.max_temperature
                )
            self.lowest_temperature_record = min(
                self.lowest_temperature_record, weather_metrix, key=lambda x: x.min_temperature
                )
            self.highest_humidity_record = max(
                self.highest_humidity_record, weather_metrix, key=lambda x: x.max_humidity
                )

        self.total_max_temperature += weather_metrix.max_temperature
        self.total_min_temperature += weather_metrix.min_temperature
        self.total_mean_humidity += weather_metrix.mean_humidity
        self.num_readings += 1

    def compute_averages(self):
        if self.num_readings == 0:
            return None, None, None
        avg_max_temperature = self.total_max_temperature / self.num_readings
        avg_min_temperature = self.total_min_temperature / self.num_readings
        avg_mean_humidity = self.total_mean_humidity / self.num_readings
        return avg_max_temperature, avg_min_temperature, avg_mean_humidity
