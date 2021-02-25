import numpy as np

from dji_asdk_to_python.products.aircraft import Aircraft
from dji_asdk_to_python.precision_landing.landing import ArucoLanding

APP_IP = "192.168.100.203"
MARKER_ID = 17
MARKER_SIZE_CM = 60
IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 720
CAMERA_MATRIX = np.loadtxt("calibration/camera_matrix.txt", delimiter=",")
CAMERA_DISTORTION = np.loadtxt("calibration/camera_distortion.txt", delimiter=",")

aircraft = Aircraft(APP_IP)
aruco_landing = ArucoLanding(aircraft=aircraft,
                             width=IMAGE_WIDTH,
                             height=IMAGE_HEIGHT,
                             camera_distortion=CAMERA_DISTORTION,
                             camera_matrix=CAMERA_MATRIX,
                             marker_id=MARKER_ID,
                             marker_size_cm=MARKER_SIZE_CM)
aruco_landing.start(is_night=True)
