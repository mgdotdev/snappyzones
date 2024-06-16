#! /usr/bin/python3
import logging

from .cmd_reader import reader
from .service import Service
from .builder import ZoneBuilder
from .process import launch_background_process, stop_background_process
from .conf.keybinding_service import KeybindingService

logger = logging.getLogger(__name__)

ZONES = "zones"
KEYFINDER = "keyfinder"


def main():
    logger.info("SnappyZones startup")
    cmd, args, kwargs = reader()
    wm = _get_window_manager()
    logger.info("Window manager is %s", wm)
    if not any([cmd, args, kwargs]):
        service = Service(window_manager=wm)
        service.listen()

    if cmd == "config":
        _config_menu(*args, **kwargs)

    elif cmd == "start":
        launch_background_process(*args, **kwargs)

    elif cmd == "stop":
        stop_background_process()

    logger.info("SnappyZones finished")

def _config_menu(*args, **kwargs):
    if ZONES in args:
        zb = ZoneBuilder(*args, **kwargs)
        zb.main()

    elif KEYFINDER in args:
        print("Press Ctrl+C to quit.")
        kf = KeybindingService()
        kf.listen()

def _get_window_manager() -> str:
    with open("/etc/X11/default-display-manager", encoding="utf-8") as f:
        if "gdm3" in f.readline():
            return "gdm3"
    with open ("/etc/sysconfig/desktop", encoding="utf-8") as f:
        if "gdm3" in f.readline():
            return "gdm3"
    with open ("/etc/sysconfig/displaymanager", encoding="utf-8") as f:
        if "gdm3" in f.readline():
            return "gdm3"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
