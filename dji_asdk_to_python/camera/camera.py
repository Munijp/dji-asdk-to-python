from dji_asdk_to_python.utils.message_builder import MessageBuilder
from dji_asdk_to_python.errors import DJIError

from dji_asdk_to_python.utils.shared import checkParameters
from dji_asdk_to_python.utils.socket_utils import SocketUtils
from dji_asdk_to_python.camera.ExposureMode import ExposureMode


class Camera:
    """
        This class contains the media manager and playback manager, which manage the camera's media content. It provides methods to change camera settings and perform camera actions.This object is available from the Aircraft object.
    """

    def __init__(self, app_ip):
        """
        Args:
            - app_ip (str): Android device ip
        """
        self.app_ip = app_ip
        self._state_callbacks = {}

    # -------------------------------- EXPOSURE & WHITE BALANCE ------------------------------------

    def getExposureMode(self, callback=None, timeout=10):
        """
            Gets the camera's exposure mode.
        """

        checkParameters(callback=callback, method_name="getExposureMode", timeout=timeout)

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.GET_EXPOSURE_MODE,
            message_class=MessageBuilder.CAMERA,
            message_data=None,
        )

        return_type = ExposureMode

        blocking = callback is None

        return SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            callback=callback,
            timeout=timeout,
            return_type=return_type,
            blocking=blocking,
        )

    def setExposureMode(self, mode, callback=None, timeout=10):
        """
            Sets the camera's exposure mode.

            Check ExposureMode to view all possible camera exposure modes.
            Please note that in different exposure mode, it will have different
            values for the same setting.

            Args:
                - callback (function): The execution callback with the returned execution result.
                - mode (ExposureMode): 	Camera exposure mode to set.
        """
        checkParameters(
            callback=callback, method_name="setExposureMode", timeout=timeout,
        )

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.SET_HOME_LOCATION,
            message_class=MessageBuilder.CAMERA,
            message_data={"mode": mode},
        )

        return_type = DJIError

        blocking = callback is None

        return SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            callback=callback,
            timeout=timeout,
            return_type=return_type,
            blocking=blocking,
        )

    def getISO(self, callback=None, timeout=10):
        """
            Gets the camera's ISO value.
        """

        checkParameters(callback=callback, method_name="getExposureMode", timeout=timeout)

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.GET_ISO,
            message_class=MessageBuilder.CAMERA,
            message_data=None,
        )

        return_type = ISO

        blocking = callback is None

        return SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            callback=callback,
            timeout=timeout,
            return_type=return_type,
            blocking=blocking,
        )
