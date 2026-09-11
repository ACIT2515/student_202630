"""Coat checker app that recommends outerwear based on the weather forecast."""

from weather_forecast import WeatherService, HourlyForecast
from constants import BCIT_DTC


RAIN_PROBABILITY_THRESHOLD = 30   # percent
WINTER_WARMTH_THRESHOLD = 6         # degrees Celsius
SPRING_FALL_WARMTH_THRESHOLD = 14   # degrees Celsius
LIGHT_WARMTH_THRESHOLD = 18   # degrees Celsius

def need_water_proof(forecasts: list[HourlyForecast]) -> bool:
    """Determine if a rain jacket is needed based on the forecast.

    Args:
        forecasts: List of HourlyForecast objects for the period of interest.

    Returns:
        True if precipitation probability reaches or exceeds the threshold in
        any forecast hour, False otherwise.
    """
    return any(forecast.precipitation_probability >= RAIN_PROBABILITY_THRESHOLD for forecast in forecasts)


def coat_warmth(forecasts: list[HourlyForecast]) -> str | None:
    """Recommend the appropriate warmth of coat based on temperature 

    Coat recommendations by minimum temperature:
        - Below 6 degrees C:     winter 
        - 6 to 14 degrees C:     spring/fall 
        - 14 to 18 degrees C:    light 
        - above 18 degrees C:    None

    Args:
        forecasts: List of HourlyForecast objects for the period of interest.

    Returns:
        A string recommendation describing warmth of jacket.
    """
    if not forecasts:
        return None
    min_temp = min(forecast.temperature for forecast in forecasts)

    if min_temp < WINTER_WARMTH_THRESHOLD:
        coat_type = "winter"
    elif min_temp < SPRING_FALL_WARMTH_THRESHOLD:
        coat_type = "spring/fall"
    elif min_temp < LIGHT_WARMTH_THRESHOLD:
        coat_type = "light"
    else:
        coat_type = None

    return coat_type


def main():
    service = WeatherService(BCIT_DTC)
    forecasts = service.get_forecast()
    coat_type = coat_warmth(forecasts)
    is_water_proof = need_water_proof(forecasts)
    if is_water_proof:
        if coat_type:
            print(f"Bring a {coat_type} rain jacket")
        else:
            print(f"Bring an umbrella")
    else:
        if coat_type:
            print(f"Bring a {coat_type} jacket ")
        else:
            print("No jacket needed today")


if __name__ == "__main__":
    main()