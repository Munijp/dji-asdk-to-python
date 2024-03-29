from dji_asdk_to_python.products.aircraft import Aircraft
from dji_asdk_to_python.flight_controller.flight_controller_state import (
    FlightControllerState,
)


APP_IP = "192.168.100.210"

drone = Aircraft(APP_IP)
fc = drone.getFlightController()
print(fc)
flight_controller_state = fc.getState()
print(flight_controller_state)
print("areMotorsOn %s " % flight_controller_state.areMotorsOn())
print("isFlying %s " % flight_controller_state.isFlying())
print("velocityX %s " % flight_controller_state.getVelocityX())
print("velocityY %s " % flight_controller_state.getVelocityY())
print("velocityZ %s " % flight_controller_state.getVelocityZ())

aircraft_location = flight_controller_state.getAircraftLocation()

print("getAltitude %s " % aircraft_location.getAltitude())
print("getLatitude %s " % aircraft_location.getLatitude())
print("getLongitude %s " % aircraft_location.getLongitude())

aircraft_attitude = flight_controller_state.getAttitude()

print("pitch %s " % aircraft_attitude.pitch)
print("roll %s " % aircraft_attitude.roll)
print("yaw %s " % aircraft_attitude.yaw)
print("GoHomeExecutionState %s" % flight_controller_state.getGoHomeExecutionState())
print("getFlightMode %s" % flight_controller_state.getFlightMode())
print("getGPSSignalLevel %s" % flight_controller_state.getGPSSignalLevel())
print("isLandingConfirmationNeeded %s" % flight_controller_state.isLandingConfirmationNeeded())
