import os.path
import json


HERE = os.path.abspath(os.path.dirname(__file__))


class Settings:

    @property
    def pid(self):
        if res := self._read(self._pid_file):
            return int(res)
        return None

    @pid.setter
    def pid(self, _pid):
        self._write(self._pid_file, str(_pid))

    @property
    def zones(self):
        if _zones := self._read(self._zone_file):
            return json.loads(_zones)
        return None

    @zones.setter
    def zones(self, _zones):
        self._write(
            self._zone_file, json.dumps(_zones, indent=2, sort_keys=True)
        )

    @property
    def keybindings(self):
        _data = self._read(self._keybindings_file)
        results = [
            char for char in _data.split('\n') 
            if not char.startswith("#") and char != ""
        ]
        if results:
            return results
        return ["Shift_L"] # a default in case someone tries to be funny

    @property
    def _keybindings_file(self):
        return os.path.join(HERE, '.keybindings')

    @property
    def _zone_file(self):
        return os.path.join(HERE, 'zones.json')

    @property
    def _pid_file(self):
        return os.path.join(HERE, '.pid')

    def _read(self, path, default=None):
        if os.path.isfile(path):
            with open(path, 'r') as f:
                return f.read()
        return default

    def _write(self, path, obj):
        with open(path, 'w') as f:
            f.write(obj)

SETTINGS = Settings()