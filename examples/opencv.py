import cv2
import time

from dji_asdk_to_python.products.aircraft import Aircraft
from dji_asdk_to_python.errors import CustomError


APP_IP = "192.168.100.206"
STREAMING_DURATION = 1000  # seconds

aircraft = Aircraft(APP_IP)
streaming_manager = aircraft.getLiveStreamManager()
cv2_manager = streaming_manager.getCV2Manager()
cv2_manager.setWidth(1920)
cv2_manager.setHeigth(1080)
cv2_manager.set_stream_id("testing")
result = cv2_manager.startStream()
print("result startStream %s" % result)

start = time.time()
elapsed_seconds = 0

if isinstance(result, CustomError):
    raise Exception("%s" % result)

while elapsed_seconds < STREAMING_DURATION:
    end = time.time()
    elapsed_seconds = end - start
    frame = cv2_manager.getFrame()

    if frame is None:
        continue

    cv2.imshow("frame", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break


cv2.destroyAllWindows()

cv2_manager.stopStream()
