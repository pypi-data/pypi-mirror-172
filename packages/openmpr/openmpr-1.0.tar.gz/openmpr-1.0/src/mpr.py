#
# mpr and mapr: SciVis-2023 Project 2
# Copyright (C)  2023 University of Chicago. All rights reserved.
#
# This is only for students and instructors in the 2023 CMSC 23710/33710
# ("SciVis") class, for use in that class. It is not licensed for open-source
# or any other kind of re-distribution. Do not allow this file to be copied
# or downloaded by anyone outside the 2023 SciVis class.
#
"""
This is a wrapper around "_mpr" (or "_rmpr"), the CFFI-generated extension
module for accessing the C shared library libmpr.{so,dylib} (or, the reference
implementation in librmpr.{so,dylib}).
The objects "exported" by this module are:
- wrappers for functions that use biff, turning biff error messages into Exceptions
- Tenums for making airEnums in libmpr useful from Python
- lib = _mpr.lib: direct references to the CFFI-generated objects
- ffi = _mpr.ffi: The value of this ffi over "from cffi import FFI; ffi = FFI()"
  is that it knows about the typedefs (especially for "real") that were cdef()'d to
  build the CFFI wrapper, which (via ffi.new) can help set up calls into libmpr.
For more about CFFI see https://cffi.readthedocs.io/en/latest/
(NOTE: GLK welcomes suggestions on how to make this more useful or pythonic)
"""

# pylint can't see inside CFFI-generated modules
# pylint: disable=c-extension-no-member

# In the interest of simplicity, this file is distributed to students twice,
# once as mpr.py (which loads the CFFI-generated _mpr extension), and again as
# rmpr.py (which loads _rmpr for reference code), but with the same file contents.
# The functional difference arises from the "if 'rmpr' == __name__:" below.
# This is pretty hacky, please suggest improvements to GLK!

# (lots of underscore prefixing to prevent "export"ing them from this module)
import re as _re  # for extracting biff key name from function name
import os as _os
import pathlib as _pathlib
import sys as _sys

# halt if python2; thanks to https://preview.tinyurl.com/44f2beza
_x, *_y = 1, 2  # NOTE: A SyntaxError means you need python3, not python2
del _x, _y


class Tenum:
    # HEY: copy-pasted from teem.py in Teem source distro w/ _teem -> _mpr rename
    """A helper/wrapper around airEnums (or pointers to them) in Teem, which
    provides convenient ways to convert between integer enum values and real
    Python strings. The C airEnum underlying the Python Tenum foo is still
    available as foo()."""

    def __init__(self, aenm, _name):
        """Constructor takes a Teem airEnum pointer (const airEnum *const)."""
        if not str(aenm).startswith("<cdata 'airEnum *' "):
            raise TypeError(f"passed argument {aenm} does not seem to be a Teem airEnum pointer")
        self.aenm = aenm
        self.name = _mpr.ffi.string(self.aenm.name).decode("ascii")
        self._name = _name  # the variable name for the airEnum
        # following definition of airEnum struct in air.h
        self.vals = list(range(1, self.aenm.M + 1))
        if self.aenm.val:
            self.vals = [self.aenm.val[i] for i in self.vals]

    def __call__(self):
        """Returns (a pointer to) the underlying Teem airEnum."""
        return self.aenm

    def __iter__(self):
        """Provides a way to iterate through the valid values of the enum"""
        return iter(self.vals)

    def valid(self, ios) -> bool:  # ios = int or string
        """Answers whether given int is a valid value of enum, or whether given string
        is a valid string in enum, depending on incoming type.
        (wraps airEnumValCheck() and airEnumVal())"""
        if isinstance(ios, int):
            return not _mpr.lib.airEnumValCheck(self.aenm, ios)
        if isinstance(ios, str):
            return self.unknown() != self.val(ios)
        # else
        raise TypeError(f"Need an int or str argument (not {type(ios)})")

    def str(self, val: int, picky=False) -> str:
        """Converts from integer enum value val to string identifier
        (wraps airEnumStr())"""
        assert isinstance(val, int), f"Need an int argument (not {type(val)})"
        if picky and not self.valid(val):
            raise ValueError(f'{val} not a valid {self._name} ("{self.name}") enum value')
        # else
        return _mpr.ffi.string(_mpr.lib.airEnumStr(self.aenm, val)).decode("ascii")

    def desc(self, val: int) -> str:
        """Converts from integer value val to description string
        (wraps airEnumDesc())"""
        assert isinstance(val, int), f"Need an int argument (not {type(val)})"
        return _mpr.ffi.string(_mpr.lib.airEnumDesc(self.aenm, val)).decode("ascii")

    def val(self, sss: str, picky=False) -> int:
        """Converts from string sss to integer enum value
        (wraps airEnumVal())"""
        assert isinstance(sss, str), f"Need an string argument (not {type(sss)})"
        ret = _mpr.lib.airEnumVal(self.aenm, sss.encode("ascii"))
        if picky and ret == self.unknown():
            raise ValueError(f'"{sss}" not parsable as {self._name} ("{self.name}") enum value')
        # else
        return ret

    def unknown(self) -> int:
        """Returns value representing unknown
        (wraps airEnumUnknown())"""
        return _mpr.lib.airEnumUnknown(self.aenm)


