import os
import signal
import sys

from .service import Service


HERE = os.path.abspath(os.path.dirname(__file__))


def launch_background_process(*args, **kwargs):
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
    

def stop_background_process(*args, **kwargs):
    with open(os.path.join(HERE, '.pid'), 'r') as f:
        pid = int(f.read())
    print(f"STOPPING...")
    os.kill(pid, signal.SIGTERM)
    print(f"STOPPED PID: {pid}")

