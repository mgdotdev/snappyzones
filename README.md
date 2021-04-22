# Snappy Zones

## FancyZones for Linux

This project is an attempt to emulate the functionality Windows users get from FancyZones. Users can drag and drop windows into predefined zones, and have SnappyZones fit the window to the zone specs. Users can also snap windows left/right between zones.

How to use:

Snappy Zones can be started from either the console command `snappy` or by calling the module `python -m snappyzones`. These two starting methods are essentially synonymous.

On first use, we'll need to configure our zones. This can be done by calling `snappy config -n <ZONE_COUNT>` where `<ZONE_COUNT>` is the number of zones to generate. Snappy Zones will generate a number or blank Xorg windows equivalent to the `<ZONE_COUNT>`. Drag these windows around your screen as you would any other window. When your zones are placed, type `save` into the terminal to save the zone configuration. You can also type `exit` to exit without saving.

With our zones configured, we can now call `snappy` to start Snappy Zones as a terminal process. With snappy running, we can hold `Left_Alt + s` to activate snapping. Holding this keybinding, we can drag windows to our zones, and upon releasing the mouse click the window will snap to the dimensions of the predefined zones. We can also press `Left/Right` arrow keys so to rotate the current active window across zones.

Snappy Zones can also be run as a background process. `snappy start` Pushes Snappy Zones to a background process. `snappy stop` kills the process.

This project is currently under active development, please check back for more updates and features soon.