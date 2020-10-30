from dji_asdk_to_python.products.aircraft import Aircraft
from dji_asdk_to_python.battery.battery_state import BatteryState

APP_IP = "192.168.0.112"

drone = Aircraft(APP_IP)
battery = drone.getBattery()
battery_state = battery.getBatteryState()
print("battery state %s" % battery_state.getChargeRemainingInPercent())
