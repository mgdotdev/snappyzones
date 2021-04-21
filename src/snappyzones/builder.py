import json
import os
import sys
import threading

from Xlib import X
from Xlib.display import Display
from Xlib.error import ConnectionClosedError

from .snap import active_window


HERE = os.path.abspath(os.path.dirname(__file__))


class ZoneBuilder:

    def __init__(self, *args, **kwargs) -> None:
        self.zones = []
        self.display = Display()
        self.screen = self.display.screen()
        self.running = True

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
        self._write(results)
        self.terminate()

    def add(self, count):
        for _ in range(int(count)):
            window = self.screen.root.create_window(
                10, 10, 500, 250, 1,
                self.screen.root_depth,
                background_pixel=750000,
                event_mask=X.ExposureMask | X.KeyPressMask,
            )
            window.map()
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

    def _read(self, path = os.path.join(HERE, "zones.json")):
        with open(path, 'r') as f:
            return json.loads(f.read())

    def _write(self, results, path = os.path.join(HERE, "zones.json")):
        with open(path, 'w') as f:
            f.write(json.dumps(results, indent=2, sort_keys=True))

    def terminate(self):
        sys.exit()