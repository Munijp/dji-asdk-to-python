import cv2.aruco as aruco
import itertools
import numpy as np
import cv2
import time
import math
import threading
import sys
from fps_limiter import LimitFPS
from dji_asdk_to_python.errors import CustomError
from dji_asdk_to_python.flight_controller.virtual_stick.flight_control_data import FlightControlData
from dji_asdk_to_python.flight_controller.flight_controller_state import FlightControllerState
from dji_asdk_to_python.camera.exposure_mode import ExposureMode
from dji_asdk_to_python.camera.iso import ISO
from dji_asdk_to_python.camera.shutter_speed import ShutterSpeed
from dji_asdk_to_python.utils.FPS import FPS
from dji_asdk_to_python.flight_controller.virtual_stick.control_mode import (
    VerticalControlMode
)
# This file is part of IvPID.
# Copyright (C) 2015 Ivmech Mechatronics Ltd. <bilgi@ivmech.com>
#
# IvPID is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IvPID is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# title           :PID.py
# description     :python pid controller
# author          :Caner Durmusoglu
# date            :20151218
# version         :0.1
# notes           :
# python_version  :2.7
# ==============================================================================


"""Ivmech PID Controller is simple implementation of a Proportional-Integral-Derivative (PID) Controller in the Python Programming Language.
More information about PID Controller: http://en.wikipedia.org/wiki/PID_controller
"""


class PID:
    """PID Controller
    """

    def __init__(self, P=0.2, I=0.0, D=0.0, current_time=None):

        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.sample_time = 0.00
        self.current_time = current_time if current_time is not None else time.time()
        self.last_time = self.current_time

        self.clear()

    def clear(self):
        """Clears PID computations and coefficients"""
        self.SetPoint = 0.0

        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0

        # Windup Guard
        self.int_error = 0.0
        self.windup_guard = 20.0

        self.output = 0.0

    def update(self, feedback_value, current_time=None):
        """Calculates PID value for given reference feedback
        .. math::
            u(t) = K_p e(t) + K_i \\int_{0}^{t} e(t)dt + K_d {de}/{dt}
        .. figure:: images/pid_1.png
           :align:   center
           Test PID with Kp=1.2, Ki=1, Kd=0.001 (test_pid.py)
        """
        error = self.SetPoint - feedback_value

        self.current_time = current_time if current_time is not None else time.time()
        delta_time = self.current_time - self.last_time
        delta_error = error - self.last_error

        if (delta_time >= self.sample_time):
            self.PTerm = self.Kp * error
            self.ITerm += error * delta_time

            if (self.ITerm < -self.windup_guard):
                self.ITerm = -self.windup_guard
            elif (self.ITerm > self.windup_guard):
                self.ITerm = self.windup_guard

            self.DTerm = 0.0
            if delta_time > 0:
                self.DTerm = delta_error / delta_time

            # Remember last time and last error for next calculation
            self.last_time = self.current_time
            self.last_error = error

            self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)

    def setKp(self, proportional_gain):
        """Determines how aggressively the PID reacts to the current error with setting Proportional Gain"""
        self.Kp = proportional_gain

    def setKi(self, integral_gain):
        """Determines how aggressively the PID reacts to the current error with setting Integral Gain"""
        self.Ki = integral_gain

    def setKd(self, derivative_gain):
        """Determines how aggressively the PID reacts to the current error with setting Derivative Gain"""
        self.Kd = derivative_gain

    def setWindup(self, windup):
        """Integral windup, also known as integrator windup or reset windup,
        refers to the situation in a PID feedback controller where
        a large change in setpoint occurs (say a positive change)
        and the integral terms accumulates a significant error
        during the rise (windup), thus overshooting and continuing
        to increase as this accumulated error is unwound
        (offset by errors in the other direction).
        The specific problem is the excess overshooting.
        """
        self.windup_guard = windup

    def setSampleTime(self, sample_time):
        """PID that should be updated at a regular interval.
        Based on a pre-determined sampe time, the PID decides if it should compute or return immediately.
        """
        self.sample_time = sample_time


"""
This demo calculates multiple things for different scenarios.
IF RUNNING ON A PI, BE SURE TO sudo modprobe bcm2835-v4l2
Here are the defined reference frames:
TAG:
                A y
                |
                |
                |tag center
                O---------> x
CAMERA:
                X--------> x
                | frame center
                |
                |
                V y
F1: Flipped (180 deg) tag frame around x axis
F2: Flipped (180 deg) camera frame around x axis
The attitude of a generic frame 2 respect to a frame 1 can obtained by calculating euler(R_21.T)
We are going to obtain the following quantities:
    > from aruco library we obtain tvec and Rct, position of the tag in camera frame and attitude of the tag
    > position of the Camera in Tag axis: -R_ct.T*tvec
    > Transformation of the camera, respect to f1 (the tag flipped frame): R_cf1 = R_ct*R_tf1 = R_cf*R_f
    > Transformation of the tag, respect to f2 (the camera flipped frame): R_tf2 = Rtc*R_cf2 = R_tc*R_f
    > R_tf1 = R_cf2 an symmetric = R_f
"""


