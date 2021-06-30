from dji_asdk_to_python.products.aircraft import Aircraft
from dji_asdk_to_python.camera.camera import Camera
from dji_asdk_to_python.camera.exposure_mode import ExposureMode
from dji_asdk_to_python.camera.iso import ISO
from dji_asdk_to_python.camera.shutter_speed import ShutterSpeed

APP_IP = "192.168.100.210"

drone = Aircraft(APP_IP)
camera = drone.getCamera()

print("Exposure Mode : %s" % camera.getExposureMode())
print("ISO : %s" % camera.getISO())
print("Shutter Speed : %s" % camera.getShutterSpeed())

# print(camera.setExposureMode(ExposureMode.PROGRAM))

# NIGHT SETTINGS
# TO DEFINE...

# ARUCA LANDING - DAY SETTINGS
print(camera.setExposureMode(ExposureMode.MANUAL))
print(camera.setISO(ISO.ISO_100))
print(camera.setShutterSpeed(ShutterSpeed.SHUTTER_SPEED_1_8000))

# ARUCA LANDING - DAY SHADOW SETTINGS
print(camera.setExposureMode(ExposureMode.MANUAL))
print(camera.setISO(ISO.ISO_400))
print(camera.setShutterSpeed(ShutterSpeed.SHUTTER_SPEED_1_8000))

# ARUCA LANDING - Night SETTINGS
print(camera.setExposureMode(ExposureMode.MANUAL))
print(camera.setISO(ISO.ISO_800))
print(camera.setShutterSpeed(ShutterSpeed.SHUTTER_SPEED_1_2000))

print("Exposure Mode : %s" % camera.getExposureMode())
print("ISO : %s" % camera.getISO())
print("Shutter Speed : %s" % camera.getShutterSpeed())
