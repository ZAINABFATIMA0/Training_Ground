class WeatherCalculations:

    def update_calculations(self, reading):

        if not hasattr(self, "num_readings"):
            self.highest_temp = self.lowest_temp = self.highest_humidity = reading
            self.total_max_temp = reading.max_temp
            self.total_min_temp = reading.min_temp
            self.total_mean_humidity = reading.mean_humidity
            self.num_readings = 1
        else:
            self.highest_temp = max(self.highest_temp, reading, key=lambda x: x.max_temp)
            self.lowest_temp = min(self.lowest_temp, reading, key=lambda x: x.min_temp)
            self.highest_humidity = max(self.highest_humidity, reading, key=lambda x: x.max_humidity)

        self.total_max_temp += reading.max_temp
        self.total_min_temp += reading.min_temp
        self.total_mean_humidity += reading.mean_humidity
        self.num_readings += 1

    def compute_averages(self):
        if self.num_readings == 0:
            return None, None, None
        avg_max_temp = self.total_max_temp / self.num_readings
        avg_min_temp = self.total_min_temp / self.num_readings
        avg_mean_humidity = self.total_mean_humidity / self.num_readings
        return avg_max_temp, avg_min_temp, avg_mean_humidity
