import os
import signal
import sys

from functools import lru_cache

from .service import Service


HERE = os.path.abspath(os.path.dirname(__file__))
PID_FILE = os.path.join(HERE, '.pid')


def _file_pid():
    if os.path.isfile(PID_FILE):
        with open(PID_FILE, 'r') as f:
            pid = int(f.read())
        return pid
    return None


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
    _pid = _file_pid()
    if _check_pid(_pid):
        print("Background Snappy Zones process found: killing process...")
        stop_background_process(_pid)
        
    print("STARTING...")
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        print(sys.stderr, f"FORK FAILED: {e.errno} ({e.strerror})")
        sys.exit(1)

    pid = str(os.getpid())

    with open(os.path.join(HERE, '.pid'), 'w') as f:
        f.write(pid)

    print(f"STARTED PID: {pid}")
    service = Service()
    service.listen()
    

def stop_background_process(pid=None):
    if not pid:
        pid = _file_pid()
    if _check_pid(pid):
        print(f"STOPPING...")
        os.kill(pid, signal.SIGTERM)
        print(f"STOPPED PID: {pid}")
        os.remove(PID_FILE)
    else:
        print(
            "No background process was found. "
            "no action will be taken."
        )

