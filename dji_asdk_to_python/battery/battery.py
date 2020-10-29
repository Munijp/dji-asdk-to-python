from dji_asdk_to_python.utils.message_builder import MessageBuilder

from dji_asdk_to_python.utils.shared import checkParameters
from dji_asdk_to_python.utils.socket_utils import SocketUtils
from dji_asdk_to_python.battery.battery_state import BatteryState


class Battery:
    """
    This class manages information and real-time status of the connected product's batteries. This object is available from the Aircraft object.
    """

    def __init__(self, app_ip):
        """
        Args:
            - app_ip (str): Android device ip
        """
        self.app_ip = app_ip
        self._state_callbacks = {}

    def getBatteryState(self, callback=None, timeout=10):
        """
        Returns:
            [BatteryState]: the current state of battery.
        """

        checkParameters(callback=callback, method_name="BatteryState", timeout=timeout)

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.GET_BATTERY_STATE,
            message_class=MessageBuilder.BATTETY,
            message_data=None,
        )

        return_type = BatteryState

        blocking = callback is None

        return SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            callback=callback,
            timeout=timeout,
            return_type=return_type,
            blocking=blocking,
        )
