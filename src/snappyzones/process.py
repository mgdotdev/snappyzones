import os
import signal
import sys

from .service import Service
from .conf.settings import SETTINGS


def _check_pid(pid): 
    if not pid:
        return False       
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def launch_background_process(*args, **kwargs):
    # if there is a process already running, kill it
    _pid = SETTINGS.pid
    if _check_pid(_pid):
        print("background Snappy Zones process found: killing process...")
        stop_background_process(_pid)
        
    print("starting...")
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        print(sys.stderr, f"FORK FAILED: {e.errno} ({e.strerror})")
        sys.exit(1)

    pid = str(os.getpid())
    SETTINGS.pid = pid
    print(f"started PID: {pid}")
    service = Service()
    service.listen()
    

def stop_background_process(pid=None):
    if not pid:
        pid = SETTINGS.pid
    if _check_pid(pid):
        print(f"stopping...")
        os.kill(pid, signal.SIGTERM)
        print(f"stopped PID: {pid}")
        os.remove(SETTINGS._pid_file)
    else:
        print(
            "No background process was found. "
            "no action will be taken."
        )

