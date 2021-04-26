import os

from Xlib import X, XK
from Xlib.ext import record
from Xlib.display import Display
from Xlib.protocol import rq

from .settings import SETTINGS


def set_keybindings(*args, **kwargs):
    SETTINGS.keybindings = args

class KeybindingService:
    def __init__(self) -> None:
        self.display = Display()
        self.root = self.display.screen().root

        self.staging = ""
        self.keys = []

        self.keymap = {
            XK.string_to_keysym(key): key for key in SETTINGS._raw_keybindings
        }

        self.context = self.display.record_create_context(
            0, [record.AllClients], [{
                'core_requests': (0, 0),
                'core_replies': (0, 0),
                'ext_requests': (0, 0, 0, 0),
                'ext_replies': (0, 0, 0, 0),
                'delivered_events': (0, 0),
                'device_events': (X.KeyReleaseMask, X.ButtonReleaseMask),
                'errors': (0, 0),
                'client_started': False,
                'client_died': False,
            }]
        )

        self.display.record_enable_context(self.context, self.handler)
        self.display.record_free_context(self.context)
        

    def handler(self, reply) -> None:
        data = reply.data
        while len(data):
            event, data = rq.EventField(None).parse_binary_value(
                data, self.display.display, None, None
            )
            
            if event.type == X.KeyPress:
                keycode = event.detail
                keysym = self.display.keycode_to_keysym(keycode, 0)
                if keysym in self.keymap and self.keymap[keysym] not in self.keys:
                    self.keys.append(self.keymap[keysym])
                end_str = f"\rKEYBINDING: {' + '.join(self.keys)}   LAST_KEY: "
                clear_str = "\r" + (" " * int(os.get_terminal_size().columns*0.75))
                print(clear_str, end=end_str)
                
            elif event.type == X.KeyRelease:
                keycode = event.detail
                keysym = self.display.keycode_to_keysym(keycode, 0)
                if keysym in self.keymap and self.keymap[keysym] in self.keys:
                    self.keys.remove(self.keymap[keysym])   
                end_str = f"\rKEYBINDING: {' + '.join(self.keys)}   LAST_KEY: "
                clear_str = "\r" + (" " * int(os.get_terminal_size().columns*0.75))
                print(clear_str, end=end_str)

            else:
                print(end="\r")


    def listen(self) -> None:
        while True:
            self.display.next_event()