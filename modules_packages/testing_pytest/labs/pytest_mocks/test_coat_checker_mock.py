"""Tests for coat_checker using pytest and unittest.mock."""

import pytest
from unittest.mock import MagicMock, patch
from weather_forecast import HourlyForecast
from coat_checker import (
    need_water_proof,
    coat_warmth,
    main,
    RAIN_PROBABILITY_THRESHOLD,
    WINTER_WARMTH_THRESHOLD,
    SPRING_FALL_WARMTH_THRESHOLD,
    LIGHT_WARMTH_THRESHOLD,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_forecast(temperature: float, precipitation_probability: float) -> HourlyForecast:
    """Create a minimal HourlyForecast for testing."""
    return HourlyForecast(date_time=None, temperature=temperature, precipitation_probability=precipitation_probability)


# ---------------------------------------------------------------------------
# need_water_proof
# ---------------------------------------------------------------------------

class TestNeedWaterProof:
    def test_returns_true_when_probability_equals_threshold(self):
        forecasts = [make_forecast(10, RAIN_PROBABILITY_THRESHOLD)]
        assert need_water_proof(forecasts) is True

    def test_returns_true_when_probability_exceeds_threshold(self):
        forecasts = [make_forecast(10, RAIN_PROBABILITY_THRESHOLD + 1)]
        assert need_water_proof(forecasts) is True

    def test_returns_false_when_all_probabilities_below_threshold(self):
        forecasts = [make_forecast(10, RAIN_PROBABILITY_THRESHOLD - 1)]
        assert need_water_proof(forecasts) is False

    def test_returns_true_when_any_hour_exceeds_threshold(self):
        forecasts = [
            make_forecast(10, 0),
            make_forecast(10, RAIN_PROBABILITY_THRESHOLD),
            make_forecast(10, 10),
        ]
        assert need_water_proof(forecasts) is True

    def test_returns_false_for_empty_list(self):
        assert need_water_proof([]) is False


# ---------------------------------------------------------------------------
# coat_warmth
# ---------------------------------------------------------------------------

class TestCoatWarmth:
    def test_returns_winter_when_below_winter_threshold(self):
        forecasts = [make_forecast(WINTER_WARMTH_THRESHOLD - 1, 0)]
        assert coat_warmth(forecasts) == "winter"

    def test_returns_winter_at_zero_degrees(self):
        forecasts = [make_forecast(0, 0)]
        assert coat_warmth(forecasts) == "winter"

    def test_returns_spring_fall_at_winter_threshold(self):
        forecasts = [make_forecast(WINTER_WARMTH_THRESHOLD, 0)]
        assert coat_warmth(forecasts) == "spring/fall"

    def test_returns_spring_fall_between_thresholds(self):
        forecasts = [make_forecast(10, 0)]
        assert coat_warmth(forecasts) == "spring/fall"

    def test_returns_light_at_spring_fall_threshold(self):
        forecasts = [make_forecast(SPRING_FALL_WARMTH_THRESHOLD, 0)]
        assert coat_warmth(forecasts) == "light"

    def test_returns_light_between_spring_fall_and_light_thresholds(self):
        forecasts = [make_forecast(16, 0)]
        assert coat_warmth(forecasts) == "light"

    def test_returns_none_at_light_threshold(self):
        forecasts = [make_forecast(LIGHT_WARMTH_THRESHOLD, 0)]
        assert coat_warmth(forecasts) is None

    def test_returns_none_above_light_threshold(self):
        forecasts = [make_forecast(25, 0)]
        assert coat_warmth(forecasts) is None

    def test_uses_minimum_temperature_across_hours(self):
        forecasts = [
            make_forecast(20, 0),
            make_forecast(WINTER_WARMTH_THRESHOLD - 1, 0),
            make_forecast(15, 0),
        ]
        assert coat_warmth(forecasts) == "winter"

    def test_returns_none_for_empty_list(self):
        assert coat_warmth([]) is None


# ---------------------------------------------------------------------------
# main — WeatherService mocked
# ---------------------------------------------------------------------------

class TestMain:
    def _run_main_with(self, temperature: float, precipitation: float, capsys):
        """Helper: mock WeatherService.get_forecast and run main()."""
        mock_forecasts = [make_forecast(temperature, precipitation)]
        with patch("coat_checker.WeatherService") as MockService:
            MockService.return_value.get_forecast.return_value = mock_forecasts
            main()
        return capsys.readouterr().out.strip()

    def test_winter_rain_jacket(self, capsys):
        output = self._run_main_with(temperature=2, precipitation=50, capsys=capsys)
        assert "winter" in output
        assert "rain" in output.lower()

    def test_winter_no_rain(self, capsys):
        output = self._run_main_with(temperature=2, precipitation=0, capsys=capsys)
        assert "winter" in output
        assert "rain" not in output.lower()

    def test_spring_fall_rain_jacket(self, capsys):
        output = self._run_main_with(temperature=10, precipitation=50, capsys=capsys)
        assert "spring/fall" in output
        assert "rain" in output.lower()

    def test_light_jacket_no_rain(self, capsys):
        output = self._run_main_with(temperature=16, precipitation=0, capsys=capsys)
        assert "light" in output
        assert "rain" not in output.lower()

    def test_no_jacket_no_rain(self, capsys):
        output = self._run_main_with(temperature=20, precipitation=0, capsys=capsys)
        assert "no jacket" in output.lower()

    def test_no_jacket_but_rain_brings_umbrella(self, capsys):
        output = self._run_main_with(temperature=20, precipitation=50, capsys=capsys)
        assert "umbrella" in output.lower()

    def test_weather_service_constructed_with_bcit_dtc(self):
        mock_forecasts = [make_forecast(10, 0)]
        with patch("coat_checker.WeatherService") as MockService:
            MockService.return_value.get_forecast.return_value = mock_forecasts
            main()
            # Verify WeatherService was constructed with BCIT_DTC
            from constants import BCIT_DTC
            MockService.assert_called_once_with(BCIT_DTC)

    def test_get_forecast_called_once(self):
        mock_forecasts = [make_forecast(10, 0)]
        with patch("coat_checker.WeatherService") as MockService:
            MockService.return_value.get_forecast.return_value = mock_forecasts
            main()
            MockService.return_value.get_forecast.assert_called_once()
