import ctypes

_lib = ctypes.CDLL('libsum.so')

result = _lib.connect()

