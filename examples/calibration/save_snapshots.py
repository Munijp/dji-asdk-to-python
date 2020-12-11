"""
Saves a series of snapshots with the current camera as <name>_<width>_<height>_<nnn>.jpg

Usage example:
    python examples/calibration/save_snapshots.py --app_ip 192.168.100.206 --folder ./examples/calibration/images --dwidth 1280 --dheight 720 --name apolo

Buttons:
    q           - quit
    space bar   - save the snapshot

"""

import cv2
import time
import sys
import argparse
import os

from dji_asdk_to_python.products.aircraft import Aircraft
from dji_asdk_to_python.errors import CustomError


def save_snaps(width=0, height=0, name="snapshot", folder=".", app_ip=None):
    aircraft = Aircraft(app_ip)
    streaming_manager = aircraft.getLiveStreamManager()
    cv2_manager = streaming_manager.getCV2Manager()
    cv2_manager.setWidth(width)
    cv2_manager.setHeigth(height)
    cv2_manager.set_stream_id("calibration")
    result = cv2_manager.startStream()
    print("result startStream %s" % result)

    if isinstance(result, CustomError):
        raise Exception("%s" % result)

    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
            # ----------- CREATE THE FOLDER -----------------
            folder = os.path.dirname(folder)
            try:
                os.stat(folder)
            except:
                os.mkdir(folder)
    except:
        pass

    nSnap = 0
    w = width
    h = height

    fileName = "%s/%s_%d_%d_" % (folder, name, w, h)
    cv2.namedWindow("output", cv2.WINDOW_NORMAL)
    while True:
        frame = cv2_manager.getFrame()

        if frame is None:
            continue

        cv2.imshow('output', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord(' '):
            print("Saving image ", nSnap)
            frame = cv2.resize(frame, (w, h))
            cv2.imwrite("%s%d.jpg" % (fileName, nSnap), frame)
            nSnap += 1

    cv2.destroyAllWindows()
    cv2_manager.stopStream()


def main():
    # ---- DEFAULT VALUES ---
    SAVE_FOLDER = "."
    FILE_NAME = "snapshot"
    APP_IP = "192.168.100.206"
    FRAME_WIDTH = 1280
    FRAME_HEIGHT = 720

    # ----------- PARSE THE INPUTS -----------------
    parser = argparse.ArgumentParser(
        description="Saves snapshot from DJI drone. \n q to quit \n spacebar to save the snapshot")
    parser.add_argument("--folder", default=SAVE_FOLDER, help="Path to the save folder (default: current)")
    parser.add_argument("--name", default=FILE_NAME, help="Picture file name (default: snapshot)")
    parser.add_argument("--app_ip", default=APP_IP, help="App ip (default: 192.168.100.206)")
    parser.add_argument("--dwidth", default=FRAME_WIDTH, type=int, help="<width> px (default 1280)")
    parser.add_argument("--dheight", default=FRAME_HEIGHT, type=int, help="<height> px (default 720)")
    args = parser.parse_args()

    SAVE_FOLDER = args.folder
    FILE_NAME = args.name
    FRAME_WIDTH = args.dwidth
    FRAME_HEIGHT = args.dheight
    APP_IP = args.app_ip

    save_snaps(width=args.dwidth, height=args.dheight, name=args.name, folder=args.folder, app_ip=APP_IP)

    print("Files saved")


if __name__ == "__main__":
    main()
