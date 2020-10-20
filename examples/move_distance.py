import time
from dji_asdk_to_python.products.aircraft import Aircraft

APP_IP = "192.168.0.109"

drone = Aircraft(APP_IP)
fc = drone.getFlightController()
fc.move_distance(pitch_distance=-3, roll_distance=-3, throttle_distance=3, meters_per_second=0.3, order=["ROLL", "THROTTLE", "PITCH"])
