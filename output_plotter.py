#!/usr/bin/env python

#import sys # for exit()
#import argparse

import abc

import textwrap
import shlex

import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt


class PlotBuilder(object):
  '''
  An abstract builder class. Concrete builders should derive from this.
  '''
  __metadata__ = abc.ABCMeta

  dataset = None
  
  def __del__(self):
    pass
    #print self.__class__.__name__, " dtor; closing dataset..."
    #self.dataset.close()

  def getDataset(self, filename):
    self.dataset = nc.Dataset(filename, 'r')
    print "A %s object opened a file: " % self.__class__.__name__, filename

  @abc.abstractmethod
  def teardown(self):
    raise

def guess_stage(filename):
  guess = filename[-5:-2]
  assert not guess in ('eq','sp','tr','sc'), "Unable to determine runstage from file name! %s" % filename
  return guess


class TimeSeriesBuilder(PlotBuilder):
  '''
  Makes a simple timeseries plot...
  '''
  def __init__(self):
    print "Constructing a %s" % self.__class__.__name__

  def some_random_build_step(self):
    print "Doing some random build step within a ", self.__class__.__name__

  def initialize( self, configstring ):
    self.traces = parse_configstringA( configstring )
    print "Checking the trace list..."
    keys = ['varname', 'units', 'axnum', 'axside']
    for entry in self.traces:
      for key in keys:
        if not key in entry.keys():
          print "Invalid config string for this builder!"

  def setup_grid(self):
    pass

  def setup_data(self):
    fname = 'latest-output-xx.nc'
    dataset = nc.Dataset(fname, 'r')
    print "A %s object opened the file " % self.__class__.__name__, fname


    rows = len(set([i['axnum'] for i in self.traces]))
    self.fig, self.axes = plt.subplots(nrows=rows, ncols=1)

    chtidx = 0
    pftidx = 0

    for trace in self.traces:
      #from IPython import embed; embed()
      ax = self.axes[trace['axnum']]
      dimensions = dataset.variables[trace['varname']].dimensions
      #print dimensions

      if dimensions == ('CHTID', 'YYYYMM', 'PFTS'):
        data = dataset.variables[trace['varname']][chtidx, :, trace['pft']]
      elif dimensions == ('CHTID', 'YYYYMM'):
        data = dataset.variables[trace['varname']][chtidx, :]
      
      ax.plot(np.arange(0, len(data)), data, label=trace['varname'])




  def setup_axes_looks(self):
    pass

  def setup_legends(self):
    pass

  def setup_titles(self):
    pass

  def setup_overall_size(self):
    pass

  def finalize(self):
    '''Returns a matplotlib figure instance and list of axes instances.'''
    return self.fig, self.axes

  def build(self, config):
    '''Returns a matplotlib Figure and a list of Axes'''
    fname = 'latest-output-xx.nc'
    self.getDataset(fname)
    config_list = parse_configstringA(config)
    self.some_random_build_step()
    
    print "Checking config list..."
    keys = ['varname', 'units', 'axnum', 'axside']
    for entry in config_list:
      for key in keys:
        if not key in entry.keys():
          print "Invalid config for this builder!"
  
    rows = len(set([i['axnum'] for i in config_list]))
    fig, axes = plt.subplots(nrows=rows, ncols=1)

    chtidx = 0
    pftidx = 0

    for item in config_list:
      #from IPython import embed; embed()
      ax = axes[item['axnum']]
      dimensions = self.dataset.variables[item['varname']].dimensions
      print dimensions
      if dimensions == ('CHTID', 'YYYYMM', 'PFTS'):
        data = self.dataset.variables[item['varname']][chtidx, :, item['pft']]
      elif dimensions == ('CHTID', 'YYYYMM'):
        data = self.dataset.variables[item['varname']][chtidx, :]

      ax.plot(np.arange(0, len(data)), data, label=item['varname'])

    return fig, axes
    

  def teardown(self):
    print "Doing some teardown...in derived class override method"


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
      print "found %s tokens: "%len(tokens), tokens

      if len(tokens) not in [4,5,6]:
        print "Error parsing config string! Invalid number of tokens: %s" % len(tokens)
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


  print dl
  return dl



def main():
  print "Hello, starting to make some plots..."
  
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
  plotter.display()


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
