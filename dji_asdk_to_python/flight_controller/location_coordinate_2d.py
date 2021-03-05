class LocationCoordinate2D:
    """
    This is a structure for presenting the location, latitude, longitude.
    """

    def __init__(self, latitude, longitude):
        """
        Args:
            latitude ([float]): Latitude in degrees
            longitude ([float]): Longitude in degrees
        """
        self.latitude = latitude
        self.longitude = longitude

    def getLatitude(self):
        """
        Returns:
            [float]: Returns the latitude.
        """
        return self.latitude

    def getLongitude(self):
        """
        Returns:
            [float]: Returns the longitude.
        """
        return self.longitude
