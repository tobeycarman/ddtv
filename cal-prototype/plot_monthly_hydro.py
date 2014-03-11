#!/usr/bin/env python

import matplotlib
matplotlib.use('TkAgg')  # this is the only one that seems to work on Mac OSX
                         # with animation...

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from gpt.CalibrationFigure import CalibrationFigure

from IPython import embed


class MonthlyThermalFigure(CalibrationFigure):
  ''' ???'''

  def __init__(self, timerange=100):
    self._fig, self._axes = plt.subplots(4,1,sharex='all')
    self._fig.suptitle('Monthly Thermal')

    self._timerange = timerange

    # build an empty container
    empty_series = np.empty(self._timerange)
    empty_series.fill(np.nan)

    self._traces = [
      {
       'jsontag': 'TempAir',
       'data': empty_series.copy(),
       'artist': self._axes[0].plot( [],[], label="air temp" ) 
      },
      {
       'jsontag': 'TempOrganicLayer',
       'data': empty_series.copy(),
       'artist': self._axes[0].plot( [],[], label="org. layer temp" )
      },

      {
       'jsontag': 'TempMineralLayer',
       'data': empty_series.copy(),
       'artist': self._axes[1].plot( [],[], label="mineral layer temp" )
      },
      {
       'jsontag': 'PAR',
       'data': empty_series.copy(),
       'artist': self._axes[1].plot( [],[], label="PAR" )
      },
      {
       'jsontag': 'ActiveLayerDepth',
       'data': empty_series.copy(),
       'artist': self._axes[2].plot( [],[], label="active layer depth" )
      },
    ]
  
  
    self.GGGG()
    

class MonthlyHydroFigure(CalibrationFigure):
  
  def __init__(self, timerange=100):
    self._fig, self._axes = plt.subplots(4,1,sharex='all')
    self._fig.suptitle('Monthly Hydro')

    self._timerange = timerange

    # build an empty container
    empty_series = np.empty(self._timerange)
    empty_series.fill(np.nan)
  
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
    
    self.GGGG()



    
      



def main():

  T = 12 * 100  # monthly data for 100 years

#  emf = CalibrationFigure( timerange=10 )

#  mhf = MonthlyHydroFigure( timerange=T )
# 
#   
#   ani = animation.FuncAnimation( mhf.figure(), 
#                                  mhf.update, 
#                                  interval=100, 
#                                  fargs=()
#                                 )


  mtf = MonthlyThermalFigure( timerange=T )

  ani = animation.FuncAnimation( mtf.figure(), 
                                 mtf.update, 
                                 interval=100, 
                                 fargs=()
                                )



  plt.show()
  
  

if __name__ == '__main__':
  main()



