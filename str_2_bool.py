#!/usr/bin/env python3
import sys
from simple_argparse import simple_argparse


#/* Return true if input_str are  y, yes, t, true, on, 1,
# *        false if n, no, f, false, off and 0.
# */
def str_2_bool(input_str, raise_exception=False):

    v = input_str
    if hasattr(v, 'lower'):
        v = v.lower()

    if v in ['y', 'yes', 't', 'true', 'on', '1']:
        v = True

    elif v in ['n', 'no', 'f', 'false', 'off', '0']:
        v = False

    else:
        v = bool(v)

    if raise_exception and (not v):
        raise Exception('\"{0}\" was evaluated False!!!'.format(input_str))

    return v


if __name__ == '__main__':
    print(simple_argparse(str_2_bool, sys.argv[1:]))
