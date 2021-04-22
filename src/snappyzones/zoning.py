import json
import os.path

HERE = os.path.abspath(os.path.dirname(__file__))


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
                    return item
                elif shift == "LEFT":
                    return self.zones[(index-1)%len(self.zones)]
                elif shift == "RIGHT":
                    return self.zones[(index+1)%len(self.zones)]
        return None

    @staticmethod
    def from_file(path = os.path.join(HERE, "zones.json")):
        if os.path.isfile(path):
            with open(path, 'r') as f:
                data = json.loads(f.read())
            return ZoneProfile([Zone(**obj) for obj in data])
        return ZoneProfile([])