class ArucoSingleTracker:
    def __init__(self, camera_matrix, camera_distortion):

        self._camera_matrix = camera_matrix
        self._camera_distortion = camera_distortion

        # --- 180 deg rotation matrix around the x axis
        self._R_flip = np.zeros((3, 3), dtype=np.float32)
        self._R_flip[0, 0] = 1.0
        self._R_flip[1, 1] = -1.0
        self._R_flip[2, 2] = -1.0

        # --- Define the aruco dictionary
        self._aruco_dict = aruco.custom_dictionary_from(
            20, 4, aruco.getPredefinedDictionary(aruco.DICT_4X4_100)
        )

        self._parameters = aruco.DetectorParameters_create()

    def _rotationMatrixToEulerAngles(self, R):
        # Calculates rotation matrix to euler angles
        # The result is the same as MATLAB except the order
        # of the euler angles ( x and z are swapped ).

        def isRotationMatrix(R):
            Rt = np.transpose(R)
            shouldBeIdentity = np.dot(Rt, R)
            I = np.identity(3, dtype=R.dtype)
            n = np.linalg.norm(I - shouldBeIdentity)
            return n < 1e-6

        assert isRotationMatrix(R)

        sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

        singular = sy < 1e-6

        if not singular:
            x = math.atan2(R[2, 1], R[2, 2])
            y = math.atan2(-R[2, 0], sy)
            z = math.atan2(R[1, 0], R[0, 0])
        else:
            x = math.atan2(-R[1, 2], R[1, 1])
            y = math.atan2(-R[2, 0], sy)
            z = 0

        return np.array([x, y, z])

    def track(
        self, frame, id_to_find=None, marker_size=None,
    ):

        marker_found = False
        x = y = z = pitch_camera = x_camera = y_camera = z_camera = 0

        # -- Convert in gray scale
        gray = cv2.cvtColor(
            frame, cv2.COLOR_BGR2GRAY
        )  # -- remember, OpenCV stores color images in Blue, Green, Red

        # -- Find all the aruco markers in the image
        corners, ids, rejected = aruco.detectMarkers(
            image=gray,
            dictionary=self._aruco_dict,
            parameters=self._parameters,
            cameraMatrix=self._camera_matrix,
            distCoeff=self._camera_distortion,
        )
        pitch_marker, roll_marker, yaw_marker = None, None, None
        pitch_camera, roll_camera, yaw_camera = None, None, None

        planned_ids = []
        if ids is not None:
            planned_ids = list(itertools.chain(*ids))
        if id_to_find in planned_ids:
            index_id_to_find = planned_ids.index(id_to_find)
            marker_found = True
            # -- array of rotation and position of each marker in camera frame
            # -- rvec = [[rvec_1], [rvec_2], ...]    attitude of the marker respect to camera frame
            # -- tvec = [[tvec_1], [tvec_2], ...]    position of the marker in camera frame
            rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(
                corners, marker_size, self._camera_matrix, self._camera_distortion
            )

            # -- Unpack the output
            rvec, tvec = rvecs[index_id_to_find][0], tvecs[index_id_to_find][0]

            x = tvec[0]
            y = tvec[1]
            z = tvec[2]

            # -- Obtain the rotation matrix tag->camera
            R_ct = np.matrix(cv2.Rodrigues(rvec)[0])
            R_tc = R_ct.T

            # -- Get the attitude in terms of euler 321 (Needs to be flipped first)
            (
                roll_marker,
                pitch_marker,
                yaw_marker,
            ) = self._rotationMatrixToEulerAngles(self._R_flip * R_tc)

            # -- Now get Position and attitude f the camera respect to the marker
            pos_camera = -R_tc * np.matrix(tvec).T
            x_camera = pos_camera[0]
            y_camera = pos_camera[1]
            z_camera = pos_camera[2]

            (
                roll_camera,
                pitch_camera,
                yaw_camera,
            ) = self._rotationMatrixToEulerAngles(self._R_flip * R_tc)

        if yaw_marker is None:
            marker_found = False
            yaw_marker = 0

        if marker_found:
            roll_camera = math.degrees(roll_camera)
            yaw_camera = math.degrees(yaw_camera)
            pitch_camera = math.degrees(pitch_camera)
            roll_marker = math.degrees(roll_marker)
            yaw_marker = math.degrees(yaw_marker)
            pitch_marker = math.degrees(pitch_marker)
            x_camera = float(x_camera)
            y_camera = float(y_camera)
            z_camera = float(z_camera)

        result = (
            marker_found,
            x,
            y,
            z,
            x_camera,
            y_camera,
            z_camera,
            roll_marker,
            yaw_marker,
            pitch_marker,
            roll_marker,
            roll_camera,
            yaw_camera,
            pitch_camera,
        )
        return result


