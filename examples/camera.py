from dji_asdk_to_python.products.aircraft import Aircraft
from dji_asdk_to_python.camera.camera import Camera
from dji_asdk_to_python.camera.exposure_mode import ExposureMode
from dji_asdk_to_python.camera.iso import ISO
from dji_asdk_to_python.camera.shutter_speed import ShutterSpeed

APP_IP = "192.168.1.14"

drone = Aircraft(APP_IP)
camera = drone.getCamera()

print("Exposure Mode : %s" % camera.getExposureMode())
print("ISO : %s" % camera.getISO())
print("Shutter Speed : %s" % camera.getShutterSpeed())

print(camera.setExposureMode(ExposureMode.PROGRAM))
print(camera.setISO(ISO.ISO_800))
# print(camera.setShutterSpeed(ShutterSpeed.SHUTTER_SPEED_1_4000))

print("Exposure Mode : %s" % camera.getExposureMode())
print("ISO : %s" % camera.getISO())
print("Shutter Speed : %s" % camera.getShutterSpeed())
