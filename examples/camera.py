from dji_asdk_to_python.products.aircraft import Aircraft
from dji_asdk_to_python.camera.camera import Camera
from dji_asdk_to_python.camera.exposure_mode import ExposureMode
from dji_asdk_to_python.camera.iso import ISO
from dji_asdk_to_python.camera.shutter_speed import ShutterSpeed
import time
APP_IP = "192.168.0.174"

drone = Aircraft(APP_IP)
camera = drone.getCamera()

print("Exposure Mode : %s" % camera.getExposureMode())
print("ISO : %s" % camera.getISO())
print("Shutter Speed : %s" % camera.getShutterSpeed())

time.sleep(1)

camera.setExposureMode(ExposureMode.PROGRAM)
print(ExposureMode.MANUAL)
time.sleep(1)
camera.setISO(ISO.ISO_3200)
print(ISO.ISO_3200)
time.sleep(1)
camera.setShutterSpeed(ShutterSpeed.SHUTTER_SPEED_1_400)
print(ShutterSpeed.SHUTTER_SPEED_1_400)

time.sleep(1)

print("Exposure Mode : %s" % camera.getExposureMode())
print("ISO : %s" % camera.getISO())
print("Shutter Speed : %s" % camera.getShutterSpeed())