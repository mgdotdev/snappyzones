import json
import os
import sys
import threading

from Xlib import X
from Xlib.display import Display
from Xlib.error import ConnectionClosedError

from .process import _check_pid, launch_background_process
from .snap import active_window
from .conf.settings import SETTINGS

HERE = os.path.abspath(os.path.dirname(__file__))


def _get_recursive(obj, args, default=None):
    """Apply successive .get() calls to container obj and return result if 
    something is found, else return specified default value"""
    if not args:
        return obj
    if isinstance(obj, (dict, list, tuple)):
        try:
            sub_obj = obj.__getitem__(args[0])
            return _get_recursive(sub_obj, args[1:], default)
        except (KeyError, IndexError):
            return default
    return default


class ZoneBuilder:

    def __init__(self, *args, **kwargs) -> None:
        self.zones = []
        self.display = Display()
        self.screen = self.display.screen()

        if count := kwargs.get('-n'):
            self.add(count)

    def _main_action(self):
        return input(
            'specify action:\n$ '
        )

    def _get_count(self):
        return input(
            'specify count:\n$ '
        )

    def main(self):
        action = self._main_action()

        if action == "save":
            self.save

        elif action == "exit":
            self.terminate() 

        else:
            print('action not understood. Please try again.\n')

        self.main()

    @property
    def save(self):
        results = []
        for zone in self.zones:
            # for some reason this works better with
            # a new display object on each iteration
            window = active_window(Display(), zone.id)  
            pg = window.query_tree().parent.query_tree().parent.get_geometry()
            results.append({
                "x": pg.x,
                "y": pg.y,
                "width": pg.width,
                "height": pg.height
            })
        SETTINGS.zones = results

        # if service is running, restart with new zones
        if _check_pid(SETTINGS.pid):
            print("restarting background process for updated zone settings...")
            launch_background_process()

        self.terminate()

    def add(self, count):
        previous_settings = SETTINGS.zones # list of dicts
        for i in range(int(count)):
            x = _get_recursive(previous_settings, (i, "x"), default=10)
            y = _get_recursive(previous_settings, (i, "y"), default=10)
            width = _get_recursive(previous_settings, (i, "width"), default=500)
            height = _get_recursive(previous_settings, (i, "height"), default=250)
            window = self.screen.root.create_window(
                10, 10, 500, 250, 1,
                self.screen.root_depth,
                background_pixel=750000,
                event_mask=X.ExposureMask | X.KeyPressMask,
            )
            window.map()
            window.configure(
                x=x,
                y=y,
                width=width,
                height=height,
                stack_mode=X.Above
            )           
            self.display.sync()
            self.zones.append(window)
        thread = threading.Thread(target=self.loop)
        thread.daemon = True
        thread.start()

    def loop(self):
        while True:
            try:
                e = self.display.next_event()
            except ConnectionClosedError:
                # raised when X button is pressed
                #
                # TODO: figure out way to allow exit of single window without
                # having to kill the entire application (currently get a
                # "socket_error" if you try to add a window after exiting 
                # an already made window)
                #
                # for now, just kill everything
                print()
                os._exit(1)

    def terminate(self):
        sys.exit()