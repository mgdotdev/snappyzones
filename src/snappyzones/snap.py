from Xlib import X
from Xlib.error import XError
from Xlib.display import Display

from .zoning import ZoneProfile

def active_window(display):
    window_id = display.screen().root.get_full_property(
        display.intern_atom('_NET_ACTIVE_WINDOW'), X.AnyPropertyType
    ).value[0]
    try:
        return display.create_resource_object('window', window_id)
    except XError:
        return None


def snap_window(x, y):
    display = Display()
    zone_profile = ZoneProfile._test()
    window = active_window(display)
    zone = zone_profile.find_zone(x, y)

    if window and zone:
        window.configure(
            x=zone.x,
            y=zone.y,
            width=zone.width,
            height=zone.height,
            stack_mode=X.Above
        )
        display.sync()
