from dji_asdk_to_python.mission_control.waypoint import WaypointMissionOperator

""" 
This example tests:
    - Waits for all the waypoints of a mission to be uploaded
"""

APP_IP = "192.168.100.210"

wpmoperator = WaypointMissionOperator(app_ip=APP_IP)

result = wpmoperator.getCurrentState()
print("current WaypointMissionState %s" % result)