# def _make_shlib(shlib_ext: str) -> None:
#     # (HEY: this is copy/pasted from build_mpr.py, but adding some underscores)
#     """Runs "make shlib" to rebuild libmpr.{so,dylib} containing *student* code."""
#     # Seem to need some directory trickery: the import that got us to this point could
#     # have been started from anywhere; we need to get to the parent directory of this
#     # very file. 1st ".parent" below is only dir containing this file); 2nd ".parent"
#     # is the parent directory with the Makefile with needed 'shlib' target
#     print(f'mpr.py: rebuilding shared library libmpr.{shlib_ext}, via:')
#     pth = _pathlib.Path(_os.path.realpath(__file__)).parent.parent
#     cmd = f'cd {pth.absolute()}; make shlib'
#     print('   ', cmd)
#     if _os.system(cmd):
#         raise RuntimeError(f'due to trying to rebuild libmpr.{shlib_ext}')


# The functions that use biff, based on a manually-generated list
# of functions that is spliced in here as part of project creation
_BIFF_LIST = [
    "nrrdMaybeAlloc_nva",
    "nrrdMaybeAlloc_va",
    "nrrdLoad",
    "nrrdSave",
    "mprCmapLutGen",
    "mprCmapLutDraw",
    "mprCmapAlloc",
    "mprCmapLoad",
    "mprImageAlloc",
    "mprImageNrrdWrap",
    "mprImageSave",
    "mprImageLoad",
    "mprImageMinMax",
    "mprImageGrayQuantize",
    "*mprCtxNew",
    "mprCtxModeFuzzyIsoParmSet",
    "mprCtxModeValueCmapShadedParmSet",
    "mprCtxHelper",
    "mprPictureItoW",
    "mprPictureSample",
    "mprIsocontour",
]


def _biffer(func, func_name, errv, bkey):
    """Generates a biff-checking wrapper around given function (from CFFI)."""

    def wrapper(*args):
        # pass all args to underlying C function; get return value rv
        retv = func(*args)
        # nrrdLoad returns 1 or 2 for different errors
        if retv == errv or ("nrrdLoad" == func_name and 2 == retv):
            err = _mpr.lib.biffGetDone(bkey)
            estr = _mpr.ffi.string(err).decode("ascii").rstrip()
            _mpr.lib.free(err)
            raise RuntimeError(f'return value {retv} from C function "{func_name}":\n{estr}')
        return retv

    wrapper.__name__ = func_name
    wrapper.__doc__ = f"""
error-checking wrapper around C function "{func_name}":
{func.__doc__}
"""
    return wrapper


