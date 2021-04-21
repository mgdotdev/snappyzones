import sys

from .help_menu import HelpMenu

def simple_isnan(item):
    try:
        float(item)
        return False
    except ValueError:
        return True

def _get_help(cmd=""):
    help_menu = HelpMenu()
    help_menu.get(cmd)
    sys.exit()

def reader():
    cmd = sys.argv[1:2]
    args = sys.argv[2::]
    kwargs = {}

    if cmd in ("-h", "--help"):
        return _get_help()
    elif any(h in args for h in ("-h", "--help")):
        return _get_help(cmd)
        
    kwarg_keys = reversed([
        index for index, item in enumerate(args) 
        if (item.startswith('-') and simple_isnan(item))
    ])
    for k in kwarg_keys:
        try:
            value = args.pop(k+1)
        except IndexError:
            value = True
        key = args.pop(k)
        kwargs[key] = value

    return cmd, args, kwargs