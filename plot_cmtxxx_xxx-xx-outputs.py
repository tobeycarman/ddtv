#!/usr/bin/env python

# July 2014
# Tobey Carman
# Spatial Ecology Lab
# University of Alaska Fairbanks

# Script to plot "cmt***_***_**.nc" files - netcdf files with a certain set of
# dimensions - that are created by dvmdostem.
# - The first set of stars denotes the type of variables: env, bgc, or dim
# - The second set of stars denotes the time resolution: dly, mly, yly
# - The third set of starts denotes the run stage: eq, sp, tr, sc


import sys      # for exit()
import os       # for path, basename
import argparse
import logging
import warnings
import textwrap

import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MaxNLocator

from IPython import embed

class FPlogger:
  '''A mini class for logging floating point warnings.'''
  def write(self, s):
    s = s[0:-1] # strip newline that comes from
    logging.warn("%s" % s)


def main(args):

  # Make numpy report all floating point errors to the log
  # NOTE: warnings were coming up due to tiny data ranges (below machine epsilon)
  np.seterr(all='log')
  np.seterrcall(FPlogger()) # pass an object that implements the write method

  # define some variable sets to plot
  varsets = {
    'N': [
        'NMOBIL', 'NRESORB', 'NUPTAKESALL', 'NUPTAKEL', 'VEGNSUM', 'NETNMIN',
        'LTRFALNALL', 'AVLNSUM', 'AVLNINPUT', 'AVLNLOST', 'ORGNLOST'
    ],
    'C': [
        'NEP', 'NPPALL', 'GPPALL', 'VEGCSUM', 'LTRFALCALL', 'SOMCSHLW',
        'SOMCDEEP', 'SOMCMINEA', 'SOMCMINEC', 'RHMOIST', 'RHQ10', 'SOILLTRFCN'
    ],
    'E': [
        'SNOWFALL','RAINFALL','EETTOTAL','PETTOTAL','TAIR','SOILTAVE',
        'SOILVWC','RZTHAWPCT','ALD',
    ]
  }

  if args.report:
    report_on_file(args)
    sys.exit(0)

  if 'E' == args.varset:
    logging.info("Make sure the cmt file is the right one!")

  logging.debug("Loading netcdf file (%s)..." % args.inputfile)
  dsA = nc.Dataset(args.inputfile)
  titlestring = "%s" % (args.inputfile)

  if args.stitch:
    logging.info("Attempting to stitch stages %s onto inputfile before displaying..." % (args.stitch))

    logging.debug("Create a temporary file to concatenate everything into...")
    tmpdata = nc.Dataset('/tmp/junk.nc', 'w')

    logging.info("Make sure the right files exist...")
    inputdir = os.path.split(args.inputfile)[0]
    bn = os.path.basename(args.inputfile)  # e.g.: 'cmtbgc_yly-eq.nc'
    for stage in args.stitch:
      sn = "%s-%s.nc" % (bn[0:10], stage)
      if not os.path.exists(os.path.join(inputdir,sn)):
        logging.error("File %s does not exist in %s!" % (sn, inputdir))
        logging.error("Cannot perform file stitching. Quitting...")
        sys.exit(-1)
      else:
        logging.info("File exists for stitching...")
        titlestring += "\n%s" % (os.path.join(inputdir,sn))


    logging.debug("Copy the dimensions from dataset A in to the temporary file...")
    for d in dsA.dimensions:
      if 'tstep' == d:
        tmpdata.createDimension(d, None)
      else:
        tmpdata.createDimension(d, len(dsA.dimensions[d]))

    logging.info("Copy values from first input file to tmpdata...")
    if not 'YEAR' in tmpdata.variables:
      tmpdata.createVariable('YEAR', 'i', dsA.variables['YEAR'].dimensions)
    tmpdata.variables['YEAR'][:] = dsA.variables['YEAR'][:]

    for v in varsets[args.varset]:
      print v
      if not v in tmpdata.variables:
        tmpdata.createVariable(v, 'f', dsA.variables[v].dimensions)
      if dsA.variables[v].dimensions[0] == 'tstep':
        tmpdata.variables[v][:] = dsA.variables[v][:]
        logging.info("tmpdata.variables[%s].shape: %s" % (v, tmpdata.variables[v].shape))


    logging.debug("Process each requested stage to stitch together...")
    stage_end_indices = ''
    for stage in args.stitch:
      seidx = len(tmpdata.dimensions['tstep'])
      stage_end_indices += '%i ' % seidx # make space delimited string of end of stage
                                 # indices

      logging.info("First getting time axis data...")
      if not 'YEAR' in tmpdata.variables:
        tmpdata.createVariable('YEAR', 'f', dsA.variables['YEAR'].dimensions)

      tmpdata.variables['YEAR'][seidx:] = get_more_data(stage, 'YEAR', args)

      logging.info("Next, getting all other variables in the var set...")
      for v in varsets[args.varset]:
        if not v in tmpdata.variables:
          tmpdata.createVariable(v, 'f', dsA.variables[v].dimensions)
        if dsA.variables[v].dimensions[0] == 'tstep':
          tmpdata.variables[v][seidx:] = get_more_data(stage, v, args)
          logging.info("tmpdata.variables[%s].shape: %s" % (v, tmpdata.variables[v].shape))

    del dsA
    dsA = tmpdata


  logging.debug("Accquiring figure and subplot objects...")
  fig, axar = plt.subplots(6, 2, sharex=True)

  logging.debug("Setup figure title...")
  fig.suptitle(titlestring)

  # Would like to label xaxis with these:
  xdata = dsA.variables['YEAR'][:]

  logging.info("%s years: [%s ... %s]" % (len(xdata), xdata[0:3], xdata[-3:]))

  logging.debug("Plot each variable in the variable set...")
  for i, v in enumerate(varsets[args.varset]):
    row = i % 6
    col = 0 if i < 6 else 1
    ax = axar[row, col]

    logging.debug( "subplot [%s, %s] %s, dims: %s" % (row, col, v, dsA.variables[v].dimensions))

    #logging.debug("choose data to plot based on variable's dimensions...")
    if dsA.variables[v].dimensions == ('tstep','pft','vegpart'):
      data2plot = round_tiny_range(dsA.variables[v][:,args.pft,0])
      linecollection = ax.plot(data2plot)
      ax.set_title('%s %s %s '%(v, 'PFT', args.pft), fontdict={'fontsize':8})

    elif dsA.variables[v].dimensions == ('tstep','pft'):
      data2plot = round_tiny_range(dsA.variables[v][:,args.pft])
      linecollection = ax.plot(data2plot)
      ax.set_title('%s %s %s '%(v, 'PFT', args.pft), fontdict={'fontsize':8})

    elif dsA.variables[v].dimensions == ('tstep',):
      data2plot = round_tiny_range(dsA.variables[v][:])
      linecollection = ax.plot(data2plot)
      ax.set_title(v, fontdict={'fontsize':8})

    elif dsA.variables[v].dimensions == ('tstep','soilayer'):
      data2plot = round_tiny_range(dsA.variables[v][:,0])
      linecollection = ax.plot(data2plot)
      ax.set_title('%s %s %s '%(v, 'layer', 0), fontdict={'fontsize':8})

    else:
      logging.error("unknown dimensions for variable %s." % v)

    logging.debug("setting the max number of ticks for x and y axes...")
    ax.yaxis.set_major_locator(MaxNLocator(nbins=4, prune='both'))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=6, prune='both'))

    if args.stitch:
      logging.debug("Setting the end-of-stage marker lines...")
      for seidx in stage_end_indices.split():
        ax.axvline(seidx, color='red')



  for row in axar:
    for ax in row:
      if 0 == len(ax.lines):
        logging.debug("Turn off empty axes...")
        ax.set_visible(False)

      logging.debug("Adjust font size for axes tick labels")
      plt.setp(ax.get_yticklabels(), fontsize=8)
      plt.setp(ax.get_xticklabels(), fontsize=8)

  topadj = 0.92 - 0.025*len(titlestring.splitlines())
  print topadj
  fig.subplots_adjust(top=topadj)
  fig.subplots_adjust(hspace=.5)

  if args.save:
    saved_file_name = "plot_cmt.png"
    print "Savging plot as '%s'..." % saved_file_name
    plt.savefig(saved_file_name, dpi=72)

  if args.display:
    print "Showing plot..."
    plt.show()

  # if args.dumpcsv:
  # possible psuedo code:
  # for each subplot
  #   make file name, comments, etc
  #   make np array to accumulate data
  #   for each line in each subplots
  #     get label
  #     get xydata, add to np array
  #   np.savetxt()

