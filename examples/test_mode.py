from dji_asdk_to_python.products.aircraft import Aircraft
from dji_asdk_to_python.flight_controller.flight_controller_state import FlightControllerState
from dji_asdk_to_python.flight_controller.flight_mode import FlightMode

APP_IP = "192.168.100.210"

if __name__ == '__main__':
    
    drone = Aircraft(APP_IP)
    ...