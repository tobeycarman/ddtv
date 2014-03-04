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


def animate(frame, mod_time, timespan, sock, data_list, line_list):
  #print frame
  #print mod_time
  #print timespan
  #print series_list
  #print type(data_list), "-->", type(data_list[0])
  #print type(line_list), "-->", type(line_list[0])
  #print line_list
  
  string = sock.recv_string()
  d = json.loads(string)

  gppD = data_list[0]
  nppD = data_list[1]


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
    gppD[idx] = d['gpp']
    nppD[idx] = d['npp']
        
    print "set the line's ydata to the new values..."  
    line_list[0].set_ydata(gppD)
    #line_list[0].set_xdata(gppD)
    line_list[1].set_ydata( nppD )
    #embed()
    print "returning lines..."
    #print line_list[0].get_ydata()[-10:]
  return line_list[0], line_list[1]



def main():


  import sys
  import zmq

  #  Socket to talk to server
  context = zmq.Context()
  socket = context.socket(zmq.SUB)

  print("Collecting updates from dmv-dos-tem server...")
  socket.connect("tcp://localhost:5556")

  # Subscribe to zipcode, default is NYC, 10001
  #zip_filter = sys.argv[1] if len(sys.argv) > 1 else "10001"

  # Python 2 - ascii bytes to unicode str
  filter = ''
  if isinstance(filter, bytes):
      filter = filter.decode('ascii')
  
  socket.setsockopt_string(zmq.SUBSCRIBE, filter)

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
  
  #embed()
  
  mt = os.stat('pass_thru.json').st_mtime

  ani = animation.FuncAnimation(fig, animate, blit=True, interval=10,
      fargs=(mt, timespan, socket, (gppData, nppData), (gppL, nppL)))       
  
  
  plt.show()
  
  

if __name__ == '__main__':
  main()