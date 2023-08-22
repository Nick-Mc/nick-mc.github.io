from ._importlib import metadata

try:
<<<<<<< HEAD
    __version__ = metadata.version('setuptools')
except Exception:
    __version__ = 'unknown'
=======
    __version__ = metadata.version('setuptools') or '0.dev0+unknown'
except Exception:
    __version__ = '0.dev0+unknown'
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)
