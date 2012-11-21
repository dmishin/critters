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

def make_func( values ):
    f = BinaryBlockFunc()
    f.set(values)
    return f

def make_rfinv_func( inv_0, #Inverse or not 0000, 1111 blocks
                     inv_2, #inverse or not 1100, 0011, 0101, 1010 blocks
                     inv_2d, #inverse or not diagonal s=2 blocks
                     inv_13, #inverse or not s=1 and s=3 blocks
                     rot_1, #rotate180 or not s=1 blocks
                     rot_3  
                     ):
    """ """
    vals = list(range(16))
    def inv(x):
        return x ^ 0xf
    def rot(x):
        y = x & 0x1
        x = x >> 1
        y = (y << 1) | (x & 0x1)
        x = x >> 1
        y = (y << 1) | (x & 0x1)
        x = x >> 1
        y = (y << 1) | (x & 0x1)
        return y
    def inv_i(i):
        vals[i] = inv(vals[i])
    def rot_i(i):
        vals[i] = rot(vals[i])
    def bin(s):
        return int(s,2)
    if inv_0:
        inv_i(bin('0000'))
        inv_i(bin('1111'))
    if inv_2:
        inv_i(bin('1100'))
        inv_i(bin('0011'))
        inv_i(bin('0101'))
        inv_i(bin('1010'))
    if inv_2d:
        inv_i(bin('1001'))
        inv_i(bin('0110'))
    if inv_13:
        inv_i(bin('1000'))
        inv_i(bin('0100'))
        inv_i(bin('0010'))
        inv_i(bin('0001'))
        inv_i(bin('0111'))
        inv_i(bin('1011'))
        inv_i(bin('1101'))
        inv_i(bin('1110'))
    if rot_1:
        rot_i(bin('1000'))
        rot_i(bin('0100'))
        rot_i(bin('0010'))
        rot_i(bin('0001'))
    if rot_3:
        rot_i(bin('0111'))
        rot_i(bin('1011'))
        rot_i(bin('1101'))
        rot_i(bin('1110'))
    assert( list(sorted(vals)) == list(range(16)))
    return make_func( vals )
              
                         


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

