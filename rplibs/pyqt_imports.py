"""

Wrapper script to import all qt classes

"""

from __future__ import print_function
import sys
import pkgutil

from importlib.metadata import files

PYQT_VERSION = 5

try:
    import PyQt5
except ImportError:
    print("Could not import PyQt5, trying to import PyQt4")
    try:
        import PyQt4
        PYQT_VERSION = 4
    except ImportError:
        print("Failed to import either PyQt4 or PyQt5!")
        sys.exit(-1)

if PYQT_VERSION == 4:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

    def qt_connect(obj, signal_name, handler):
        QObject.connect(obj, SIGNAL(signal_name), handler)

elif PYQT_VERSION == 5:
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *

    def qt_connect(obj, signal_name, handler):
        if "(" in signal_name:
            slot_name = signal_name[:signal_name.index("(")]
            handler_type = signal_name[signal_name.index("(") + 1:].rstrip(")")
            handler_type = str(handler_type.replace("*", "")).strip()
            if not handler_type:
                getattr(obj, slot_name).connect(handler)
            else:
                py_type = {
                    "int": int,
                    "QString": str,
                    "double": float,
                    "QListWidgetItem": QListWidgetItem
                }[handler_type]
                getattr(obj, slot_name)[py_type].connect(handler)
        else:
            getattr(obj, signal_name).connect(handler)


def qt_register_fonts():
    for i in files('render-pipeline'):
        if len(i.parts) == 4 and '/'.join(i.parts[:3]) == 'rpcore/data/font':
            f = i.parts[3]
            if f.endswith('.ttf'):
                modpath = '.'.join(i.parts[:3])
                data = pkgutil.get_data(modpath, f)
                QFontDatabase.addApplicationFontFromData(data)