#
# Utility functions...
#

def round_tiny_range(data):
  # http://stackoverflow.com/questions/10555659/python-arithmetic-with-small-numbers
  mn = min(data)
  mx = max(data)
  logging.debug("min: %s, max: %s " % (mn, mx))
  datarange = np.abs(mx - mn)
  if (datarange < np.finfo(np.float).eps):
    logging.warn("The data range is tiny! Less than this machine's epsilopn!")
    logging.warn("Replacing data with new values of %s size, rounded to 14 decimals" % mn)
    adj = np.empty(len(data))
    adj.fill(np.around(mn, decimals=14))
    return adj
  else:
    # range is larger than epsilon, just return original data
    return data


def validate_outputnc_file(file):
  ds = nc.Dataset(file)
  try:
    # check correct dimensions
    assert set(ds.dimensions.keys()) == set(['PFTS', 'CHTID', 'YEAR', 'YYYYMM'])

  except AssertionError as e:
    print "Problem with NetCDF file shape! Quitting."

def determine_stage(filename):
  stage = os.path.basename(filename)[-5:-3]
  if stage in ['eq','sp','tr','sc']:
    return stage
  else:
    return 'unknown'

def determine_timeres(filename):
  timeres = os.path.basename(filename)[-9:-6]
  if timeres in ['yly','mly','dly']:
    return timeres
  else:
    return 'unknown'

