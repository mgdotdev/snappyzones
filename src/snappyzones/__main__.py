#! /usr/bin/python3

from .cmd_reader import reader
from .service import Service
from .builder import ZoneBuilder


def main():
    cmd, args, kwargs = reader()
    if not any([cmd, args, kwargs]):
        service = Service()
        service.listen()
    
    if cmd == ["config"]:
        zb = ZoneBuilder()
        zb.main()
    
    
if __name__ == "__main__":
    main()
