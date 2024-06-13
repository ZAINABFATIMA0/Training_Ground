class WeatherReading:

    def __init__(self, observation_date, max_temperature, min_temperature, max_humidity, mean_humidity):
        self.observation_date = observation_date
        self.max_temperature = max_temperature
        self.min_temperature = min_temperature
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity
                                                                                                   
    def __repr__(self):
        return (f"WeatherReading(date={self.observation_date}, max_temperature={self.max_temperature},"             
                f"min_temperature={self.min_temperature}, max_humidity={self.max_humidity},"
                f"mean_humidity={self.mean_humidity})")