def report_on_file(args):
  ds = nc.Dataset(args.inputfile)

  print "-- File report for: %s" % args.inputfile
  print "- runstage: ", determine_stage(args.inputfile)
  print "- timestep: ", determine_timeres(args.inputfile)
  print "- dimensions (size)"
  for d in ds.dimensions:
    print "   ", d, "(%s)" % len(ds.dimensions[d])


# deprecated...
def set_bg_tag_txt(ax, tag, num):
  #logging.debug("set the background 'PFTx' text for axes that are plotting pft specific variables.")
  font = {
    'family' : 'sans-serif',
    'color'  : 'black',
    'weight' : 'bold',
    'size'   : 18,
    'alpha'  : 0.5,
  }

  ax.text(
      0.5, 0.5,
      "%s %s" % (tag, num),
      fontdict=font,
      horizontalalignment='center',
      #verticalalignment='top',
      transform=ax.transAxes,
      #bbox=dict(facecolor='red', alpha=0.2)
  )

def get_more_data(stage, var, args):
  '''Based on stage and variable, returns an array of data from a cmt file.'''

  inputdir = os.path.split(args.inputfile)[0]
  bn = os.path.basename(args.inputfile)  # e.g.: 'cmtbgc_yly-eq.nc'

  sn = "%s-%s.nc" % (bn[0:10], stage)
  logging.info("Looking for %s in file %s" % (var, os.path.join(inputdir, sn)))
  d = nc.Dataset(os.path.join(inputdir,sn))
  logging.info("Found! Returning dataset for %s. (Shape: %s)" % (var, d.variables[var].shape))

  return d.variables[var][:]



if __name__ == '__main__':
  logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

  parser = argparse.ArgumentParser(description=textwrap.dedent('''\
      Plots a cmt***_***-**.nc file from dvmdostem. The script has three 
      different "variable sets" it can plot (C, N, E) related to Carbon, 
      Nitrogen, Environmental variables respectively. The script can optionally 
      stitch data from other cmt***_***-**.nc files onto the end of the plot 
      (plot data from multiple files consecutively on one time series/axis).'''))

  parser.add_argument('-r', '--report', action='store_true',
      help=textwrap.dedent('''\
      Read the input netCDF file, reporting on the runstage, time resolution,
      and dimensions of the file. Deduces runstage and time resolution from 
      file name.'''))

  parser.add_argument('-p', '--pft', default=0, required=False, type=int, metavar='N',
      help="For pft variables, which pft to show (0-9)")

  parser.add_argument('-v', '--varset', default='C', choices=['C','N','E'],
      help="Choose the 'variable set' to plot (Carbon, Nitrogen, Environmental")

  parser.add_argument('-d', '--display', action='store_true',
      help="Display the plot")
  parser.add_argument('-s', '--save', action='store_true',
      help="Save the plot with generic name. Warning: will overwrite existing file with same name!!")

#  parser.add_argument('-s', '--startyr', default=0, required=False, type=int, metavar='N',
#      help="Which year to start with. Defaults to 0, for all years. (will show env only warmup)")
#  parser.add_argument('-e', '--endyr', default=None, required=False, type=int, metavar='N',
#      help="Which year to end with. Defaults to None, for all years. (will read everything in the file)")

  parser.add_argument('inputfile', help=textwrap.dedent(''' Path to a 
      cmtxxx_xxx-xx.nc file produced by dvmdostem.'''))

  parser.add_argument('--stitch', required=False,
      nargs='+',
      help=textwrap.dedent('''\
        Look for other files of the subsequent runstages in the same directory
        as the inputfile. If found, stitch the data together along the time
        dimension, and plot the resulting timeseries.'''))


  logging.debug("Parsing command line...")
  args = parser.parse_args()


  main(args)




