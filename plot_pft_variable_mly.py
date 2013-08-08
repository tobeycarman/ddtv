#!/usr/bin/env python

# Tobey Carman
# Spatial Ecology Lab
# Aug 2013

try:
  import os
  import sys
  import string
  import math
  import argparse

  import netCDF4 as nc
  import numpy as np
  import matplotlib.pyplot as plt
  from matplotlib.ticker import MultipleLocator, FormatStrFormatter

except ImportError as e:
  print "%s" % e
  sys.exit()


def main():
  parser = argparse.ArgumentParser(description='''Plots a variable vs. time for  
each PFT in a cohort (left axis). The right axis plots the PFT's percent 
coverage. If there are 10 PFTs, there will be 10 plots generated.

There are two modes: "normal" and "explorer".

In "normal" mode, the min and max for each plot are determined by the min and 
max among all PFTs. In "explorer" mode, the y axis of each PFT plot will auto-
scale to the range for only that PFT.''')

  group = parser.add_mutually_exclusive_group()
  group.add_argument('-n', '--normal', action="store_true")
  group.add_argument('-e', '--explorer', action="store_true")


  parser.add_argument('-d', '--display', action='store_true', help="Display the plot")
  parser.add_argument('-s', '--save', default=False, help="Save the plot to simple-plot.png")
  parser.add_argument('-c', '--cohort', required=True, type=int, help='Which cohort to plot')
  parser.add_argument('-v', '--variable', default='NPP', help="Which variable to plot")
  parser.add_argument('inputfile', help='the file to read from')

  args = parser.parse_args()
  #print args
  
  print "Loading dataset..."
  ds = nc.Dataset(args.inputfile)
  
  var = args.variable
  
  time_range = np.arange(0, len(ds.dimensions['YYYYMM']))  
  num_pfts = len(ds.dimensions['PFTS'])

  plt.rcParams['figure.figsize'] = 9, 12 # w, h

  # GET A FIGURE AND ARRAY OF AXES TO WORK WITH 
  fig, axesarr = plt.subplots(num_pfts, 1, sharex=True)
  
  # MAKE ANOTHER ARRAY OF AXES FOR THE COVERAGE PLOTS 
  covaxesarr = [axe.twinx() for axe in axesarr]
   
  fig.subplots_adjust(hspace=.5)
  fig.suptitle('%s cohort %s'%(var, args.cohort), fontsize=20)

  print "Extracting data for each PFT..."
  for pft in range(num_pfts):
    # pull some data out to plot
    pft_series = ds.variables[var][args.cohort, :, pft]
    pft_cov = 100*ds.variables['VEGFRAC'][args.cohort, :, pft]

    # Axes instances to work with cax -> "current axes"
    cax1 = axesarr[pft]    # the variable data axes
    cax2 = covaxesarr[pft] # the coverage data axes

    # plot the PFT's variable data vs time
    cax1.plot(time_range, pft_series, 'b', label='pft%s'%pft)
    # set tick colors
    for tl in cax1.get_yticklabels():
      tl.set_color('b')
      tl.set_size(10)

    # plot the PFT's coverage data vs time (x axis is shared)
    cax2.plot(time_range, pft_cov, linestyle=':', color='0.75', label='pft%s cov'%pft)
    # set tick colors
    for tl in cax2.get_yticklabels():
      tl.set_color('0.0')
      tl.set_size(10)
    
    # control # of tics and labels on y axis,
    cax1.yaxis.set_major_locator(plt.MaxNLocator(2))
    cax1.set_ylabel('pft%s'%pft)#, fontsize=16)

    # since coverage seems to often be 0 or 100, expand the range
    # so that the trace is visible
    cax2.set_yticks(np.arange(-10, 111))
    cax2.yaxis.set_major_locator(plt.MaxNLocator(2))

    

  # done looping setting up individual plots...
  if (args.normal):
    print "Finding the 'global' max and min..."
    maxes = [max(ds.variables[var][args.cohort, :, pft]) for pft in range(num_pfts)]
    mx = max(maxes)

    mins = [min(ds.variables[var][args.cohort, :, pft]) for pft in range(num_pfts)]
    mn = min(mins)

    print "Looping over the axes instance array and setting tick marks..."
    for cax in axesarr:
      cax.yaxis.set_major_locator(plt.MaxNLocator(4))
      cax.set_yticks(np.arange(mn, mx+1, (abs(mx-mn)/4) ) )
         
  
  # set the x axis label. this labels only the bottom plot,
  # but all the other plots get tick marks.
  # have it make tick marks at year boundaries (every 12 months)
  plt.xticks(np.arange(0,len(ds.dimensions['YYYYMM']),12) )
  
  # for some reason plt.xlabel('blah') does nothing, so to put on the 
  # label at the bottom of the plot, we simply add it to the last 
  # element in the axes array
  axesarr[-1].set_xlabel("time (months)")

  if (args.display):
    print "Displaying..."
    plt.show()

  if (args.save):
    outputfile = args.save
    print "Saving %s..." % outputfile
    plt.savefig(outputfile, dpi=300)

  
    
if __name__ == "__main__":
  main()

