#!/usr/bin/env python

import sys
import time
import collections
import numpy as np
import matplotlib.pyplot as plt



def main():

    while True:
        line = sys.stdin.readline()
        if line == '':
            break
        else:
          print line.split()
          time.sleep(1)
    return 0

if __name__ == '__main__':
        sys.exit(main())