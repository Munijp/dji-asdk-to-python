from dji_asdk_to_python.products.aircraft import Aircraft
from dji_asdk_to_python.errors import CustomError


APP_IP = "192.168.100.206"
SIGNALING_SERVER = "https://webrtc-signaling-server-demo.herokuapp.com"
SECRET_KEY = "webrtc_testing"

aircraft = Aircraft(APP_IP)
streaming_manager = aircraft.getLiveStreamManager()
webrtc_manager = streaming_manager.getWebRTC_Manager()
webrtc_manager.start(SIGNALING_SERVER, SECRET_KEY)
