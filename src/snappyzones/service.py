from Xlib import X
from Xlib.ext import record
from Xlib.display import Display
from Xlib.protocol import rq

from .snap import snap_window, shift_window

KEYS = {
    's': 39,
    'ALT': 64,
    "UP_ARROW": 111,
    "LEFT_ARROW": 113,
    "RIGHT_ARROW": 114,
    "DOWN_ARROW": 116
}

class Service:
    def __init__(self) -> None:
        self.alt = True
        self.track = False

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
                
            if event.type == X.KeyPress and event.detail == KEYS['ALT']:
                self.alt = True

            elif event.type == X.KeyRelease and event.detail == KEYS['ALT']:
                self.alt = False
                self.track = False

            elif all([
                event.type == X.KeyPress,
                self.alt,
                event.detail == KEYS['s']
            ]):
                self.track = True

            elif event.type == X.ButtonRelease and self.track:
                snap_window(event.root_x, event.root_y)
                self.alt = False
                self.track = False

            elif event.type == X.KeyPress and self.track and event.detail == KEYS['LEFT_ARROW']:
                shift_window('LEFT')

            elif event.type == X.KeyPress and self.track and event.detail == KEYS['RIGHT_ARROW']:
                shift_window('RIGHT')

    def listen(self):
        while True:
            self.root.display.next_event()