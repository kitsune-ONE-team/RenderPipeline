"""

Main PyYAML importer script. Provides functions to load YAML files as dictionaries.

"""

from __future__ import print_function

import io
import os
import pkgutil
import sys

from panda3d.core import VirtualFileSystem
from rpcore.rpobject import RPObject

# Import different PyYaml versions depending on the used python version
if sys.version_info < (3, 0):
    from .yaml_py2 import load as yaml_load
    from .yaml_py2 import YAMLError, SafeLoader
else:
    from .yaml_py3 import load as yaml_load
    from .yaml_py3 import YAMLError, SafeLoader

__all__ = ["load_yaml_file", "load_yaml_file_flat"]


def load_yaml_file(filepath):
    """ This method is a wrapper arround yaml_load, and provides error checking """

    # import time
    # start = time.process_time()

    try:
        vfs = VirtualFileSystem.get_global_ptr()
        if vfs.exists(filepath):  # load from VFS
            handle = io.BytesIO(vfs.read_file(filepath, False))
        else:  # load from zipped package
            if filepath.startswith('/$$rp/'):
                filepath = filepath.replace('/$$rp/', '')
            modpath = os.path.dirname(filepath).replace('/', '.')
            filename = os.path.basename(filepath)
            handle = io.BytesIO(pkgutil.get_data(modpath, filename))

        parsed_yaml = yaml_load(handle, Loader=SafeLoader)
        handle.close()
    except IOError as msg:
        RPObject.global_error("YAMLLoader", "Could not find or open file:", filename)
        RPObject.global_error("YAMLLoader", msg)
        raise Exception("Failed to load YAML file: File not found")
    except YAMLError as msg:
        RPObject.global_error("YAMLLoader", "Invalid yaml-syntax in file:", filename)
        RPObject.global_error("YAMLLoader", msg)
        raise Exception("Failed to load YAML file: Invalid syntax")

    # duration = (time.process_time() - start) * 1000.0

    # Optionally print out profiling information
    # print("Took", round(duration, 2), "ms to load", filename)

    return parsed_yaml


def __flatten(d, parent_key=''):
    """ Internal method to flatten a dictionary """
    items = []
    for k, v in d.items():
        try:
            items.extend(__flatten(v, '{}{}.'.format(parent_key, k)).items())
        except AttributeError:
            items.append(('{}{}'.format(parent_key, k), v))
    return dict(items)


def load_yaml_file_flat(filename):
    """ Behaves like load_yaml_file, but instead of creating nested dictionaries
    it connects keys via '.' """
    return __flatten(load_yaml_file(filename))
