from Xlib import XK

from .conf.settings import SETTINGS

MEAN_PIXEL_TOLERANCE = 10

def mean(lst):
    return sum(lst) / len(lst)


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

    @property
    def corners(self):
        return [
            (self.x, self.y),
            (self.x+self.width, self.y),
            (self.x+self.width, self.y+self.height),
            (self.x, self.y+self.height)
        ]


class ZoneProfile:
    def __init__(self, zones) -> None:
        self.zones = zones

    def find_zones(self, service, x, y, shift=None):
        _zones = []
        for coordinate in service.coordinates:
            for item in self.zones:
                if item.check(*coordinate) and item not in _zones:
                    _zones.append(item)
                    break
        
        if not _zones:
            return None

        if len(_zones) == 1:
            return _zones.pop()

        x_min_zone = min((i for i in _zones), key=lambda i: i.x)
        y_min_zone = min((i for i in _zones), key=lambda i: i.y)

        # if all zones are in the same row
        if abs(mean(set(i.x for i in _zones)) - x_min_zone.x) < MEAN_PIXEL_TOLERANCE:
            width = x_min_zone.width
            height = sum(i.height for i in _zones)

        # if all zones are in the same column
        elif abs(mean(set(i.y for i in _zones)) - y_min_zone.y) < MEAN_PIXEL_TOLERANCE:
            width = sum(i.width for i in _zones)
            height = y_min_zone.height
        
        # stretch first zone into last zone
        elif len(_zones) == 2:
            initial_zone = self.find_zone(*service.coordinates[0])
            final_zone = self.find_zone(*service.coordinates[-1])
            slope = abs((initial_zone.y - final_zone.y) / (initial_zone.x - final_zone.x))
            if slope > 1: # means we're stretching the height
                x = x_min_zone.x
                y = y_min_zone.y
                width = initial_zone.width
                height = initial_zone.height + final_zone.height
            else: # means we're stretching the width
                x = x_min_zone.x
                y = initial_zone.y
                width = initial_zone.width + final_zone.width
                height = initial_zone.height
            return Zone(x, y, width, height)

        # return a zone which covers all zones
        else:
            width, height = 0, 0
            for z in _zones:
                if z.corners[1][0] - x_min_zone.x > width:
                    width = z.corners[1][0] - x_min_zone.x
                if z.corners[3][1] - y_min_zone.y > height:
                    height = z.corners[3][1] - y_min_zone.y
            return Zone(
                x_min_zone.x,
                y_min_zone.y,
                width,
                height
            )
        return Zone(x_min_zone.x, y_min_zone.y, width, height)


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
