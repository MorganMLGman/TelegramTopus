from enum import Enum
import psutil
from datetime import datetime
import time
import psutil

class Host_System(Enum):
        FEDORA = 0,
        UBUNTU = 1,
        RASPBIAN = 2,
        WINDOWS = 3

class Commands:   
    def __init__(self, host: Host_System) -> None:
        if host in Host_System:
            self.__host_system = host
        else:
            raise KeyError(f"{host} not found in Host_System enum")  
        
    def get_time():
        return datetime.now()
    
    def get_uptime() -> tuple[str, float]:
        bootTime = psutil.boot_time()
        uptime = time.time() - bootTime        
        bootTimeStr = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        
        return bootTimeStr, uptime
                
                
            
                