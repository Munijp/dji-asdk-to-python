import time

from dji_asdk_to_python.products.aircraft import Aircraft

APP_IP = "192.168.100.203"

aircraft = Aircraft(APP_IP)
video_record_manager = aircraft.getVideoRecordManager()

video_record_manager.start_record("/media/jetson-a0002/DATA/video_records/drone.mp4")
time.sleep(20)  # record for 20 seconds
video_record_manager.stop_record()
