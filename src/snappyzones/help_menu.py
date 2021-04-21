import os.path

HERE = os.path.abspath(os.path.dirname(__file__))


class CacheProperty:
    def __init__(self, fget) -> None:
        self.fget = fget

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = self.fget(obj)
        setattr(obj, self.fget.__name__, value)
        return value


class HelpMenu:
    def __init__(self) -> None:
        with open(os.path.join(HERE, 'help_text.md'), 'r') as f:
            self._raw_menu = f.read()


    def get(self, cmd):
        pass