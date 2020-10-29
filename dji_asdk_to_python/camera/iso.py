from enum import Enum


class ISO(Enum):
    AUTO = 0
    ISO_50 = 2
    ISO_100 = 3
    ISO_200 = 4
    ISO_400 = 5
    ISO_800 = 6
    ISO_1600 = 7
    ISO_3200 = 8
    ISO_6400 = 9
    ISO_12800 = 10
    ISO_25600 = 11
    FIXED = 255
    UNKNOWN = 65535

    def __str__(self):
        return self.name
