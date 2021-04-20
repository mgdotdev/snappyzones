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

    def find_zone(self, x, y):
        for item in self.zones:
            if item.check(x, y):
                return item

    @staticmethod
    def from_file(path = os.path.join(HERE, "zones.json")):
        with open(path, 'r') as f:
            data = json.loads(f.read())
        return ZoneProfile([Zone(**obj) for obj in data])
