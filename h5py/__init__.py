# This file is part of h5py, a Python interface to the HDF5 library.
#
# http://www.h5py.org
#
# Copyright 2008-2013 Andrew Collette and contributors
#
# License:  Standard 3-clause BSD; see "license.txt" for full license terms
#           and contributor agreement.

from h5py import _errors
_errors.silence_errors()

from h5py import _conv
_conv.register_converters()

from h5py import h5a, h5d, h5ds, h5f, h5fd, h5g, h5r, h5s, h5t, h5p, h5z

h5s.NULL = h5s._NULL  # NULL is a reserved name at the Cython layer
h5z._register_lzf()

from h5py.highlevel import *

from h5py.h5 import get_config
from h5py.h5r import Reference, RegionReference
from h5py.h5t import special_dtype, check_dtype

# Deprecated functions
from h5py.h5t import py_new_vlen as new_vlen
from h5py.h5t import py_get_vlen as get_vlen
from h5py.h5t import py_new_enum as new_enum
from h5py.h5t import py_get_enum as get_enum

from h5py import version

from .tests import run_tests

__version__ = version.version

__doc__ = \
"""
    This is the h5py package, a Python interface to the HDF5
    scientific data format.

    Version %s

    HDF5 %s
""" % (version.version, version.hdf5_version)


def enable_ipython_completer():
    import sys
    if 'IPython' in sys.modules:
        ip_running = False
        try:
            from IPython.core.interactiveshell import InteractiveShell
            ip_running = InteractiveShell.initialized()
        except ImportError:
            # support <ipython-0.11
            from IPython import ipapi as _ipapi
            ip_running = _ipapi.get() is not None
        except Exception:
            pass
        if ip_running:
            from . import ipy_completer
            return ipy_completer.load_ipython_extension()

    raise RuntimeError('completer must be enabled in active ipython session')

