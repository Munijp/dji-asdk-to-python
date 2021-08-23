from dji_asdk_to_python.products.aircraft import Aircraft
from dji_asdk_to_python.camera.display_mode import DisplayMode

APP_IP = "192.168.100.210"

drone = Aircraft(APP_IP)
camera = drone.getCamera()

#camera_mode = DisplayMode.VISUAL_ONLY
camera_mode = DisplayMode.THERMAL_ONLY

camera.setDisplayMode(camera_mode)

print(f"Changed camera mode to {camera_mode}")