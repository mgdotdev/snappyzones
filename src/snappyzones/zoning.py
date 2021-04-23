from Xlib import XK

from .conf.settings import SETTINGS

class Zone:
    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def check(self, x, y):
        if (
            self.x <= x <= self.x + self.width
        ) and (
            self.y <= y <= self.y + self.height
        ):
            return True
        return False


class ZoneProfile:
    def __init__(self, zones) -> None:
        self.zones = zones

    def find_zone(self, x, y, shift=None):
        for index, item in enumerate(self.zones):
            if item.check(x, y):
                if not shift:
                    obj_i = index
                    return self._shift_and_return(obj_i)
                elif shift == XK.XK_Left:
                    obj_i = (index-1)%len(self.zones)
                    return self._shift_and_return(obj_i)

                elif shift == XK.XK_Right:
                    obj_i = (index+1)%len(self.zones)
                    return self._shift_and_return(obj_i)
        return None

    def _shift_and_return(self, obj_i):
        obj = self.zones[obj_i]
        self.zones = self.zones[obj_i:] + self.zones[:obj_i]
        return obj

    @staticmethod
    def from_file():
        if data := SETTINGS.zones:
            return ZoneProfile([Zone(**obj) for obj in data])
        return ZoneProfile([])
