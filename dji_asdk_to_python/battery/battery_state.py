import uuid

class BatteryState:
    """
    This class keeps track of the real-time state of the battery.
    """

    class Callback:
        """
        Callback class that updates the flight controller's current state data. This method gets called 10 times per second after startUpdatingFlightControllerCurrentState is called.
        """

        def __init__(self, onUpdate):
            """
            Args:
                onUpdate ([function]): Called with a single arg of type FlightControllerState when the flight controller's current state data has been updated. This method is called 10 times per second.
            """
            assert callable(onUpdate)
            self.uid = uuid.uuid1()
            self.running = True
            self.onUpdate = onUpdate

    def __init__(self):
        self._battery_state = None

    # -------------------------------- BATTERY PROPERTIES ------------------------------------

    def getChargeRemainingInPercent(self):
        """
        Returns:
            [int]: the percentage of battery energy left with range [0, 100].
        """
        return self._battery_state
