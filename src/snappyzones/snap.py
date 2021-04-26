from Xlib import X, XK
from Xlib.error import XError
from Xlib.display import Display


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


def snap_window(self, x, y):
    display = Display()
    window = active_window(display)
    dx, dy, _, _ = geometry_deltas(window)
    zone = self.zone_profile.find_zone(x, y)
    if window and zone:
        window.configure(
            x=zone.x,
            y=zone.y,
            width=zone.width - dx,
            height=zone.height - dy,
            stack_mode=X.Above
        )
        display.sync()



def shift_window(self, keysym):
    if keysym in (XK.XK_Down, XK.XK_Up):
        return stack_shuffle(self, keysym)
    return shift_lateral(self, keysym)


def shift_lateral(self, keysym):
    display = Display()
    window = active_window(display)
    pg = window.query_tree().parent.query_tree().parent.get_geometry()
    x, y = pg.x + pg.width/2, pg.y + pg.height/2
    zone = self.zone_profile.find_zone(x, y, keysym)

    dx, dy, _, _ = geometry_deltas(window)
    
    if window and zone:
        window.configure(
            x=zone.x,
            y=zone.y,
            width=zone.width - dx,
            height=zone.height - dy,
            stack_mode=X.Above
        )
        display.sync()


def stack_shuffle(self, keysym):
    display = Display()
    root = display.screen().root
    window = active_window(display)
    pg = window.query_tree().parent.query_tree().parent.get_geometry()
    x, y = pg.x + pg.width/2, pg.y + pg.height/2
    zone = self.zone_profile.find_zone(x, y, keysym)
    windows = []
    for child in root.query_tree().children:
        geometry = child.get_geometry()
        if all([
            zone.x == geometry.x,
            zone.y == geometry.y,
            zone.width == geometry.width,
            zone.height == geometry.height,
        ]):
            windows.append(
                child
            )

    if keysym == XK.XK_Down:
        window = active_window(display, windows[-1].id)
        window.map()
        window.raise_window() # = active_window(display)

    elif keysym == XK.XK_Up:
        window.query_tree().parent.query_tree().parent.configure(
            stack_mode=X.Below
        )
        # active = active_window(display, windows[1].id)
        # active.raise_window()
        # import pdb; pdb.set_trace()

    display.sync()

    # if keysym == XK.XK_Up:
    #     shift_list = windows[1:] + windows[:1]
    # elif keysym == XK.XK_Down:
    #     shift_list = windows[-1:] + windows[:-1]

    # if keysym == XK.XK_Down:
    # for window in shift_list:
    #     window = active_window(display, window.id)
    #     window.configure(
    #         stack_mode=X.Below
    #     )
    #     # window = active_window(display, windows[1].id)
        
    #     display.sync()
    #     window.set_input_focus(X.RevertToParent, X.CurrentTime)


    # for window in windows:
        # import pdb; pdb.set_trace()
        # window.configure(
            
        # )

    print('shift')

################################################################################

    # if keysym == XK.XK_Up:
    #     shift_list = windows[1:] + windows[:1]
    # elif keysym == XK.XK_Down:
    #     shift_list = windows[-1:] + windows[:-1]

    # if keysym == XK.XK_Down:
    #     window = active_window(display, windows[-1].id)
    #     window.raise_window() # = active_window(display)
    #     # _push_all(window, X.Below)
    #     # window.configure(
    #     #     stack_mode=X.Below
    #     # )
    #     

    

    # for window in shift_list:
    #     w = active_window(display, window.id)
    #     import pdb; pdb.set_trace()
    #     # window.set_input_focus(X.RevertToParent, X.CurrentTime)
    #     # window.configure(
    #     #     stack_mode=X.Above
    #     # )
    #     # window.raise_window()
    #     display.sync()
    #     import pdb; pdb.set_trace()
