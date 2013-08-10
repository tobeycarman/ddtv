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
  parser = argparse.ArgumentParser(description='''Makes a heatmap for a single
  variable, and a single PFT. The heatmap is a time vs. time heatmap with years
  on the vertical axis and months on the horizontal axis. The color of each
  pixel in this grid corresponds to the variables value at that month, and year.
  
  This plot is good for looking at seasonal trends in longer time series data.
  ''')

  #group = parser.add_mutually_exclusive_group()
  #group.add_argument('-n', '--normal', action="store_true")
  #group.add_argument('-e', '--explorer', action="store_true")

  parser.add_argument('-d', '--display', action='store_true', help="Display the plot")
  parser.add_argument('-s', '--save', default=False, help="Save the plot to the file name you provide")

  parser.add_argument('-c', '--cohort', required=True, type=int, help='Which cohort to plot')
  parser.add_argument('-v', '--variable', default='NPP', help="Which variable to plot")
  parser.add_argument('-pft', type=int, default=0, help="Which PFT to display data for.")

  parser.add_argument('inputfile', help='path to a NetCDF file to read from (A).')
  #parser.add_argument('--compare', default=None, help='path to a NetCDF file to compare to (B).')

  args = parser.parse_args()
  print args
  
  print "Loading dataset..."
  dsA = nc.Dataset(args.inputfile)
  #if (args.compare != None):
  #  dsB = nc.Dataset(args.compare)
  
  print '(A): ', args.inputfile
  #print '(B): ', args.compare 
  args.variable
  
  time_range = np.arange(0, len(dsA.dimensions['YYYYMM']))  
  #num_pfts = len(dsA.dimensions['PFTS'])

  #plt.rcParams['figure.figsize'] = 9, 12 # w, h

  # GET A FIGURE AND ARRAY OF AXES TO WORK WITH 
  fig, curax = plt.subplots(1, 1)
  
  #fig.subplots_adjust(hspace=.5)
  #if args.compare:
  t = '''cohort %s, pft%s, %s
    (A) %s''' % (args.cohort, args.pft, args.variable, args.inputfile)
  
  fig.suptitle(t)

  print "Extracting data..."
  data = dsA.variables[args.variable][args.cohort,:,args.pft]
  print data
  print len(data)
  print data.shape
  img_data = np.reshape(data, (data.shape[0]/12,12))
  print img_data[0]
  print img_data[1]
  
  curax.set_xticks(np.arange(0,12))
  curax.set_xticklabels(['j', 'f', 'm', 'a', 'm','j','j','a','s','o','n','d',])
  curax.set_xlabel('Month')
  curax.set_ylabel('Year')
  
  cmap = plt.cm.jet
  cmap.set_bad('k', .80)
  
  im1 = curax.imshow(img_data, interpolation='nearest', aspect='.1', cmap=cmap)
  curax.set_aspect('auto')
  fig.colorbar(im1)



  if (args.display):
    print "Displaying..."
    plt.show()

  if (args.save):
    outputfile = args.save
    print "Saving %s..." % outputfile
    plt.savefig(outputfile, dpi=300)

  
    
if __name__ == "__main__":
  main()

