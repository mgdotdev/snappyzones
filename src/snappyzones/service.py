from Xlib import X, XK
from Xlib.ext import record
from Xlib.display import Display
from Xlib.protocol import rq

from snappyzones.zoning import ZoneProfile

from .snap import snap_window, shift_window


class Service:
    def __init__(self) -> None:
        self.keybindings = {
            XK.XK_s: False,
            XK.XK_Alt_L: False
        }
        self.zp = ZoneProfile.from_file()

        self.display = Display()
        self.root = self.display.screen().root
        
        self.context = self.display.record_create_context(0, [record.AllClients], [{
            'core_requests': (0, 0),
            'core_replies': (0, 0),
            'ext_requests': (0, 0, 0, 0),
            'ext_replies': (0, 0, 0, 0),
            'delivered_events': (0, 0),
            'device_events': (X.KeyReleaseMask, X.ButtonReleaseMask),
            'errors': (0, 0),
            'client_started': False,
            'client_died': False,
        }])

        self.display.record_enable_context(self.context, self.handler)
        self.display.record_free_context(self.context)
        
    def handler(self, reply):
        data = reply.data
        while len(data):

            event, data = rq.EventField(None).parse_binary_value(data, self.display.display, None, None)
                
            if event.type == X.KeyPress or X.KeyRelease:
                keysym = self.display.keycode_to_keysym(event.detail, 0)
                if keysym in self.keybindings:
                    self.keybindings[keysym] = (
                        True if event.type == X.KeyPress else False
                    )

            if all([value == True for value in self.keybindings.values()]):

                if event.type == X.ButtonRelease:
                    snap_window(self, event.root_x, event.root_y)

                elif event.type == X.KeyPress:
                    keysym = self.display.keycode_to_keysym(event.detail, 0)
                    if keysym == XK.XK_Left:
                        shift_window(self, 'LEFT')

                    elif keysym == XK.XK_Right:
                        shift_window(self, 'RIGHT')

    def listen(self):
        while True:
            self.root.display.next_event()