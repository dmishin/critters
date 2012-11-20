import ctypes
import numpy
import platform

def load_module(name):
    plat = platform.system()
    if plat == "Linux":
        return ctypes.CDLL("./"+name+".so")
    elif plat == "Windows":
        return ctypes.CDLL(name+".dll")
    else:
        raise ValueError("Don't know platform "+plat)

critters =  load_module( "_critters" )

_uint8_array = numpy.ctypeslib.ndpointer(dtype=numpy.uint8,
                                        flags='C_CONTIGUOUS')

class BinaryBlockFunc(ctypes.Structure):
    _fields_=[("y", ctypes.c_uint8 * 16)]
    def valid(self):
        return _is_func_valid(self)
    def set(self, values):
        values = list(values)
        assert(len(values) == 16)
        for i, v in enumerate(values):
            self.y[i] = v
        assert( self.valid() )

BinaryBlockFuncP = ctypes.POINTER(BinaryBlockFunc)

_eval_even = critters.evaluate_even
_eval_even.argtypes = [BinaryBlockFuncP, _uint8_array, ctypes.c_int, ctypes.c_int ]

_eval_odd = critters.evaluate_odd
_eval_odd.argtypes = [BinaryBlockFuncP, _uint8_array, ctypes.c_int, ctypes.c_int ]

_set_critters_func = critters.set_critters_func
_set_critters_func.argtypes = [BinaryBlockFuncP]

critters_func = BinaryBlockFunc()
_set_critters_func(critters_func)

_is_func_valid = critters.is_func_valid
_is_func_valid.argtypes = [BinaryBlockFuncP]

def eval_even(arr, func=critters_func):
    h, w = arr.shape
    if not _eval_even( func, arr, w, h ):
        raise ValueError("eval_even returned False")

def eval_odd(arr, func=critters_func):
    h, w = arr.shape
    if not _eval_odd( func, arr, w, h ):
        raise ValueError("eval_odd returned False")

def evaluate_steps(F, steps, start_step = 0, func = critters_func):
    for i in xrange(start_step, start_step+steps):
        (eval_even, eval_odd)[i%2](F, func=critters_func)

