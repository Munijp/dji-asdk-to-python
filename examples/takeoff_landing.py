# importing dji-asdk-to-python library

from dji_asdk_to_python.products.aircraft import Aircraft
from dji_asdk_to_python.flight_controller.flight_controller_state import FlightControllerState
from dji_asdk_to_python.flight_controller.flight_mode import FlightMode

# Setup aircraft ip

APP_IP = "192.168.100.210"
drone = Aircraft(APP_IP)

# init flight controller

fc = drone.getFlightController()

# executing take off

print(fc.startTakeoff())

# validate state of flight controller

while True:

    # validating the allowed state

    flight_controller_state = fc.getState()
    if not isinstance(flight_controller_state, FlightControllerState):
        print(flight_controller_state)
        continue
    
    # Evaluate the Drone state to finish the loop "is flying and the mode isn't AUTO_TAKEOFF"

    flight_mode = flight_controller_state.getFlightMode()
    if flight_controller_state.isFlying() and flight_mode != FlightMode.AUTO_TAKEOFF:
        break

# starting landing

print(fc.startLanding())
