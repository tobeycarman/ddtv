#!/usr/bin/env python


# Tobey Carman, June 2014
# Spatial Ecology Lab

# Quick prototype script for making images to "see" dvm-dos-tem restart files.
# Not meant for any sort of scientific analysis. Simply a way to take a quick
# glance at a netCDF restart file that is generated by the model and get an
# idea of the variables and how things are setup.

import argparse
import textwrap
import itertools

import matplotlib.pyplot as plt
import numpy as np
import netCDF4 as nc
import matplotlib.gridspec as gridspec


import collections


# turns out there is no need to use this - just get a numpy array straight
# from a netcdf variable, slice, and then reshape as needed.
def flat_gen(x):
  '''Generator to flatten arbitrarily deep nested list...'''

  # Basically copied from here:
  # http://stackoverflow.com/questions/16176742/python-3-replacement-for-deprecated-compiler-ast-flatten-function

  # might be dangerous if we have even deeper nested structures - too deep of
  # recursion?? But for now it should work..

  # Note that I encountered some problems testing this in the embedded IPython
  # shell. See here:
  # https://github.com/ipython/ipython/issues/62

  def iselement(e):
    return not(isinstance(e, collections.Iterable) and not isinstance(e, str))
  for el in x:
    if iselement(el):
      yield el
    else:
      for sub in flat_gen(el): yield sub

# try it out:
#print(list(flat_gen(["junk",["nested stuff"],[],[[[],['deep']]]])))



def main(fileA, compareFile):

  dsA = nc.Dataset(fileA)
  if compareFile:
    print "WARNING - NOT IMPLEMENTED YET!!"
    dsB = nc.Dataset(compareFile)

  # make a list of dimesions for every variable in the file
  # reduce to a set of 'dimension groups' that covers all variables in each file
  dim_grpA = set( [dsA.variables[v].dimensions for v in dsA.variables] )

  if compareFile:
    dim_grpB = set([dsB.variables[v].dimensions for v in dsB.varables])
    if dim_grpA != dim_grpB:
      print "WARNING! The two files don't seem to have the same variables/dimensions!"

  dim_grpA_2D = [g for g in dim_grpA if len(g) == 2]
  dim_grpA_3D = [g for g in dim_grpA if len(g) == 3]

  print "2D dimension groups: ", dim_grpA_2D
  print "3D dimension groups: ", dim_grpA_3D

  # Set up figure for 2D image plots
  gs = gridspec.GridSpec( len(dim_grpA_2D), 1 )
  fig = plt.figure()
  fig.suptitle("2D variables for %s" % args.file)

  print "Finding all variables that are in terms of each 2D dimension group..."
  for i, dim_grp in enumerate(dim_grpA_2D):
    print "Axes {0:}  {1:}".format(i, dim_grp)
    vars = [var for var in dsA.variables if dsA.variables[var].dimensions == dim_grp]

    ax = plt.subplot(gs[i])

    flatdata = list(itertools.chain.from_iterable( dsA.variables[vars[0]] ))
    for j, v in enumerate(vars):
      print "  {0:} {1:}".format(v, dsA.variables[v].shape)
      if not j == 0:
        flatdata = np.vstack( (flatdata, list(itertools.chain.from_iterable( dsA.variables[vars[j]]))) )
      else:
        pass # already added the first var's data ouside loop

    #ax.set_title("??")

    ax.set_xlabel("%s, %s" % (dim_grp[0], dim_grp[1]))
    ax.set_xticks(())
    ax.set_xticklabels(())

    ax.set_ylabel("%i" % i)
    ax.set_yticks( range(0, len(vars)) )
    ax.set_yticklabels(())

    print "shape of image being plotted:", flatdata.shape
    plt.imshow(flatdata, interpolation='none', aspect=1.0) # 4 -> height is 4x the width

  plt.show()



  gs = gridspec.GridSpec( 1, len(dim_grpA_3D) )
  fig = plt.figure()
  fig.suptitle("3D variables for %s" % args.file)
  print "Finding all variables that are in terms of each 3D dimension group..."

  #from IPython import embed; embed()
  for i, dim_grp in enumerate(dim_grpA_3D):
    print "Axes {0:}  {1:}".format(i, dim_grp)
    vars = [var for var in dsA.variables if dsA.variables[var].dimensions == dim_grp]

    ax = plt.subplot(gs[i])
    s = dsA.variables[vars[0]].shape
    flatdata = np.vstack( (dsA.variables[vars[0]][:].reshape((s[0]*s[1], s[2]))) )
    for j, v in enumerate(vars):
      print "  {0:} {1:}".format(v, dsA.variables[v].shape)

      s = dsA.variables[v].shape
      flatdata = np.vstack( (flatdata, dsA.variables[v][:].reshape((s[0]*s[1], s[2]))) )

    #ax.set_xlabel("%s, %s" % (dim_grp[0], dim_grp[1]))
    ax.set_xticks(())
    ax.set_xticklabels(())

    #ax.set_ylabel("%i" % i)
    #ax.set_yticks( range(0, len(vars)) )
    ax.set_yticklabels(())

    print "shape of image being plotted:", flatdata.shape
    plt.imshow(dsA.variables[v][:].reshape((s[0]*s[1], s[2])), aspect=1.0, interpolation='none')

  plt.show()

if __name__ == '__main__':
  
  parser = argparse.ArgumentParser(

    formatter_class=argparse.RawDescriptionHelpFormatter,
      
      description=textwrap.dedent('''\
        Show some restart files as images.
        '''),
        
      epilog=textwrap.dedent('''''')
  )
  
  parser.add_argument('file', default='',
      help="A file to show")

  parser.add_argument('--compare', default=None,
      help='path to a NetCDF file to compare to (B). NOT IMPLEMENTED YET!')

  print "Parsing command line arguments..."
  args = parser.parse_args()

  main(args.file, args.compare)







