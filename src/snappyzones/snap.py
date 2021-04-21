from Xlib import X
from Xlib.error import XError
from Xlib.display import Display

from .zoning import ZoneProfile


def active_window(display, window_id=None):
    if not window_id:
        window_id = display.screen().root.get_full_property(
            display.intern_atom('_NET_ACTIVE_WINDOW'), X.AnyPropertyType
        ).value[0]
    try:
        return display.create_resource_object('window', window_id)
    except XError:
        return None
        

def geometry_deltas(window):
    """The window of an app usually sits within an Xorg parent frame, and we 
    want to fit that parent frame to the zone and not the inner window (so 
    decorations like borders are properly handled). I can't seem to get that
    window to update directly, so we'll update the child window using the
    difference b/t the parent and child so to fit the final result 
    correctly."""
    wg = window.get_geometry()
    dx, dy, dw, dh = 0, 0, 0, 0
    parent = window.query_tree().parent
    pg = parent.get_geometry()
    dx = pg.x - wg.x
    dy = pg.y - wg.y
    dw = pg.width - wg.width
    dh = pg.height - wg.height
    return dx, dy, dw, dh


def shift_window(direction):
    display = Display()
    zone_profile = ZoneProfile.from_file()
    window = active_window(display)
    dx, dy, dw, dh = geometry_deltas(window)
    pg = window.query_tree().parent.query_tree().parent.get_geometry()
    zone = zone_profile.find_zone(pg.x + pg.width/2, pg.y + pg.height/2, direction)
    if window and zone:
        window.configure(
            x=zone.x,
            y=zone.y,
            width=zone.width - dx,
            height=zone.height - dy,
            stack_mode=X.Above
        )
        display.sync()


def snap_window(x, y):
    display = Display()
    zone_profile = ZoneProfile.from_file()
    window = active_window(display)
    dx, dy, dw, dh = geometry_deltas(window)
    zone = zone_profile.find_zone(x, y)
    if window and zone:
        window.configure(
            x=zone.x,
            y=zone.y,
            width=zone.width - dx,
            height=zone.height - dy,
            stack_mode=X.Above
        )
        display.sync()
