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
  import matplotlib.colors
  from matplotlib.ticker import MultipleLocator, FormatStrFormatter

except ImportError as e:
  print "%s" % e
  sys.exit()


def stitch(cht, var, pft, infiles, comparefiles=None):
  '''Grabs the right data from the input files (and compare files).
  
  Returns one (or two if comparing) 2d arrays with all the right data.
  
  The first dimension of the returned array(s) is years.'''

  print "Loading dataset..."  
  if comparefiles:
    ds = nc.Dataset(comparefiles[0], 'r')
    dataB = ds.variables[var][cht, :, pft]
    for i in range(1, len(comparefiles)):
      ds = nc.Dataset(comparefiles[i], 'r')
      data = ds.variables[var][cht, :, pft]
      dataB = np.append(dataB, data, axis=0)

  ds = nc.Dataset(infiles[0], 'r')
  dataA = ds.variables[var][cht, :, pft]
  for i in range(1, len(infiles)):
    ds = nc.Dataset(infiles[i], 'r')
    data = ds.variables[var][cht, :, pft]
    dataA = np.append(dataA, data, axis=0)

  if comparefiles:
    rsa = np.reshape(dataA, (dataA.shape[0]/12,12))
    rsb = np.reshape(dataB, (dataB.shape[0]/12,12))
    return (rsa, rsb)
  else:
    rsa =  np.reshape(dataA, (dataA.shape[0]/12,12))
    #print rsa.shape
    #print "Returning %s years of data" % rsa.shape[0]
    return rsa

def img_plot_polar_A(args, data):
  #img_data = np.reshape(data, (data.shape[0]/12,12)) 
  months, years = np.mgrid[0:2*np.pi:2*np.pi/12,  0:data.shape[0]:1]
  print data.shape
  data = np.transpose(data)
  print data.shape
  #print data[1:,0]
  #print data[0:,0:3]
  # GET A FIGURE AND ARRAY OF AXES TO WORK WITH 
  fig, curax = plt.subplots(1, 1, subplot_kw=dict(projection='polar'))
  t = '''cohort %s, pft%s, %s
    (A) %s''' % (args.cohort, args.pft, args.variable, args.inputfiles)
  fig.suptitle(t)
  
  curax.set_xticks(np.arange(0, 2*np.pi, 2*np.pi/12))
  curax.set_xticklabels(['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'])
  curax.set_xlabel('Month')
  curax.set_ylabel('Year')
  print months.shape, months
  print years.shape, years
  curax.pcolormesh(months, years, data, cmap=plt.cm.jet)
  
  wrapup(args)


def img_plot_polar_B(args, data):

  # GET A FIGURE AND ARRAY OF AXES TO WORK WITH 
  fig, curax = plt.subplots(1, 1, subplot_kw=dict(projection='polar'))
  t = '''cohort %s, pft%s, %s
    (A) %s''' % (args.cohort, args.pft, args.variable, args.inputfiles)
  fig.suptitle(t)
  
  years = data.shape[0]
  print "Now we got this many years: %s" % years
  #img_data = np.reshape(data, (years,12))
  #years = np.arange(0, data.shape[0])
  months = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'] 

  cmap = plt.cm.jet
  cmap.set_bad('k', .80)

  bars = []
  for mi, m in enumerate(months):
    for yi in range(0,years):
      #print data[yi,mi]
      #print type(data[yi,mi])
      #print "working on month %s, year %s: " % (m, yi)
      #print "theta: %s" % (2*np.pi/12)*mi
      #print "rad: %s->%s" % (yi-1, yi)
      a = (0.8,0.8,0.8)
      #norm = matplotlib.colors.Normalize()
      
      c = data[yi,mi]/(data.max()-data.min())
      #print c
      #print type(c)
      c = 1-c
      c = '%0.2f' % (c)
      #print c      
      bars.append(curax.bar((2*np.pi/12)*mi, 1, 
                            width=2*np.pi/18,
                            bottom=yi-1,
                            color=c,                            
                            edgecolor=c,
                            #alpha=.75
                           )
                 )


      
      

  plt.ylim(0,years)
  #curax.set_yticks(np.arange(years))
  #curax.set_xticks(months)

  wrapup(args)