def _export_mpr() -> None:
    """Figures out what to export, and how, from _mpr extension module."""
    err_val = {}  # dict maps from function name to return value signifying error
    for bfunc in _BIFF_LIST:
        if "*" == bfunc[0]:
            # if function name starts with '*', then returning NULL means biff error
            fff = bfunc[1:]
            eee = ffi.NULL
        else:
            # else returning 1 indicates error (except for nrrdLoad, handled specially)
            fff = bfunc
            eee = 1
        err_val[fff] = eee
    for sym_name in dir(_mpr.lib):
        name_in = sym_name.startswith("mpr") or sym_name.startswith("MPR")
        sym = getattr(_mpr.lib, sym_name)
        # Initialize python object to export from this module for sym.
        exprt = None
        if not sym_name in _BIFF_LIST:
            # ... either not a function, or a function not known to use biff
            if str(sym).startswith("<cdata 'airEnum *' "):
                # sym_name is name of an airEnum, wrap it as such
                exprt = Tenum(sym, sym_name)
            else:
                if name_in:
                    exprt = sym
                # else sym is outside mpr and is not a biff-using function,
                # so we don't make it directly available with "import mpr"
                # (though still available in mpr.lib)
        else:
            # ... or a Python wrapper around a function known to use biff (including
            # things not in mpr like nrrdLoad). The biff key for a given function
            # is the string of lower-case letters prior to the first upper-case letter.
            bkey = _re.findall("^[^A-Z]*", sym_name)[0].encode("ascii")
            exprt = _biffer(sym, sym_name, err_val[sym_name], bkey)
        if exprt is not None:
            globals()[sym_name] = exprt
            # Everything in C library mpr is already prefixed by "mpr" or "MPR",
            # because it is designed to play well with other C libraries (and C, just like
            # the compiler's linker, has notion of namespaces). So, "from mpr import *"
            # is not actually as crazy as it would be in general. We add sym_name to list
            # of what "import *" imports if it starts with mpr or MPR
            if name_in:
                __all__.append(sym_name)


if __name__ != "__main__":  # here because of an "import"
    if _sys.platform == "darwin":  # mac
        _SHEXT = "dylib"
    else:
        _SHEXT = "so"
    # Start by importing _mpr or _rmpr, which depends (as described above) on
    # envvar LD_LIBRARY_PATH (or DYLD_LIBRARY_PATH) on mac being set to include
    # $SCIVIS/tpz/shlib/libtpz.  Why can't we use an rpath set in the shared
    # library to avoid depending on environment variables: because the directory
    # identified by $SCIVIS is not actually required to be in any particular
    # location relative to where we are here (so the rpath can't be a relative
    # path), and we certainly can't assume an absolute path that will work for
    # all students.
    if "rmpr" == __name__:
        # no attempt to re-make, assume already created as part of distribution
        try:
            import _rmpr as _mpr
        except ModuleNotFoundError:
            print(
                f"*\n* {__name__}.py: failed to load librmpr extension module _rmpr.\n"
                '* Did you first run "python3 build_mpr.py -r"?\n*\n'
            )
            raise
    else:
        # first re-make shared library as needed
        # _make_shlib(_SHEXT)
        # now import the shared library
        try:
            import _mpr
        except ModuleNotFoundError:
            print(
                f"*\n* {__name__}.py: failed to load libmpr extension module _mpr.\n"
                '* Did you first run "python3 build_mpr.py"?\n*\n'
            )
            raise
    # The value of this ffi, as opposed to "from cffi import FFI; ffi = FFI()" is that it knows
    # about the various typedefs that were learned to build the CFFI wrapper, which may in turn
    # be useful for setting up calls into libmpr
    ffi = _mpr.ffi
    # enable access to all the un-wrapped things straight from cffi
    lib = _mpr.lib
    # initialize the list of names that will be exported with "import *"
    # (will not include ffi and lib)
    __all__ = []
    _export_mpr()
