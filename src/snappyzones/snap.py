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


def geometry_deltas(window, display):
    root = display.screen().root
    wg = window.get_geometry()
    dx, dy, dw, dh = 0, 0, 0, 0
    while all(x == 0 for x in (dx, dy, dw, dh)):
        parent = window.query_tree().parent
        pg = parent.get_geometry()
        dx = pg.x - wg.x
        dy = pg.y - wg.y
        dw = pg.width - wg.width
        dh = pg.height - wg.height
        window = parent
    return dx, dy, dw, dh


def snap_window(x, y):
    display = Display()
    zone_profile = ZoneProfile._test()
    window = active_window(display)
    dx, dy, dw, dh = geometry_deltas(window, display)
    zone = zone_profile.find_zone(x, y)
    if window and zone:
        window.configure(
            x=zone.x + dw,
            y=zone.y + dh,
            width=zone.width - dx,
            height=zone.height - dy,
            stack_mode=X.Above
        )
        display.sync()
