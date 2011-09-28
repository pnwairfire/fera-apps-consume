#-------------------------------------------------------------------------------
# Name:        module1
# Author:      kjells
# Created:     21/01/2011
# Purpose:
#-------------------------------------------------------------------------------

import struct
from functools import partial

# (c) 2010 Eric L. Frederich
#
# Python implementation of algorithms detailed here...
# from http://www.cygnus-software.com/papers/comparingfloats/comparingfloats.htm

def c_mem_cast(x, f=None, t=None):
    '''
    do a c-style memory cast

    In Python...

    x = 12.34
    y = c_mem_cast(x, 'd', 'l')

    ... should be equivilent to the following in c...

    double x = 12.34;
    long   y = *(long*)&x;
    '''
    return struct.unpack(t, struct.pack(f, x))[0]

dbl_to_lng = partial(c_mem_cast, f='d', t='l')
lng_to_dbl = partial(c_mem_cast, f='l', t='d')
flt_to_int = partial(c_mem_cast, f='f', t='i')
int_to_flt = partial(c_mem_cast, f='i', t='f')

def ulp_diff_maker(converter, negative_zero):
    '''
    Getting the ulp difference of floats and doubles is similar.
    Only difference if the offset and converter.
    '''
    def the_diff(a, b):

        # Make a integer lexicographically ordered as a twos-complement int
        ai = converter(a)
        if ai < 0:
            ai = negative_zero - ai

        # Make b integer lexicographically ordered as a twos-complement int
        bi = converter(b)
        if bi < 0:
            bi = negative_zero - bi

        return abs(ai - bi)

    return the_diff

def WithinThisManyULP(numberOne, numberTwo, fudgeFactor):
    if numberOne == numberTwo:
        return True
    checker = ulp_diff_maker(flt_to_int, 0x80000000)
    out = checker(numberOne, numberTwo)
    return out < fudgeFactor

def HowManyULP(numberOne, numberTwo):
    checker = ulp_diff_maker(flt_to_int, 0x80000000)
    return checker(numberOne, numberTwo)


def main():
    pass

if __name__ == '__main__':
    main()
