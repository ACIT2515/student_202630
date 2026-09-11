"""Geographic location model with automatic timezone resolution."""

from zoneinfo import ZoneInfo
from timezonefinder import TimezoneFinder


class Location:
    """Geographic location with coordinates and an auto-derived timezone.
    
    Attributes:
        latitude: Latitude coordinate in decimal degrees.
        longitude: Longitude coordinate in decimal degrees.
        timezone: ZoneInfo object derived lazily from coordinates (memoized).
    """

    def __init__(self, latitude: float, longitude: float):
        """Initialise a Location with geographic coordinates.

        Args:
            latitude: Latitude coordinate in decimal degrees.
            longitude: Longitude coordinate in decimal degrees.
        """
        self.latitude = latitude
        self.longitude = longitude

    @property
    def timezone(self) -> ZoneInfo:
        """Derive the timezone from the location's coordinates.

        Returns:
            ZoneInfo object for the location's timezone.

        Raises:
            ValueError: If the timezone cannot be determined for the given coordinates.
        """
        tz_name = TimezoneFinder().timezone_at(lat=self.latitude, lng=self.longitude)
        if tz_name is None:
            raise ValueError(f"Could not determine timezone for coordinates ({self.latitude}, {self.longitude})")
        return ZoneInfo(tz_name)
