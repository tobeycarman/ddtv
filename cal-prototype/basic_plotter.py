#!/usr/bin/env python


import os
import time
import json
import collections # for deque


import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#import pandas as pd

from IPython import embed


def animate(frame, mod_time, timespan, data_list, line_list):
  #print frame
  #print mod_time
  #print timespan
  #print series_list
  #print type(data_list), "-->", type(data_list[0])
  #print type(line_list), "-->", type(line_list[0])
  #print line_list


  if os.stat('pass_thru.json').st_mtime == mod_time:
    print "No change in pass thru file...nothing to do..."
    return line_list[0], line_list[1]
  else:
    print "Pass thru file changed! "

    # update the modification time
    print "update the modification time"
    mod_time = os.stat('pass_thru.json').st_mtime
    
    # trim data from full deques  
    for s in data_list:
      if len(s) >= timespan:
        print "Trimming data from a full deque..."
        s.popleft()

    print "getting the existing data..."
    gppD = data_list[0]
    nppD = data_list[1]
    
    # read the freshly modified file
    print "open pass thru file..."
    with open('pass_thru.json') as infile:
      
      d = json.load(infile)
      #print d['gpp']
      
      # add new data that we just read from the file.
      # ( not provision for skipped years/months? )
      gppD.append( float(d['gpp']) )      
      nppD.append( float(d['npp']) )
      print "read pass thru file and append new data to data deque..."
    #print np.array(gppD)[0:10], "...", np.array(gppD)[-10:] 
    
    print "set the line's ydata to the new values..."  
    line_list[0].set_ydata( np.array(gppD) )
    line_list[0].set_xdata( np.arange(len(gppD)) )
    line_list[1].set_ydata( np.array(nppD) )
    #embed()
    print "returning lines..."
    #print line_list[0].get_ydata()[-10:]
    return line_list[0], line_list[1]


def init():
  line  


def main():

  timespan = 12 * 100

  empty_series = np.empty(timespan)
  empty_series.fill(np.nan)

  xrange = np.arange(1, timespan+1)

  gpp_deque = collections.deque(empty_series.copy(), timespan)
  npp_deque = collections.deque(empty_series.copy(), timespan)
  
  fig, axes = plt.subplots(nrows=2)

#   for ax in axes:
#     ax.set_ylim(0,1)
  
  #gppL, = axes[0].plot([],[], 'r', label='GPP', lw=2)
  #nppL, = axes[1].plot([],[], 'b', label='NPP')

  gppL, = axes[0].plot(xrange, np.array(gpp_deque), 'r', label='GPP')
  nppL, = axes[1].plot(xrange, np.array(npp_deque), 'b', label='NPP')
  
  axes[0].set_xlim(1,1200)
  axes[0].set_ylim(0, 1)  
  axes[1].set_xlim(1,1200)
  axes[1].set_ylim(0, 1)
  
  #embed()
  
  mt = os.stat('pass_thru.json').st_mtime

  ani = animation.FuncAnimation(fig, animate, blit=True, interval=100,
      fargs=(mt, timespan, (gpp_deque, npp_deque), (gppL, nppL)))       
  
  
  plt.show()
  
  

if __name__ == '__main__':
  main()