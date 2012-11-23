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
def bits4(x):
    return [ (x >> i) & 0x1 for i in xrange(4)]
def from_bits( *abcd):
    b = 0x1
    y = 0x0
    for bit in abcd:
        if bit:
            y = y | b
        b = b << 1
    return y

TYPE_INVERSE = 0
TYPE_PRESERVE = 1
TYPE_RANDOM = 2

_type2name={
    TYPE_INVERSE : "INV",
    TYPE_PRESERVE: "CONST",
    TYPE_RANDOM: "RAND"
}

class BinaryBlockFunc(ctypes.Structure):
    _fields_=[("y", ctypes.c_uint8 * 16)]
    def valid(self):
        return list(sorted(self.y)) == list(range(16))

    def set(self, values):
        values = list(values)
        assert(len(values) == 16)
        for i, v in enumerate(values):
            self.y[i] = v
        assert( self.valid() )

    def sum_invariance_type(self):
        ftype = None
        is_preserve = True
        is_flipping = True
        for x, y in enumerate(self.y):
            sx = sum(bits4(x))
            sy = sum(bits4(y))
            if sy != sx:
                is_preserve = False
            if sy != 4-sx:
                is_flipping = False
            if not is_preserve and not is_flipping:
                break
        if is_preserve: return TYPE_PRESERVE
        if is_flipping: return TYPE_INVERSE
        return TYPE_RANDOM

    def __str__(self):
        return _type2name[self.sum_invariance_type()] + " " + str(list(self.y))

    def __repr__(self):
        return "make_func(%s)"%(repr(list(self.y)))
            

def make_func( values ):
    f = BinaryBlockFunc()
    f.set(values)
    return f

def make_rinv_func( rfinv_func, 
                    rot2_90,    #bool
                    rot1_angle, #0, 1, -1
                    rot3_angle ):#0, 1, -1
    """From the rotation-flip-invariant function, make a rotation-invariant one"""
    def bin(s):
        return int(s,2)
    ys = list(rfinv_func.y)
    if rot2_90:
        for x in map(bin, ('1100','0101', '1010', '0011')):
            ys[x] = rot90(ys[x], 1)
    if rot1_angle != 0:
        for x in map(bin, ('1000','0100', '0010', '0001')):
            ys[x] = rot90(ys[x], rot1_angle)
    if rot3_angle != 0:
        for x in map(bin, ('0111','1011', '1101', '1110')):
            ys[x] = rot90(ys[x], rot3_angle)

    return make_func( ys )

def inv4(x):
    return x ^ 0xf
    
def rot(x):
    a,b,c,d = bits4(x)
    return from_bits(d,c,b,a)

def rot90(x, direction):
    a,b,c,d = bits4(x)
    # a b  -> c a
    # c d  -> d b
    if direction == 1:
        return from_bits(c, a, d, b)
    elif direction == -1:
        return from_bits(b, d, a, c)
    else: 
        raise ValueError("Bad direction")

def make_rfinv_func( inv_0, #Inverse or not 0000, 1111 blocks
                     inv_2, #inverse or not 1100, 0011, 0101, 1010 blocks
                     inv_2d, #inverse or not diagonal s=2 blocks
                     inv_13, #inverse or not s=1 and s=3 blocks
                     rot_1, #rotate180 or not s=1 blocks
                     rot_3  
                     ):
    """Create a binary transfer function, which is invariant to grid rotations and mirror flips"""
    vals = list(range(16))
    def inv_i(i):
        vals[i] = inv4(vals[i])
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

