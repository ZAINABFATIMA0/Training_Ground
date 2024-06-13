class WeatherCalculations:
    """A class to perform calculations on weather metrics.

    Attributes:
        num_readings (int): Number of weather readings processed.
        highest_temperature_record (WeatherReading or None): Weather record with Highest temperature.
        lowest_temperature_record (WeatherReading or None): Weather record with Lowest temperature.
        highest_humidity_record (WeatherReading or None): Weather record with Highest humidity.
        total_max_temperature (float): Total sum of maximum temperatures.
        total_min_temperature (float): Total sum of minimum temperatures.
        total_mean_humidity (float): Total sum of mean humidities.
    """

    def update_calculations(self, weather_metrics):
        """
        Update calculations based on a new weather metric readings.

        Args:
            weather_metrics (WeatherReading): Weather metrics object containing max_temperature,
                                              min_temperature, max_humidity and mean_humidity.
        """
        if not hasattr(self, "num_readings"):
            self.highest_temperature_record = self.lowest_temperature_record = self.highest_humidity_record = weather_metrics
            self.total_max_temperature = weather_metrics.max_temperature
            self.total_min_temperature = weather_metrics.min_temperature
            self.total_mean_humidity = weather_metrics.mean_humidity
            self.num_readings = 1
        else:
            self.highest_temperature_record = max(
                self.highest_temperature_record, weather_metrics, key=lambda x: x.max_temperature
            )
            self.lowest_temperature_record = min(
                self.lowest_temperature_record, weather_metrics, key=lambda x: x.min_temperature
            )
            self.highest_humidity_record = max(
                self.highest_humidity_record, weather_metrics, key=lambda x: x.max_humidity
            )

        self.total_max_temperature += weather_metrics.max_temperature
        self.total_min_temperature += weather_metrics.min_temperature
        self.total_mean_humidity += weather_metrics.mean_humidity
        self.num_readings += 1

    def compute_averages(self):
        """
        Compute average values of max temperature, min temperature, and mean humidity.

        Returns:
            float: Average max temperature.
            float: Average min temperature.
            float: Average mean humidity.
        
        Returns (None, None, None) if no readings have been processed yet.
        """
        if self.num_readings == 0:
            return None, None, None
        avg_max_temperature = self.total_max_temperature / self.num_readings
        avg_min_temperature = self.total_min_temperature / self.num_readings
        avg_mean_humidity = self.total_mean_humidity / self.num_readings
        print(type(avg_max_temperature))
        return avg_max_temperature, avg_min_temperature, avg_mean_humidity
