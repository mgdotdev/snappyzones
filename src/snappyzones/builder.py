import json
import os
import sys
import threading

from Xlib import X
from Xlib.display import Display
from Xlib.error import ConnectionClosedError

from .snap import active_window

HERE = os.path.abspath(os.path.dirname(__file__))


class Window:
    def __init__(self, display, msg):
        self.display = display
        self.msg = msg
 
        self.screen = self.display.screen()
        self.window = self.screen.root.create_window(
            10, 10, 500, 250, 1,
            self.screen.root_depth,
            background_pixel=self.screen.black_pixel,
            event_mask=X.ExposureMask | X.KeyPressMask,
        )
        self.gc = self.window.create_gc(
            background = self.screen.black_pixel,
        )
        self.window.map()
 
    def loop(self):
        # maybe only have one event loop per builder?
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
                os._exit(1)

    @property
    def _id(self):
        return self.window.id

class ZoneBuilder:

    def __init__(self) -> None:
        self.zones = []
        self.display = Display()
        self.screen = self.display.screen()

    def _main_action(self):
        return input(
            'specify action:\n$ '
        )

    def main(self):
        action = self._main_action()
        if action == "add":
            self.add

        elif action == "done":
            self.done

        elif action == "exit":
            self.terminate() 

        self.main()

    @property
    def done(self):
        results = []
        for zone, _ in self.zones:
            window = active_window(self.display, zone._id)
            pg = window.query_tree().parent.query_tree().parent.get_geometry()
            results.append({
                "x": pg.x,
                "y": pg.y,
                "width": pg.width,
                "height": pg.height
            })
        self._write(results)
        self.terminate()
            
    @property
    def add(self):
        window = Window(self.display, f"Zone {len(self.zones) + 1}")
        thread = threading.Thread(target=window.loop)
        thread.daemon = True
        thread.start()
        self.zones.append([window, thread])

    def _read(self, path = os.path.join(HERE, "zones.json")):
        with open(path, 'r') as f:
            return json.loads(f.read())

    def _write(self, results, path = os.path.join(HERE, "zones.json")):
        with open(path, 'w') as f:
            f.write(json.dumps(results, indent=2, sort_keys=True))

    def terminate(self):
        sys.exit()