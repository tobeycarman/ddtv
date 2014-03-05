#!/usr/bin/env python

import os
import glob
import json

import matplotlib
matplotlib.use('TkAgg')  # this is the only one that seems to work on Mac OSX
                         # with animation...

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from IPython import embed

def YYYY_MM2idx(s):
  year = int(s[0:4])
  month = int(s[5:])
  return (year * 12) + month

class MonthlyHydroFigure(object):
  
  
  def __init__(self, timerange=100):
    self._fig, self._axes = plt.subplots(4,1,sharex='all')
    self._fig.suptitle('Monthly Thermal')

    self._timerange = timerange

    # build an empty container
    empty_series = np.empty(self._timerange)
    empty_series.fill(np.nan)
  
    t = np.arange(1, self._timerange + 1) # plot against a one based index

    self._traces = [
      {
        'jsontag': 'Precipitation',
        'data': empty_series.copy(),
        'artist': self._axes[0].plot( [],[], label="Precip" )
      },
      {
        'jsontag': 'WaterTable',
        'data': empty_series.copy(),
        'artist': self._axes[1].plot( [],[], label="Water Table" )
      },
      {
        'jsontag': 'VWCOrganicLayer',
        'data': empty_series.copy(),
        'artist': self._axes[2].plot( [],[], label="vwc organic layer" )

      },
      {
        'jsontag': 'VWCMineralLayer',
        'data': empty_series.copy(),
        'artist': self._axes[2].plot( [],[], label="vwc mineral layer" )
      },
      {
        'jsontag': 'Evapotranspiration',
        'data': empty_series.copy(),
        'artist': self._axes[3].plot( [],[], label="evapo transpiration" )
      },
    ]
    
    for ax in self._axes:
      ax.set_xlim(t[0], t[-1])
      ax.set_ylim(-1,200)
      l = ax.legend()
      #l.set_zorder(1000)

    
    
  def figure(self):
    '''Returns a figure instance'''
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

    for file in glob.glob('tmp-json/*.json'):
      base = os.path.basename(file)              # YYYY_MM.json
      idx = YYYY_MM2idx( os.path.splitext(base)[0] )  # 0 based month number

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
    
    t = np.arange(1, self._timerange + 1)
    
    
    if self.load_data():
      print "loaded new data..."
      for trace in self._traces:
        a = trace['artist'][0]  # <-- not sure why this is a list?
        a.set_data( t, trace['data'] )

    else:
      print "no new data loaded..."
    artist_list = [ trace['artist'] for trace in self._traces ]
    return artist_list
      



def main():

  timespan = 12 * 100  # monthly data for 100 years

  mhf = MonthlyHydroFigure( timerange=(12*100) )

  
  ani = animation.FuncAnimation( mhf.figure(), 
                                 mhf.update, 
                                 #blit=True, 
                                 #init=mhf.empty, 
                                 interval=100, 
                                 fargs=()
                                )

  print "When is this called?"
  plt.show()
  
  

if __name__ == '__main__':
  main()