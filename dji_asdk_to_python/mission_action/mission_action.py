import socket
from dji_asdk_to_python.utils.message_builder import MessageBuilder
from dji_asdk_to_python.utils.shared import checkParameters
from dji_asdk_to_python.utils.socket_utils import SocketUtils
from dji_asdk_to_python.utils.process_message import DJIError


class MissionAction:
    """
    Base class for all Mission Control Timeline based actions.
    """

    def __init__(self, app_ip):
        """
        Args:
            - app_ip (str): Android device ip
        """
        self.app_ip = app_ip
        self._state_callbacks = {}
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def goToAction(self, coordinate, altitude, callback=None, timeout=10):
        """
        Go to the specified coordinate and altitude (in meters) from the current aircraft position.
        """

        checkParameters(callback=callback, method_name="goToAction", timeout=timeout)

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.GO_TO_ACTION,
            message_class=MessageBuilder.MISSION_ACTION,
            message_data={"coordinate": coordinate.__dict__, "altitude": altitude},
        )

        return_type = DJIError

        blocking = callback is None

        return SocketUtils.send(
            socket_obj=self.socket_obj,
            message=message,
            app_ip=self.app_ip,
            callback=callback,
            timeout=timeout,
            return_type=return_type,
            blocking=blocking,
        )

    def aircraftYawAction(self, angle, isAbsolute, callback=None, timeout=10):
        """
        Initialize with a yaw angle relative to current heading or absolute heading against true north.
        The range of angle is [-180, 180]. This initializer should be preferred when accuracy of the angle
        is more of a priority than smooth yaw movement.
        """

        checkParameters(callback=callback, method_name="aircraftYawAction", timeout=timeout)

        is_absolute_str = "true" if isAbsolute else "false"
        message = MessageBuilder.build_message(
            message_method=MessageBuilder.AIRCRAFT_YAW_ACTION,
            message_class=MessageBuilder.MISSION_ACTION,
            message_data={"angle": angle, "isAbsolute": is_absolute_str},
        )

        return_type = DJIError

        blocking = callback is None

        return SocketUtils.send(
            socket_obj=self.socket_obj,
            message=message,
            app_ip=self.app_ip,
            callback=callback,
            timeout=timeout,
            return_type=return_type,
            blocking=blocking,
        )
