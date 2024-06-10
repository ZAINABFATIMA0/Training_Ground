class WeatherReading:
    def __init__(self, observation_date, max_temp, min_temp, max_humidity, mean_humidity):
        self.observation_date = observation_date
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity
                                                                                                   
    def __repr__(self):
        return (f"WeatherReading(date={self.observation_date}, max_temp={self.max_temp}, min_temp={self.min_temp},"              
                f"max_humidity={self.max_humidity}, mean_humidity={self.mean_humidity})")