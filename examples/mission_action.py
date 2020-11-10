from dji_asdk_to_python.products.aircraft import Aircraft
from dji_asdk_to_python.mission_control.waypoint.waypoint import LocationCoordinate2D
from dji_asdk_to_python.mission_action.mission_action import MissionAction

import time
APP_IP = "192.168.0.119"

drone = Aircraft(APP_IP)
mission_action = drone.getMissionAction()

coordinate = LocationCoordinate2D(3.3310334728130204, -76.53937525628518)

print(mission_action)

print(mission_action.aircraftYawAction(-180, "false"))
time.sleep(5)
print(mission_action.aircraftYawAction(180, "false"))
print(mission_action.goToAction(coordinate, 20))
