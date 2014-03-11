#!/usr/bin/env python

import os
import glob
import json

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mplticker

#from IPython import embed

def YYYY_MM2idx(s):
  '''Convert 'YYYY_MM' string to index, assuming year and month start at 0
     
     0000_00 --> index 0 (jan, year 0)
     0001_00 --> index 12 (jan of year 1)
     etc...
  '''
  year = int(s[0:4])
  month = int(s[5:])
  return (year * 12) + month


class CalibrationFigure(object):
  ''' A generic figure that provides the general display and scaling for
  a dynamically updating "calibration plot" for dvm-dos-tem.
  
  Subclass this for plotting different groups of traces. The plot has the ability
  to rescale if more data is added.
  '''
  
  def __init__(self, timerange):
    self._fig, self._axes = plt.subplots(4,1,sharex='all')
    self._fig.suptitle('4 empty plots...')

    self._timerange = timerange
    
    # build an empty container
    empty_series = np.empty(self._timerange)
    empty_series.fill(np.nan)
  
    self._traces = [
      {
        'jsontag': 'sample',
        'data': empty_series.copy(),
        'artist': self._axes[0].plot( [],[], label="make more of these..." )
      },
    ]
    
    
    
  def figure(self):
    '''Returns a figure instance. Useful for the first arg to FuncAnimation.'''
    return self._fig

  def empty(self):
    '''Sets all artist's data to empty and returns an artist list'''
    for ax in self._axes:
      ax.set_data([],[])
    
    artist_list = [ trace['artist'] for trace in self._traces ]
    return artist_list
 
  def load_data(self):
    '''Checks all json files in a directory and returns true if it finds any 
    a json file with any data that is not loaded into the self's traces' data
    containers.'''
    did_load_more_data = False    

    for file in glob.glob('/tmp/cal-dvmdostem/*.json'):
      base = os.path.basename(file)              # YYYY_MM.json
      idx = YYYY_MM2idx( os.path.splitext(base)[0] )  # 0 based month number

      if idx > self._timerange:
        print "idx(%i) > self._timerange(%i)! Rescaling..." % (idx, self._timerange)
        self.rescale()
        print "new timerange: %s" % self._timerange

      if idx < self._timerange:

       for trace in self._traces:
          if ( np.isnan(trace['data'][idx]) ):
            with open(file) as f:
              new_data = json.load(f)
          
            trace['data'][idx] = new_data[ trace['jsontag'] ]
            did_load_more_data = True
      else:
        pass    
    return did_load_more_data
    
  def update(self, frame):
    print "frame[%i]" % frame, 

    if self.load_data():
      print "loaded new data..."
      t = np.arange(1, self._timerange + 1)
      for trace in self._traces:
        a = trace['artist'][0]  # <-- not sure why this is a list?
        a.set_data( t, trace['data'] )

    else:
      print "no new data loaded..."
    artist_list = [ trace['artist'] for trace in self._traces ]
    return artist_list
      
  def rescale(self, percent=0.25):
    i = int(percent * self._timerange)
    self._timerange += i
    new_container = np.empty(self._timerange)
    new_container.fill(np.nan)
    
    for trace in self._traces:
      new_container[0:len(trace['data']) ] = trace['data']
      trace['data'] = new_container

    self.set_all_axis_limits_and_tickers()

  def set_all_axis_limits_and_tickers(self):

    loc = mplticker.MultipleLocator(base=120)
    t = np.arange(1, self._timerange + 1) 

    for ax in self._axes:
      ax.set_xlim(t[0], t[-1])
      ax.set_ylim(-1,200)
      ax.xaxis.set_major_locator(loc)
      l = ax.legend()
      
      
      
      
      
      
      
      
      
      

