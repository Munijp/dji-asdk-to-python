from dji_asdk_to_python.products.aircraft import Aircraft
from dji_asdk_to_python.mission_control.waypoint.waypoint import LocationCoordinate2D
from dji_asdk_to_python.mission_action.mission_action import MissionAction

import time
APP_IP = "192.168.0.112"

drone = Aircraft(APP_IP)
mission_action = drone.getMissionAction()

coordinate = LocationCoordinate2D(3.3310794794873844, -76.53948434110453)


mission_action.aircraftYawAction(45, True)
time.sleep(3)
mission_action.goToAction(coordinate.__dict__, 15)

