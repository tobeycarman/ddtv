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
    #return line_list[0], line_list[1]
  
  else:
    print "Pass thru file changed! "

    # update the modification time
    print "  update the modification time"
    mod_time = os.stat('pass_thru.json').st_mtime

    gppD = data_list[0]
    nppD = data_list[1]

    
    # read the freshly modified file
    print "  open pass thru file..."
    try:
      with open('pass_thru.json') as infile:
      
        d = json.load(infile)
        #print d['gpp']
        
        year = d['year']
        month = d['month']
        idx = (year * 12) + month
        
        print "Got data!:"
        print "Year: %s, Month: %s, idx: %s" % (year, month, idx)

        if not (idx < len(gppD)):
          print "  ERROR: data from model is out of range!!"
          print "  Doing nothing..."
          #return line_list[0], line_list[1]
        else:
          if (year % 5) == 0:
            print "executing some long process in the plotter and may miss data in pass thru file!!"
            time.sleep(10)
            pass
          else:
            gppD[idx] = d['gpp']
            nppD[idx] = d['npp']
          
          
    except ValueError as e:
      print e
      print "Problem reading pass thru file!!"
    #print np.array(gppD)[0:10], "...", np.array(gppD)[-10:] 
    
    print "set the line's ydata to the new values..."  
    line_list[0].set_ydata(gppD)
    #line_list[0].set_xdata(gppD)
    line_list[1].set_ydata( nppD )
    #embed()
    print "returning lines..."
    #print line_list[0].get_ydata()[-10:]
  return line_list[0], line_list[1]



def main():

  timespan = 12 * 100

  empty_series = np.empty(timespan)
  empty_series.fill(np.nan)

  xrange = np.arange(1, timespan+1)

  gppData = empty_series.copy()
  nppData = empty_series.copy()
  
  fig, axes = plt.subplots(nrows=2)

  ax0 = axes[0]
  ax1 = axes[1]
  
  gppL, = ax0.plot(xrange, gppData, 'r', label='GPP')
  nppL, = ax1.plot(xrange, nppData, 'b', label='NPP')
  
  ax0.set_xlim(1,1200)
  ax0.set_ylim(0, 1)  
  ax1.set_xlim(1,1200)
  ax1.set_ylim(0, 1)
  
  embed()
  
  mt = os.stat('pass_thru.json').st_mtime

  ani = animation.FuncAnimation(fig, animate, blit=True, interval=10,
      fargs=(mt, timespan, (gppData, nppData), (gppL, nppL)))       
  
  
  plt.show()
  
  

if __name__ == '__main__':
  main()