from dji_asdk_to_python.flight_controller.location_coordinate_2d import LocationCoordinate2D
from dji_asdk_to_python.products.aircraft import Aircraft
import time

app_ip = "192.168.100.203"

drone = Aircraft(app_ip)
fc = drone.getFlightController()

homeLocation = LocationCoordinate2D(3.3310794794873844, -76.53948434110453)

current_home_location = fc.getHomeLocation()
print(current_home_location)
# fc.setHomeLocation(homeLocation)
# fc.startGoHome(startGoHomeCallback)
# fc.cancelGoHome(cancelGoHomeCallback)

