#! /usr/bin/python3

from .cmd_reader import reader
from .service import Service
from .builder import ZoneBuilder
from .process import (
    launch_background_process, 
    stop_background_process
)

def main():
    cmd, args, kwargs = reader()
    if not any([cmd, args, kwargs]):
        service = Service()
        service.listen()
    
    if cmd == ["config"]:
        zb = ZoneBuilder(*args, **kwargs)
        zb.main()

    elif cmd == ["start"]:
        launch_background_process(*args, **kwargs)

    elif cmd == ["stop"]:
        stop_background_process()

    
if __name__ == "__main__":
    main()