class ArucoLanding:
    LANDING_CM = 270
    SECONDS_BEFORE_GET_UP = 10
    MAX_SECONDS_GETTING_LANDING = 15
    X_Y_CM_ERROR_ALLOWED = 12
    YAW_ERROR_ALLOWED = 15
    """
    Inits aruco precision landing
        Parameters:
        drone_ip (str) -> The IP of the drone
        camera_matrix (ndarray) -> The camera matrix of the drone's camera
        camera_distortion (ndarray) -> The camera distortion of the drone's camera
        marker_id (int) -> The ID of the aruco marker to be detected on the landing stage
        marker_size_cm (int) -> The size in CM of the aruco marker to be detected in the stage
    """

    def resetPid(self):
        self.p = 0.004
        self.i = 0.000005
        self.d = 0.0005

        self.pidx = PID(P=self.p, I=self.i, D=self.d)
        self.pidy = PID(P=self.p, I=self.i, D=self.d)
        self.pidz = PID(P=self.p, I=self.i, D=self.d)

        self.pidx.SetPoint = 0.0
        self.pidy.SetPoint = 15.0
        self.pidz.SetPoint = ArucoLanding.LANDING_CM / 1.2

        self.pidx.setSampleTime(0.1)
        self.pidy.setSampleTime(0.1)
        self.pidz.setSampleTime(0.1)

    def __init__(self, aircraft, marker_id, marker_size_cm, width, height, camera_matrix, camera_distortion):
        self.aircraft = aircraft
        self.cv2_manager = self.aircraft.getLiveStreamManager().getCV2Manager(with_buffer=True)
        self.cv2_manager.setWidth(width)
        self.cv2_manager.setHeigth(height)

        self.marker_id = marker_id
        self.marker_size_cm = marker_size_cm
        self.ast = ArucoSingleTracker(camera_distortion=camera_distortion, camera_matrix=camera_matrix)
        self.resetPid()

        self.running = True
        t2 = threading.Thread(target=self.revive_virtual_stick, args=[])
        t2.start()

    def revive_virtual_stick(self):
        fc = self.aircraft.getFlightController()
        while self.running:
            fc.setVirtualStickModeEnabled(True)
            time.sleep(1)

    def camera_iso_setup(self, camera, cameraType):

        camera.setExposureMode(ExposureMode.MANUAL)

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
        else:
            camera.setExposureMode(ExposureMode.PROGRAM)


    def start(self, is_night):
        result = self.cv2_manager.startStream()
        if isinstance(result, CustomError):
            raise Exception("%s" % result)

        gimbal = self.aircraft.getGimbal()
        gimbal.rotate(-90, 0, 0)

        fc = self.aircraft.getFlightController()
        fc.setVirtualStickModeEnabled(True)
        fcd = FlightControlData()
        fc.setCollisionAvoidanceEnabled(False)
        fc.setVerticalControlMode(VerticalControlMode.VELOCITY)

        camera = self.aircraft.getCamera()

        print("LANDING IS NIGHT", is_night)

        
        camera.setExposureMode(ExposureMode.MANUAL)

        cameraTypeSettings = ["DAY_VERY_SUNNY","DAY_SUNNY","DAY_AFTERNOON","EVENING","MORNING","PROGRAM"]
        #cameraTypeSettings = ["DAY_SUNNY","DAY_AFTERNOON"]
        # if is_night:
        #     camera.setExposureMode(ExposureMode.PROGRAM)
        #     camera.setISO(ISO.ISO_100)
        # else:
        #     camera.setExposureMode(ExposureMode.MANUAL)
        #     camera.setISO(ISO.ISO_800)
        #     camera.setShutterSpeed(ShutterSpeed.SHUTTER_SPEED_1_8000)

        start = time.perf_counter()
        last_z = sys.maxsize
        fps = FPS()
        fps_limiter = LimitFPS(fps=15)
        i = 0
        isoCountChanger = 0
        maxChance = 0
        rightIso = False
        self.camera_iso_setup(camera, cameraTypeSettings[i])
        while True:
            end = time.perf_counter()
            fcd.setPitch(0)
            fcd.setYaw(0)
            fcd.setRoll(0)
            fcd.setVerticalThrottle(0)

            frame = self.cv2_manager.getFrame()
            if maxChance <= 100:
                maxChance = maxChance+1

            if frame is None:
                print("FRAME IS NONE")
                result = self.cv2_manager.startStream()
                continue
            (
                marker_found,
                x_marker,
                y_marker,
                z_marker,
                x_camera,
                y_camera,
                z_camera,
                roll_marker,
                yaw_marker,
                pitch_marker,
                roll_marker,
                roll_camera,
                yaw_camera,
                pitch_camera,
            ) = self.ast.track(frame, self.marker_id, self.marker_size_cm)

            print("1 PRE MARKER FOUND")

            if marker_found:
                print("2 MARKER FOUND")

                if not rightIso:
                    isoCountChanger = isoCountChanger+1
                    if isoCountChanger >= 90:
                        print("FOUND RIGHT ISO")
                        rightIso = True

                if not fps_limiter():
                    print("3  FPS LIMITER YES")
                    continue
                fps_ = float(fps())
                try:
                    sample_time = 1/float(fps_)
                except:
                    sample_time = 0.1
                print("4 FPS marker detection %s" % (fps_))
                print("x %s y %s z %s yaw %s" % (x_marker, y_marker, z_marker, yaw_camera))

                start = time.perf_counter()
                last_z = z_marker

                if abs(yaw_camera) > 5:
                    if yaw_camera < 0:
                        fcd.setYaw((abs(yaw_camera) / 10) * 1.5)
                    else:
                        fcd.setYaw(-(abs(yaw_camera) / 10) * 1.5)

                self.pidx.update(x_marker)
                self.pidy.update(y_marker)

                xoutput = self.pidx.output
                youtput = self.pidy.output

                fcd.setPitch(youtput)
                fcd.setRoll(xoutput * -1)

                if z_marker > (ArucoLanding.LANDING_CM / 1.5) and abs(yaw_camera) < ArucoLanding.YAW_ERROR_ALLOWED:
                    self.pidz.update(z_marker)
                    zoutput = self.pidz.output
                    fcd.setVerticalThrottle(max(min(-0.4, -abs(zoutput) / 4), -2))

                if z_marker < ArucoLanding.LANDING_CM and abs(yaw_camera) < ArucoLanding.YAW_ERROR_ALLOWED and math.sqrt(math.pow(x_marker - self.pidx.SetPoint, 2) + math.pow(y_marker - self.pidy.SetPoint, 2)) < ArucoLanding.X_Y_CM_ERROR_ALLOWED:
                    fc.startLanding()

                    fps_limiter_aux = LimitFPS(fps=15)
                    landing_done = False
                    while True:
                        if fps_limiter_aux():

                            flight_controller_state = fc.getState()

                            if not isinstance(flight_controller_state, FlightControllerState):
                                continue

                            if flight_controller_state.isLandingConfirmationNeeded():
                                print("Confirm Landing...")
                                fc.confirmLanding()

                            flying = flight_controller_state.isFlying()

                            if flying is not None and not flying:
                                landing_done = True
                                break

                            if fps_limiter_aux.get_elapsed_seconds() > ArucoLanding.MAX_SECONDS_GETTING_LANDING:
                                break

                    if landing_done:
                        # Reset camera settings
                        camera.setExposureMode(ExposureMode.PROGRAM)
                        fc.setCollisionAvoidanceEnabled(True)
                        self.running = False
                        break

                    gimbal.rotate(-90, 0, 0)
                    fc.setVirtualStickModeEnabled(True)
                fc.sendVirtualStickFlightControlData(fcd)
                fcd.setPitch(0)
                fcd.setYaw(0)
                fcd.setRoll(0)
                fcd.setVerticalThrottle(0)
            else:
                print("2 MARKER NOT FOUND")

                if last_z < ArucoLanding.LANDING_CM and (end - start) > ArucoLanding.SECONDS_BEFORE_GET_UP:
                    fc.setVirtualStickModeEnabled(True)
                    fc.move_distance(pitch_distance=0, roll_distance=0, throttle_distance=2, meters_per_second=0.3, order=["THROTTLE", "ROLL", "PITCH"])
                    gimbal.rotate(-90, 0, 0)
                    self.resetPid()
                    end = time.perf_counter()
                    start = time.perf_counter()
                
                flight_controller_state = fc.getState()
                flying = flight_controller_state.isFlying()
                if flying is not None and flying and not rightIso and maxChance > 100:
                    print("FINDING NEW ISO")
                    maxChance = 0
                    isoCountChanger = 0
                    i = i+1
                    if i < len(cameraTypeSettings):
                        self.camera_iso_setup(camera, cameraTypeSettings[i])
                    else:
                        i = 0
                        self.camera_iso_setup(camera, cameraTypeSettings[i])



                if flying is not None and not flying:
                    camera.setExposureMode(ExposureMode.PROGRAM)
                    fc.setCollisionAvoidanceEnabled(True)
                    self.running = False
                    break
        gimbal.rotate(0, 0, 0)
