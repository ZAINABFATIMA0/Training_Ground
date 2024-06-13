class WeatherReading:
    """A class representing weather readings.

    Attributes:
        observation_date (str): The date of the observation.
        max_temperature (float): The maximum temperature recorded that day.
        min_temperature (float): The minimum temperature recorded that day.
        max_humidity (float): The maximum humidity recorded that day.
        mean_humidity (float): The mean humidity recorded taht day.
    """

    def __init__(self, observation_date, max_temperature, min_temperature, max_humidity, mean_humidity):
        """
        Initialize a WeatherReading object.

        Args:
            observation_date (str): The date of the observation.
            max_temperature (float): The maximum temperature recorded.
            min_temperature (float): The minimum temperature recorded.
            max_humidity (float): The maximum humidity recorded.
            mean_humidity (float): The mean humidity recorded.
        """
        self.observation_date = observation_date
        self.max_temperature = max_temperature
        self.min_temperature = min_temperature
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity

    def __repr__(self):
        """
        Return a string representation of the WeatherReading object.

        Returns:
            str: String representation of the object.
        """
        return (f"WeatherReading(date={self.observation_date}, "
                f"max_temperature={self.max_temperature}, "
                f"min_temperature={self.min_temperature}, "
                f"max_humidity={self.max_humidity}, "
                f"mean_humidity={self.mean_humidity})")
