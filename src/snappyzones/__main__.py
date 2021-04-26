#! /usr/bin/python3

from .cmd_reader import reader
from .service import Service
from .builder import ZoneBuilder
from .process import (
    launch_background_process, 
    stop_background_process
)
from .conf.keybinding_service import KeybindingService

ZONES = "zones"
KEYFINDER = "keyfinder"

def main():
    cmd, args, kwargs = reader()
    if not any([cmd, args, kwargs]):
        service = Service()
        service.listen()
    
    if cmd == "config":
        _config_menu(*args, **kwargs)

    elif cmd == "start":
        launch_background_process(*args, **kwargs)

    elif cmd == "stop":
        stop_background_process()

def _config_menu(*args, **kwargs):
    if ZONES in args:
        zb = ZoneBuilder(*args, **kwargs)
        zb.main()

    elif KEYFINDER in args:
        kf = KeybindingService()
        kf.listen()
    
if __name__ == "__main__":
    main()
