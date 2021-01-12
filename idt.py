import ctypes

_sum = ctypes.CDLL('libsum.so')

result = _sum.connect()

