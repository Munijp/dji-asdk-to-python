import cv2
import socket
import time
import threading


class VideoRecordManager:
    VIDEO_WIDTH = 1280
    VIDEO_HEIGHT = 720
    VIDEO_FPS = 24.0

    def __init__(self, aircraft):
        self.aircraft = aircraft
        self.recording = False
        self.path = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive_frames(self):
        streaming_manager = self.aircraft.getLiveStreamManager()
        cv2_manager = streaming_manager.getCV2Manager(with_buffer=False)
        cv2_manager.setWidth(VideoRecordManager.VIDEO_WIDTH)
        cv2_manager.setHeigth(VideoRecordManager.VIDEO_HEIGHT)
        cv2_manager.startStream()

        video_size = (VideoRecordManager.VIDEO_WIDTH, VideoRecordManager.VIDEO_HEIGHT)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.path,
                              fourcc,
                              VideoRecordManager.VIDEO_FPS,
                              video_size)

        while self.recording:
            frame = cv2_manager.getFrame()
            time.sleep(1 / 60)

            if frame is None:
                continue
            out.write(frame)
        out.release()
        cv2_manager.stopStream()

    def start_record(self, path):
        self.recording = True
        self.path = path
        thread_record = threading.Thread(target=self.receive_frames, args=[])
        thread_record.start()

    def stop_record(self):
        self.recording = False
