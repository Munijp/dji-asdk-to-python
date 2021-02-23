import enum


class GPSSignalLevel(enum.Enum):
    """
    A enum class representing GPS signal levels, which are used to measure the signal quality.
        - LEVEL_0: The GPS has almost no signal, which is very bad.
        - LEVEL_1: The GPS signal is very weak.
        - LEVEL_2: The GPS signal is weak. At this level, the aircraft's go home functionality will still work.
        - LEVEL_3: The GPS signal is good. At this level, the aircraft can hover in the air.
        - LEVEL_4: The GPS signal is very good. At this level, the aircraft can record the home point.
        - LEVEL_5: The GPS signal is very strong.
        - NONE: There is no GPS signal.
    """
    LEVEL_0 = "LEVEL_0"
    LEVEL_1 = "LEVEL_1"
    LEVEL_2 = "LEVEL_2"
    LEVEL_3 = "LEVEL_3"
    LEVEL_4 = "LEVEL_4"
    LEVEL_5 = "LEVEL_5"
    NONE = "NONE"
