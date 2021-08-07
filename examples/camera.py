from dji_asdk_to_python.products.aircraft import Aircraft
from dji_asdk_to_python.camera.camera import Camera
from dji_asdk_to_python.camera.exposure_mode import ExposureMode
from dji_asdk_to_python.camera.iso import ISO
from dji_asdk_to_python.camera.shutter_speed import ShutterSpeed

APP_IP = "192.168.1.14"

drone = Aircraft(APP_IP)
camera = drone.getCamera()

# print("Exposure Mode : %s" % camera.getExposureMode())
# print("ISO : %s" % camera.getISO())
# print("Shutter Speed : %s" % camera.getShutterSpeed())
# print(camera.setExposureMode(ExposureMode.PROGRAM))

#ARUCO LANDING FOR ISO AFTERNOON DAY
# print(camera.setExposureMode(ExposureMode.MANUAL))
# camera.setISO(ISO.ISO_400)
# camera.setShutterSpeed(ShutterSpeed.SHUTTER_SPEED_1_2000)

cameraType = "EVENING"

if cameraType == "DAY_VERY_SUNNY":
    camera.setISO(ISO.ISO_50)
    camera.setShutterSpeed(ShutterSpeed.SHUTTER_SPEED_1_8000)
elif cameraType == "DAY_SUNNY":
    camera.setISO(ISO.ISO_200)
    camera.setShutterSpeed(ShutterSpeed.SHUTTER_SPEED_1_4000)
elif cameraType == "DAY_AFTERNOON":
    camera.setISO(ISO.ISO_400)
    camera.setShutterSpeed(ShutterSpeed.SHUTTER_SPEED_1_2000)
elif cameraType == "EVENING":
    camera.setISO(ISO.ISO_400)
    camera.setShutterSpeed(ShutterSpeed.SHUTTER_SPEED_1_8000)
elif cameraType == "MORNING":
    camera.setISO(ISO.ISO_400)
    camera.setShutterSpeed(ShutterSpeed.SHUTTER_SPEED_1_4000)


print("Exposure Mode : %s" % camera.getExposureMode())
print("ISO : %s" % camera.getISO())
print("Shutter Speed : %s" % camera.getShutterSpeed())
