from contextlib import closing
import socket
import numpy as np
import random
import string

import os
on_rtd = os.environ.get('READTHEDOCS') == 'True'
if not on_rtd:
    import cv2

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('localhost', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port = s.getsockname()[1]
        return port


class CV2_Listener(object):
    def __init__(self, width=1920, height=1080, port=None):
        self.width = width
        self.height = height
        self.streaming = False

        if port is None:
            self.port = find_free_port()
        else:
            self.port = port

        self.gst_str = ('udpsrc port={} caps="application/x-rtp, encoding-name=(string)H264" ! '
               'queue ! rtph264depay ! queue ! h264parse ! omxh264dec ! '
               'nvvidconv ! '
               'video/x-raw, '
               'format=(string)BGRx ! '
               'videoconvert ! appsink').format(self.port)


    def start(self):
        self.cap = cv2.VideoCapture(self.gst_str, cv2.CAP_GSTREAMER)
        self.streaming = True

    def getFrame(self):
        ret, frame = self.cap.read()
        return None if self.cap is None or not ret else cv2.resize(frame, (self.width, self.height), interpolation = cv2.INTER_AREA)

    def stop(self):
        self.cap.release()
        self.streaming = False

