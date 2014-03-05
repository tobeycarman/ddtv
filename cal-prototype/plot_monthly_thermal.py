#!/usr/bin/env python

import os
import glob
import json

import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from IPython import embed

def ym2idx(s):
  year = int(s[0:4])
  month = int(s[5:])
  return (year * 12) + month


def myfunc(frame, plotitems):
  for file in glob.glob('../../testing/*.json'):
    base = os.path.basename(file)              # YYYY_MM.json
    idx = ym2idx( os.path.splitext(base)[0] )  # 0 based month number
    #print file, idx

    for v in plotitems:
      if ( np.isnan(v['data'][idx]) ):

        with open(file) as infile:
          #print "loading ", file
          new_data = json.load(infile)
  
          
        v['data'][idx] = new_data[v['jsontag']]
    
    for v in plotitems:
      l = v['artist'][0]
      l.set_ydata(v['data'])

  artist_list = [p['artist'][0] for p in plotitems]  
  return artist_list

  

def main():

  timespan = 12 * 100  # monthly data for 100 years

  xrange = np.arange(1, timespan+1)  # make a one based index for month number
                                     # useful for x axis labeling

  # build an empty container
  empty_series = np.empty(timespan)
  empty_series.fill(np.nan)

  # container for each variable to plot
  minLayerTemp = empty_series.copy()
  orgLayerTemp = empty_series.copy()
  airTemp = empty_series.copy()
  par = empty_series.copy()
  activeLayerDepth = empty_series.copy()
  
  fig, axes = plt.subplots(4,1,sharex='all')
  
  fig.suptitle('Monthly Thermal')
    
  mineralLayerTempLine  = axes[0].plot(xrange, minLayerTemp, label='Mineral Layer Temp')

  orgLayerTempLine      = axes[1].plot(xrange, orgLayerTemp, label='Organic Layer Temp')
  airTempLine           = axes[1].plot(xrange, airTemp, label='Air Temp')
  
  parLine               = axes[2].plot(xrange, par, label='Photosyntehtically Active Radiation')
  activeLayerDepthLine  = axes[3].plot(xrange, activeLayerDepth, label='Active Layer Depth')

  # all axes/subplots have the same x axis range
  for ax in axes:
    ax.set_xlim(xrange[0], xrange[-1])
    ax.set_ylim(-1,200)
    #ax.legend()

  # a convenient package of data, artists and tags to send to the animator
  update_stuff = [ 
    {'jsontag': 'TempMineralLayer',
     'data': minLayerTemp,
     'artist': mineralLayerTempLine, },

    {'jsontag': 'TempOrganicLayer',
     'data': orgLayerTemp,
     'artist': orgLayerTempLine, },
    {'jsontag': 'TempAir',
     'data': airTemp,
     'artist': airTempLine, },

    {'jsontag': 'PAR',
     'data': par,
     'artist': parLine, },

    {'jsontag': 'ActiveLayerDepth',
     'data': activeLayerDepth,
     'artist': activeLayerDepthLine, },
  ]

  ani = animation.FuncAnimation(fig, myfunc, blit=True, interval=10, fargs=(update_stuff,) )    
  
  for ax in axes:
    ax.legend()
  
  plt.show()
  
  

if __name__ == '__main__':
  main()