import logging
from Xlib import X, XK
from Xlib.error import BadDrawable, XError
from Xlib.display import Display
from Xlib.xobject.drawable import Window

logger = logging.getLogger(__name__)

# the default gdm3 offsets due to shadows, borders etc
GEOMETRY_DELTAS_SNAP_GDM3 = 26,23,-57,-97
# The offset to apply to the window when saving because the visual part of the
# display box is not exactly the same as it's xlib coordinates
GEOMETRY_DELTAS_SAVE_GDM3 = 10,-19,-20,-55

def active_window(display, window_id=None):
    if not window_id:
        window_id = (
            display.screen()
            .root.get_full_property(
                display.intern_atom("_NET_ACTIVE_WINDOW"), X.AnyPropertyType
            )
            .value[0]
        )
    try:
        return display.create_resource_object("window", window_id)
    except XError:
        return None


def geometry_deltas(window:Window, window_manager:str = None):
    """The window of an app usually sits within an Xorg parent frame, and we
    want to fit that parent frame to the zone and not the inner window (so
    decorations like borders are properly handled). I can't seem to get that
    window to update directly, so we'll update the child window using the
    difference b/t the parent and child so to fit the final result
    correctly."""
    if window_manager == "gdm3":
        # In the case of gdm3, the above strategy doesnt seem to work.
        # When searching for parent frames, you quickly get to the root frame
        # without any obvious way of figuring out how big the shadow elements etc
        # are. So as a workaround, we hardcode them here.
        return GEOMETRY_DELTAS_SNAP_GDM3 
    wg = window.get_geometry()
    dx, dy, dw, dh = 0, 0, 0, 0
    parent = window.query_tree().parent
    pg = parent.get_geometry()
    dx = pg.x - wg.x
    dy = pg.y - wg.y
    dw = pg.width - wg.width
    dh = pg.height - wg.height
    return dx, dy, dw, dh


def geometry_deltas_save(window_manager:str = None):
    if window_manager == "gdm3":
        return GEOMETRY_DELTAS_SAVE_GDM3
    else:
        return 0,0,0,0


def shift_window(self, keysym, stretch=False, window_manager=None):
    try:
        display = Display()
        zone_profile = self.zp
        window = active_window(display)
        dx, dy, dw, dh = geometry_deltas(window)
        if window_manager == "gdm3":
            pg = window.get_geometry()
        else:
            pg = window.query_tree().parent.query_tree().parent.get_geometry()
        zone = zone_profile.find_zone(pg.x + pg.width / 2, pg.y + pg.height / 2, keysym)
        if window and zone:
            window.configure(
                x=zone.x - dx,
                y=zone.y - dy,
                width=zone.width - dw,
                height=zone.height - dh,
                stack_mode=X.Above,
            )
            display.sync()
    except BadDrawable:
        pass


def snap_window(self, x, y, window_manager=None):
    try:
        display = Display()
        zone_profile = self.zp
        window = active_window(display)
        dx, dy, dw, dh = geometry_deltas(window, window_manager=window_manager)
        zone = zone_profile.find_zones(self, x, y)
        if window and zone:
            window.configure(
                x=zone.x - dx,
                y=zone.y - dy,
                width=zone.width - dw,
                height=zone.height - dh,
                stack_mode=X.Above,
            )
            display.sync()
    except BadDrawable:
        pass
