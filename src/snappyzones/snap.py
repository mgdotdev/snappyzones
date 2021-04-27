from Xlib import X, XK
from Xlib.error import BadDrawable, BadWindow, XError
from Xlib.display import Display


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


def shift_window(self, keysym, stretch=False):
    try:
        display = Display()
        zone_profile = self.zp
        window = active_window(display)
        wg = window.get_geometry()
        dx, dy, dw, dh = geometry_deltas(window)
        pg = window.query_tree().parent.query_tree().parent.get_geometry()
        zone = zone_profile.find_zone(pg.x + pg.width / 2, pg.y + pg.height / 2, keysym)
        if window and zone:
            window.configure(
                x=zone.x,
                y=zone.y,
                width=zone.width - dx,
                height=zone.height - dy,
                stack_mode=X.Above,
            )
            display.sync()
    except BadDrawable:
        pass


def snap_window(self, x, y):
    try:
        display = Display()
        zone_profile = self.zp
        window = active_window(display)
        dx, dy, dw, dh = geometry_deltas(window)
        zone = zone_profile.find_zones(self, x, y)
        if window and zone:
            window.configure(
                x=zone.x,
                y=zone.y,
                width=zone.width - dx,
                height=zone.height - dy,
                stack_mode=X.Above,
            )
            display.sync()
    except BadDrawable:
        pass


def cycle_windows(self, keysym):
    try:
        display = Display()
        window = active_window(display).query_tree().parent.query_tree().parent
        root = display.screen().root
        tree = root.query_tree()

        stack = [
            item
            for item in tree.children
            if all(
                getattr(item.get_geometry(), x) == getattr(window.get_geometry(), x)
                for x in ("x", "y", "width", "height")
            )
        ]

        if keysym == XK.XK_Up:
            item = display.create_resource_object("window", stack[0].id)
            item.configure(stack_mode=X.Below)
            display.set_input_focus(stack[1], X.RevertToParent, X.CurrentTime)

        elif keysym == XK.XK_Down:
            item = display.create_resource_object("window", stack[-1].id)
            item.configure(stack_mode=X.Above)

        display.sync()
    except BadWindow as e:
        print(e)
