from dji_asdk_to_python.flight_controller.location_coordinate_2d import LocationCoordinate2D
from dji_asdk_to_python.products.aircraft import Aircraft
import time

app_ip = "192.168.100.203"



drone = Aircraft(app_ip)
fc = drone.getFlightController()
home_location = fc.getHomeLocation()

print(home_location)