def img_plot_rect(args, data):
  print data.shape
  print data
  print '(A): ', args.inputfiles

  #args.variable
  #time_range = np.arange(0, len(data))
  #num_pfts = len(dsA.dimensions['PFTS'])

  #plt.rcParams['figure.figsize'] = 9, 12 # w, h

  # GET A FIGURE AND ARRAY OF AXES TO WORK WITH 
  fig, curax = plt.subplots(1, 1)

  #fig.subplots_adjust(hspace=.5)
  #if args.compare:
  t = '''cohort %s, pft%s, %s
    (A) %s''' % (args.cohort, args.pft, args.variable, args.inputfiles)

  fig.suptitle(t)

  ##img_data = np.reshape(data, (data.shape[0]/12,12))
  #print img_data[0]
  #print img_data[1]

  curax.set_xticks(np.arange(0,12))
  curax.set_xticklabels(['j', 'f', 'm', 'a', 'm','j','j','a','s','o','n','d',])
  curax.set_xlabel('Month')
  curax.set_ylabel('Year')

  cmap = plt.cm.jet
  cmap.set_bad('k', .80)

  im1 = curax.imshow(data, interpolation='nearest', aspect='.1', cmap=cmap)
  curax.set_aspect('auto')
  fig.colorbar(im1)
  wrapup(args)



def wrapup(args):
  if (args.display):
    print "Displaying..."
    plt.show()

  if (args.save):
    outputfile = args.save
    print "Saving %s..." % outputfile
    plt.savefig(outputfile, dpi=300)

def plot(args, data):
  if args.mode == 'rect':
    img_plot_rect(args, data)
  elif args.mode == 'polar':
    img_plot_polar_B(args, data)


def main():
  parser = argparse.ArgumentParser(description='''Makes a heatmap for a single
  variable, and a single PFT. The heatmap is a time vs. time heatmap with years
  on the vertical axis and months on the horizontal axis. The color of each
  pixel in this grid corresponds to the variables value at that month, and year.
  
  A similar to the example here:
  http://stat-computing.org/dataexpo/2009/posters/wicklin-allison.pdf
  ''')

  #group = parser.add_mutually_exclusive_group()
  #group.add_argument('-n', '--normal', action="store_true")
  #group.add_argument('-e', '--explorer', action="store_true")

  parser.add_argument('-d', '--display', action='store_true', help="Display the plot")
  parser.add_argument('-s', '--save', default=False, help="Save the plot to the file name you provide")

  parser.add_argument('-m', '--mode', default='rect', choices=['rect', 'polar'], help="Whether to use rectangular or polar coords")
  parser.add_argument('-c', '--cohort', required=True, type=int, help='Which cohort to plot')
  parser.add_argument('-v', '--variable', default='NPP', help="Which variable to plot")
  parser.add_argument('-pft', type=int, default=0, help="Which PFT to display data for.")

  parser.add_argument('inputfiles', nargs='+', help='path to one or more NetCDF file(s) to read from (A).')
  parser.add_argument('--compare', nargs='+', default=None, help='path to one or more NetCDF file(s) to compare to (B).')

  args = parser.parse_args()
  print args

  if args.compare:
    dsA, dsB = stitch(cht=args.cohort, 
                      var=args.variable, 
                      pft=args.pft, 
                      infiles=args.inputfiles,comparefiles=args.compare)
  else:
    dsA = stitch(cht=args.cohort, 
                 var=args.variable, 
                 pft=args.pft, 
                 infiles=args.inputfiles)

  # compare_plot() # needs two data arrays, one for each set of files to compare
              # will produce plots with differetn color traces for the compare
              # files

  # plot() # <- will need data array, list of input files?
  # save()

  if args.compare:
    plot_compare(args, data=[dsA, dsB])
  else:
    print "WTFFFFF?"
    plot(args, data=dsA)




  
    
if __name__ == "__main__":
  main()

