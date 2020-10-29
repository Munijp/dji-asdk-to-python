from enum import Enum


class ExposureMode(Enum):
    PROGRAM = 1
    SHUTTER_PRIORITY = 2
    APERTURE_PRIORITY = 3
    MANUAL = 4
    UNKNOWN = 255

    def __str__(self):
        return self.name
