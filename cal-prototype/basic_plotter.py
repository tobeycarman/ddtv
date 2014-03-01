#!/usr/bin/env python

import json

import os
import time

#import numpy as np
#import matplotlib.pyplot as plt


def main():

  mt = os.stat('pass_thru.json').st_mtime

  plotdata = {}

  while True:
    time.sleep(0.5)
    if os.stat('pass_thru.json').st_mtime == mt:
      print "[PLOTTER] No change in pass thru file...nothing to do..."

      pass # nothing to do
    else:
      mt = os.stat('pass_thru.json').st_mtime
      with open('pass_thru.json') as infile:
        d = json.load(infile)
        
      print d['year'], d['month'], d['gpp']
      plotdata[(d['year'], d['month'])] = d['gpp']
  
      print "[PLOTTER] added to the local data. new length: ", len(plotdata)


if __name__ == '__main__':
  main()