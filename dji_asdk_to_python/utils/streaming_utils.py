import threading
import os

on_rtd = os.environ.get('READTHEDOCS') == 'True'
if not on_rtd:
    import cv2


class VideoCaptureWithoutBuffer():
    def __init__(self, cap):
        self.cap = cap
        self.frame = None
        self.streaming = True
        t = threading.Thread(target=self._reader, args=[])
        t.start()

    def _reader(self):
        while self.streaming:
            ret, frame = self.cap.read()
            if ret:
                self.frame = frame

    def read(self):
        ret, frame = self.frame is not None, self.frame
        self.frame = None
        return ret, frame

    def release(self):
        self.streaming = False
        self.cap.release()


class CV2_Listener(object):
    STREAMING_PORT = 11112

    def __init__(self, width=1920, height=1080, port=None, with_buffer=True, app_ip=None):
        self.width = width
        self.height = height
        self.streaming = False
        self.with_buffer = with_buffer
        self.app_ip = app_ip
    
    def isStreaming(self):
        return self.streaming

    def start(self):
        cap_str = "tcp://%s:%s" % (self.app_ip, CV2_Listener.STREAMING_PORT)
        if self.with_buffer:
            self.cap = cv2.VideoCapture(cap_str)
        else:
            self.cap = VideoCaptureWithoutBuffer(cv2.VideoCapture(cap_str))
        self.streaming = True

    def getFrame(self):
        ret, frame = self.cap.read()
        return None if self.cap is None or not ret else cv2.resize(frame, (self.width, self.height), interpolation = cv2.INTER_AREA)

    def stop(self):
        self.cap.release()
        self.streaming = False

    def getVideoCapture(self):
        return self.cap

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.width
