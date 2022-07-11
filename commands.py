""" commands.py - containst generic implementation of functions, not Telegram releated"""
from enum import Enum
from datetime import datetime
import time
import psutil

class HostSystem(Enum):
    """HostSystem class containing type of OS bot is run at"""
    FEDORA = 0
    UBUNTU = 1
    RASPBIAN = 2
    WINDOWS = 3

class Commands:
    """ Commands class contains definition of generic functions, functions would need to be
    wrapped in bot_commands.py file to become usable in telegram bot
    """

    host_system = None

    def __init__(self, host: HostSystem) -> None:
        """__init__ constructor

        Args:
            host (HostSystem): type of system bot is run at

        Raises:
            KeyError: provided value not found in HostSystem class
        """
        if host in HostSystem:
            self.host_system = host
        else:
            raise KeyError(f"{host} not found in Host_System enum")

    @staticmethod
    def get_time() -> datetime:
        """get_time Basic fucntion to get server local time

        Returns:
            datetime: server local time
        """
        return datetime.now()

    @staticmethod
    def get_uptime() -> tuple[str, float]:
        """get_uptime Basic function to get server uptime

        Returns:
            tuple[str, float]: Returns formated string representing boot time and also float value
            representing second since boot time
        """
        boot_time = psutil.boot_time()
        uptime = time.time() - boot_time
        boot_time_str = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        return boot_time_str, uptime

    @staticmethod
    def get_load() -> tuple[float, float, float]:
        """get_load Basic function to get average system load,
        on Linux machine it will use "load" and on Windows average CPU
        usage over last 10 seconds

        Returns:
            tuple[float, float, float]: Average load after 1m, 5m and 15m,
            on windows only first value is valid
        """
        if psutil.WINDOWS:
            cpu_load = psutil.cpu_percent(10.0, False)
            return cpu_load, None, None
        if psutil.LINUX:
            load = [x / psutil.cpu_count() * 100.0 for x in psutil.getloadavg()]
            return load[0], load[1], load[2]
        return None, None, None

    @staticmethod
    def get_temp() -> dict:
        """get_temp Function to read temperature of various components of PC,
        only available on Linux

        Returns:
            dict: Returns dict of all read values or None if run on non linux environment
        """
        if psutil.LINUX:
            temps = psutil.sensors_temperatures()
            if temps:
                ret = {}
                for key, val in temps.items():
                    if "wifi" in key.lower() or "wireless" in key.lower():
                        ret["wifi_card"] = val[0].current
                    elif "nvme" in key.lower():
                        ret["nvme_disk"] = val[0].current
                    elif "core" in key.lower():
                        core = {}
                        for item in val:
                            core[item.label] = item.current
                        ret["cpu"] = core
                return ret
        return None
