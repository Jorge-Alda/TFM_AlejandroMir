#!/usr/bin/env python

import sys


def suma(x):
    return sum(float(i) for i in x)


if __name__ == '__main__':
    print(sys.argv)
    if sys.argv[1] == 'suma':
        s = suma(sys.argv[2:])
        print(s)
