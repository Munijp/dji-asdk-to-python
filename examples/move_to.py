# importing necessary libraries to starting working with Drone

import sys
import threading
from time import sleep
from dji_asdk_to_python.products.aircraft import Aircraft
from dji_asdk_to_python.flight_controller.flight_controller_state import FlightControllerState
from dji_asdk_to_python.flight_controller.flight_mode import FlightMode

# Global parameters

APP_IP = "192.168.100.210"

# function that allows to start take off

def starting_take_off(fc):

    #execution command to start take off
    fc.startTakeoff()

    while True:

        # validating the allowed state

        global flight_controller_state
        flight_controller_state = fc.getState()

        if not isinstance(flight_controller_state, FlightControllerState):
            print(flight_controller_state)
            continue

        # Evaluate the Drone state to finish the loop "is flying and the mode isn't AUTO_TAKEOFF"

        flight_mode = flight_controller_state.getFlightMode()
        if flight_controller_state.isFlying() and flight_mode != FlightMode.AUTO_TAKEOFF:
            break
    print('Take off done')

# entrypoint from terminal execution

if __name__ == '__main__':


    # Getting flight controller object

    drone = Aircraft(APP_IP)
    fc = drone.getFlightController()

    # getting variables from users

    pitch = float(input('Defina la distancia del pitch: '))
    roll = float(input('Defina la distancia del roll: '))
    throttle = float(input('Defina la distancia del throttle: '))
    speed = float(input('Defina la velocidad del drone: '))

    # starting Take off

    starting_take_off(fc)
    
    # cleaning 

    sys.stdout.flush()

    # defining move actions
    
    fc.move_distance(pitch_distance = pitch, 
                     roll_distance = roll, 
                     throttle_distance = throttle, 
                     meters_per_second = speed, 
                     order = ["ROLL","THROTTLE", "PITCH"])

    print(f'Throttle distance {throttle} reached')
    
    # time to wait for GPS response

    print('Waiting 3 seconds')
    sleep(3)

    # Verifying GPS telemetry

    print("getGPSSignalLevel %s" % flight_controller_state.getGPSSignalLevel())
    location = flight_controller_state.getAircraftLocation()

    try:
        print("Altitud: ", location.getAltitude())
        print("Latitud: ", location.getLatitude())
        print("Longitud: ", location.getLongitude())

    except Exception as e:
        print(f'The exeption is: {e}')

    # starting landing

    fc.startLanding()
    print('Landing done')
