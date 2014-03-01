#!/usr/bin/env python

import json

import os
import time

#import numpy as np
#import matplotlib.pyplot as plt


def main():

  mt = os.stat('pass_thru.json').st_mtime

  while True:
    time.sleep(0.5)
    if os.stat('pass_thru.json').st_mtime == mt:
      pass # nothing to do
    else:
      mt = os.stat('pass_thru.json').st_mtime
      with open('pass_thru.json') as infile:
        d = json.load(infile)
      
        print "[PLOTTER] add d to the local data and re-draw plot...", d

if __name__ == '__main__':
  main()