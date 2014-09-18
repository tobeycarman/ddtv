#!/usr/bin/env python

#import sys # for exit()
#import argparse

import abc

import textwrap
import shlex

import logging

import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt



class PlotBuilder(object):
  '''
  An abstract builder class. Concrete builders should derive from this.
  '''
  __metaclass__ = abc.ABCMeta

  dataset = None
  
  def __del__(self):
    pass

  @abc.abstractmethod
  def initialize(self):
    pass

  @abc.abstractmethod
  def finalize(self):
    pass

def guess_stage(filename):
  guess = filename[-5:-2]
  assert not guess in ('eq','sp','tr','sc'), "Unable to determine runstage from file name! %s" % filename
  return guess


class TimeSeriesBuilder(PlotBuilder):
  '''
  Makes a simple timeseries plot...
  '''
  def __init__(self):
    logging.info("Constructing a %s" % self.__class__.__name__)

  def initialize( self, configstring ):
    self.traces = parse_configstringA( configstring )
    logging.info("Checking the trace list...")
    keys = ['varname', 'units', 'axnum', 'axside']
    for trace in self.traces:
      for key in keys:
        if not key in trace.keys():
          logging.warn("Invalid config string for this builder!")
  
    logging.debug("Printing the config string to stdout.")
    print configstring


  def setup_grid(self):
    pass

  def setup_data(self):
    fname = 'latest-output-xx.nc'
    dataset = nc.Dataset(fname, 'r')
    logging.debug("A %s object opened the file %s" % (self.__class__.__name__, fname))

    rows = len(set([i['axnum'] for i in self.traces]))
    self.fig, self.axes = plt.subplots(nrows=rows, ncols=1)

    self.fig.suptitle(fname)

    chtidx = 0
    pftidx = 0


    logging.debug(self.traces)

    for trace in self.traces:
      ax = self.axes[trace['axnum']]
      dimensions = dataset.variables[trace['varname']].dimensions

      if dimensions == ('CHTID', 'YYYYMM', 'PFTS'):
        data = dataset.variables[trace['varname']][chtidx, :, trace['pft']]
        l = '%s cht %s pft %s'%(trace['varname'], chtidx, trace['pft'] )
      elif dimensions == ('CHTID', 'YYYYMM'):
        data = dataset.variables[trace['varname']][chtidx, :]
        l = '%s cht %s'%(trace['varname'], chtidx)
      
      ax.plot(np.arange(0, len(data)), data, label=l)

  def setup_axes_looks(self):
    pass
  

  def setup_legends(self):
    for ax in self.axes:
      ax.legend()
  
  def setup_titles(self):
    pass

  def setup_overall_size(self):
    pass

  def finalize(self):
    '''Returns a matplotlib figure instance and list of axes instances.'''
    return self.fig, self.axes

class Plotter(object):
  '''
  The director class, this class maintains a concrete builder.'''
  def __init__(self, builder_instance=None):
    self.builder = builder_instance

  def create(self, config):
    '''
    Creates and reuturns a plot using self.builder
    Precondition: not self.builder is None
    '''
    assert not self.builder is None, "No defined builder!"
   
   
    # could return the result of building...
    # not quite sure what I am going to end up with yet
    # maybe the whole plt.fig??

    self.builder.initialize(config)
    self.builder.setup_data()
    self.builder.setup_axes_looks()
    self.builder.setup_legends()
    self.builder.setup_titles()
    self.builder.setup_overall_size()
    self.builder.setup_grid()

    self.fig, self.axes = self.builder.finalize()
    # do more stuff with fig and axes??
  

  def interactive_display(self):
    plt.ion()
    logging.debug("Run plt.show() to show the plot!")
    from IPython import embed; embed()
  
  
  def display(self):
    plt.show()

  def save(self):
    #from IPython import embed; embed()
    plt.savefig("junk")






def probe_query_report_dataset(dataset):
  d = {}
  d['stage'] = guess_stage(d)
  return


def parse_configstringA(configstr):
  dl = [] # list for config dicts
  for line in configstr.splitlines():
    d = {} # empty config dict
    if (line.startswith('#') or len(line) < 1 ):
      pass # comments, empty, lines
    else:
      tokens = shlex.split(line) # lets us use quoted strings.
      logging.debug("found %s tokens: " % len(tokens))
      logging.debug("Tokens: %s " % tokens)

      if len(tokens) not in [4,5,6]:
        logging.debug("Error parsing config string! Invalid number of tokens: %s" % len(tokens))
      else:

        # assign some data values based on columns
        if len(tokens) >= 4:
          d['varname'] = tokens[0]
          d['units'] = tokens[1]
          d['axnum'] = int(tokens[2])
          d['axside'] = tokens[3]
        if len(tokens) >= 5:
          d['pft'] = int(tokens[4])
#        if len(tokens) == 6:
#          d['pftpart'] = tokens[5]
        dl.append(d)


  logging.debug(dl)
  return dl



def main():


  print "Setting up logging..."
  LOG_FORMAT = '%(levelname)-7s %(name)-8s %(message)s'
  numeric_level = getattr(logging, 'DEBUG')
  #numeric_level = getattr(logging, loglevel.upper(), None)
  if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)

  logging.basicConfig(level=numeric_level, format=LOG_FORMAT)

  logging.debug("Hello, starting to make some plots...")
  
  configstr = textwrap.dedent('''\
  # var     units     axnum  axside  pft pftpart
  # --------------------------------------------
  VEGC    gC/m^2      0         L     0    leaf
  NPP     gC/m^2      0         R     0
  
  ALD     m           1         L
  EET     gH20/m^2    1         L
  TSHLW   "deg C"     1         R
  ''')
  
  plotter = Plotter( TimeSeriesBuilder() )
  plotter.create(configstr)
  plotter.save()
  plotter.interactive_display()


#  from IPython import embed
#  embed()
#  plot.save()
#  plot.display()





if __name__ == '__main__':
  #  parser = argparse.ArgumentParser(description=textwrap.dedent('''\
  #    Make various plots from dvmdostem's "output-**.nc" files. "output-**.nc"
  #    files can hold data from multiple cohorts, for multiple years. They
  #    should have the following dimensions:
  #    CHTID (UNLIMITED), YEAR, YYYYMM, PFTS
  #    '''))
  #
  #  #group = parser.add_mutually_exclusive_group()
  #  #group.add_argument('-n', '--normal', action="store_true")
  #  #group.add_argument('-e', '--explorer', action="store_true")
  #
  #  parser.add_argument('-ls', '--list', action='store_true',
  #                      help="List the cohorts and PFTs in this file and then exit.")
  #
  #  parser.add_argument('-d', '--display', action='store_true',
  #                      help="Display the plot")
  #  parser.add_argument('-s', '--save', action='store_true',
  #                      default=False,
  #                      help="Save the plot with generic name. Warning: will overwrite existing file with same name!!")
  #
  #  parser.add_argument('-cix', '--cohortindex', default=0, required=False, type=int, metavar='N',
  #                      help="The *index* of the cohort to plot. NOTE: this may or may not be the same as the COHORTID!")
  #  parser.add_argument('-p', '--pft', default=0, required=False, type=int, metavar='N',
  #                      help='Which PFT to plot')
  #
  #  parser.add_argument('inputfile', help="path to a output-xx.nc file (A) to read from.")
  #  parser.add_argument('--compare', default=None, help="path to an output-xx.nc file (B) to compare.")
  #
  #  args = parser.parse_args()
  #
  #  if args.list:
  #    print_file_summary(args)
  #    sys.exit(0)
  #

  main()
