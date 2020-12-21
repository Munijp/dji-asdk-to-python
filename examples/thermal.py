from dji_asdk_to_python.camera.display_mode import DisplayMode
from dji_asdk_to_python.camera.camera import Camera

APP_IP = "192.168.100.203"

camera = Camera(app_ip=APP_IP)
print(camera)

res = camera.setDisplayMode(DisplayMode.THERMAL_ONLY)
print(res)