import time
from dji_asdk_to_python.products.aircraft import Aircraft
from dji_asdk_to_python.errors import CustomError


APP_IP = "192.168.100.206"
SIGNALING_SERVER = "https://webrtc-signaling-server-demo.herokuapp.com"
SECRET_KEY = "YOUR_SECRET_KEY"

aircraft = Aircraft(APP_IP)
cv2_with_webrtc_manager = aircraft.getLiveStreamManager().getCV2_With_WebRTC_Manager()
cv2_with_webrtc_manager.start(SIGNALING_SERVER, SECRET_KEY)

time.sleep(100)

cv2_with_webrtc_manager.stop()
