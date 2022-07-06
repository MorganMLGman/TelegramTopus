from enum import Enum
from datetime import datetime
import time
import psutil

class HostSystem(Enum):
    FEDORA = 0
    UBUNTU = 1
    RASPBIAN = 2
    WINDOWS = 3

class Commands:
    def __init__(self, host: HostSystem) -> None:
        if host in HostSystem:
            self.__host_system = host
        else:
            raise KeyError(f"{host} not found in Host_System enum")
 
    def get_time() -> datetime:
        return datetime.now()

    def get_uptime() -> tuple[str, float]:
        boot_time = psutil.boot_time()
        uptime = time.time() - boot_time
        boot_time_str = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

        return boot_time_str, uptime

    def get_load() -> tuple[float, float, float]:
        load = [x / psutil.cpu_count() * 100.0 for x in psutil.getloadavg()]
        return load[0], load[1], load[2]

    def get_temp() -> dict:
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