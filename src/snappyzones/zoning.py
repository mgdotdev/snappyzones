import json
from os import stat

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
    def from_file(path):
        with open(path, 'r') as f:
            data = json.loads(f.read())
        return ZoneProfile([Zone(**obj) for obj in data])

    @staticmethod
    def _test():
        return ZoneProfile([
            Zone(0, 0, 1080, 1920),
            Zone(1080, 0, 1080, 600),
            Zone(1080, 600, 1080, 1320),
            Zone(2160, 335, 1920, 540),
            Zone(2160, 335, 1920, 540)
        ])