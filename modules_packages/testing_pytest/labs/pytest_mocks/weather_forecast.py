""" Weather forecasting library that uses Open-Meteo, an open-source weather 
API that offers free access for non-commercial use.

Resources:
1. https://open-meteo.com/en/docs/gem-api

"""
import openmeteo_requests

import pandas as pd
from datetime import date, datetime
from dataclasses import dataclass
from location import Location
import pprint

@dataclass
class HourlyForecast:
    """Hourly weather forecast with timezone-aware datetime.
    
    Attributes:
        date_time: datetime object for the forecast hour.
        temperature: Temperature in degrees Celsius.
        precipitation_probability: Probability of precipitation as a percentage (0-100).
    """
    date_time: datetime
    temperature: float
    precipitation_probability: float


class WeatherService:
    """Retrieves weather forecast data from the Open-Meteo API for a given location.

    Attributes:
        location: The geographic location to retrieve forecasts for.
    """

    _API_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, 
                 location: Location,
                 forecast_days: int = 1,
                 forecast_hours: int = 12,
                 past_hours: int = 0):
        """Initialize the WeatherService for a given location.

        Args:
            location: The geographic location to retrieve forecasts for.
            forecast_days: Number of days to forecast. Defaults to 1.
            forecast_hours: Number of hours to forecast. Defaults to 12.
            past_hours: Number of past hours to include. Defaults to 0.
        """
        self.location = location
        self._forecast_days = forecast_days
        self._forecast_hours = forecast_hours
        self._past_hours = past_hours
        self._client = openmeteo_requests.Client()

    def get_forecast(self, forecast_date: date | None = None) -> list[HourlyForecast]:
        """Get hourly weather forecast (temperature and possibility of 
        percipitation) for a specific date.

        Args:
            forecast_date: Date object for the forecast. Defaults to today if not provided.

        Returns:
            List of HourlyForecast objects for the next 12 hours.
        """
        if forecast_date is None:
            forecast_date = date.today()

        params = {
            "latitude": self.location.latitude,
            "longitude": self.location.longitude,
            "hourly": ["temperature_2m", "precipitation_probability"],
            "timezone": self.location.timezone.key,
            "forecast_days": self._forecast_days,   
            "forecast_hours": self._forecast_hours, 
            "past_hours": self._past_hours,      
        }

        responses = self._client.weather_api(self._API_URL, params=params)
        return self._parse_response(responses[0])

    def _parse_response(self, response) -> list[HourlyForecast]:
        """Parse a single Open-Meteo API response into a list of HourlyForecast objects.

        Args:
            response: A single Open-Meteo API response object.

        Returns:
            List of HourlyForecast objects containing the weather data.
        """
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_precipitation_probability = hourly.Variables(1).ValuesAsNumpy()

        date_times = pd.date_range(
            start=pd.to_datetime(hourly.Time() + response.UtcOffsetSeconds(), unit="s"),
            end=pd.to_datetime(hourly.TimeEnd() + response.UtcOffsetSeconds(), unit="s"),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        )

        return [
            HourlyForecast(
                date_time=dt,
                temperature=float(temp),
                precipitation_probability=float(precip),
            )
            for dt, temp, precip in zip(
                date_times, hourly_temperature_2m, hourly_precipitation_probability
            )
        ]


if __name__ == "__main__":
    from constants import BCIT_DTC
    service = WeatherService(BCIT_DTC)
    hourly_forecasts = service.get_forecast()
    pprint.pp(hourly_forecasts)
