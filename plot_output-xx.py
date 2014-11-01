#!/usr/bin/env python

import sys # for exit()
import argparse
import textwrap

import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.ticker import MaxNLocator

def main():

  parser = argparse.ArgumentParser(description=textwrap.dedent('''\
      Make various plots from dvmdostem's "output-**.nc" files. "output-**.nc" 
      files can hold data from multiple cohorts, for multiple years. They
      should have the following dimensions: 
      CHTID (UNLIMITED), YEAR, YYYYMM, PFTS
      '''))

  #group = parser.add_mutually_exclusive_group()
  #group.add_argument('-n', '--normal', action="store_true")
  #group.add_argument('-e', '--explorer', action="store_true")

  parser.add_argument('-ls', '--list', action='store_true', 
      help="List the cohorts and PFTs in this file and then exit.")
  
  parser.add_argument('-d', '--display', action='store_true', 
      help="Display the plot")
  parser.add_argument('-s', '--save', action='store_true', default=False, 
      help="Save the plot with generic name. Warning: will overwrite existing file with same name!!")
  
  parser.add_argument('-cix', '--cohortindex', default=0, required=False, type=int, metavar='N',
      help='The *index* of the cohort to plot. NOTE: this may or may not be the same as the COHORTID!')
  parser.add_argument('-p', '--pft', default=0, required=False, type=int, metavar='N',
      help='Which PFT to plot')

  parser.add_argument('inputfile', help="path to a output-xx.nc file (A) to read from.")
  parser.add_argument('--compare', default=None, help="path to an output-xx.nc file (B) to compare.")

  args = parser.parse_args()
  
  if args.list:
    print_file_summary(args)
    sys.exit(0)


  validate_outputnc_file(args.inputfile)

  print "Loading dataset(s)..."
  dsA = nc.Dataset(args.inputfile)
  if (args.compare != None):
    dsB = nc.Dataset(args.compare)

  pftidx = args.pft
  chtidx = args.cohortindex
  
  print '(A): ', args.inputfile
  print '(B): ', args.compare 
   
  #  
  # General plot settings...
  #
  plt.rcParams['figure.figsize'] = 7.5, 10 # w, h
  # get a figure instance and an axes instance for each subplot
  if args.compare:
    plt.rcParams['figure.figsize'] = 14, 10 # w, h
    # get a figure instance and an axes instance for each subplot
    fig, (CaxL, LAIaxL, NaxL, SOILCaxL, SOILaxL, VWCaxL, ) = plt.subplots(nrows=6, ncols=2)
    (Cax, CaxB) = CaxL[:]
    (LAIax, LAIaxB) = LAIaxL[:]
    (Nax, NaxB) = NaxL[:]
    (SOILCax, SOILCaxB) = SOILCaxL[:]
    (SOILax, SOILaxB) = SOILaxL[:]
    (VWCax, VWCaxB) = VWCaxL[:]

  else:
    fig, (Cax, LAIax, Nax, SOILCax, SOILax, VWCax, ) = plt.subplots(nrows=6, ncols=1)


  fig.subplots_adjust(hspace=.5)

  # build the title...
  title = '''General Diagnostics for dvm-dos-tem
  (A) %s
  ''' % (args.inputfile)
  if args.compare:
    title = title + ''' (B) %s
    ''' % (args.compare)
  title = title + '''(Cohort Index: %s) (PFT: %s)''' % (args.cohortindex, args.pft)  
  fig.suptitle(title, linespacing=1.95)

  # Now work on each subplot. In general, the idea is:
  #  1) select data from the files(s)
  #  2) subset the data as necessary
  #  3) actually plot the data on the matplotlib axes
  #  4) finish up any settings (legends, etc)
  # Here we go...

  # Carbon subplot...
  vegc = dsA.variables['VEGC']
  npp = dsA.variables['NPP']

  vegc_cht_pft = vegc[chtidx, :, pftidx]
  npp_cht_pft = npp[chtidx, :, pftidx]

  Cax.plot(np.arange(0,len(vegc_cht_pft)), vegc_cht_pft, color='k', label='vegc')
  Cax.legend(fontsize='small', loc='upper left', fancybox=True)

  Cax1 = Cax.twinx()
  Cax1.plot(np.arange(0,len(npp_cht_pft)), npp_cht_pft, color='r', label='npp')
  Cax1.legend(fontsize='small', loc='upper right', fancybox=True)

  if args.compare:
    vegcB = dsB.variables['VEGC']
    nppB = dsB.variables['NPP']

    vegc_cht_pftB = vegcB[chtidx, :, pftidx]
    npp_cht_pftB = nppB[chtidx, :, pftidx]

    CaxB.plot(np.arange(0,len(vegc_cht_pftB)), vegc_cht_pftB, color='k', label='vegc')
    CaxB.legend(fontsize='small', loc='upper left', fancybox=True)

    CaxB1 = CaxB.twinx()
    CaxB1.plot(np.arange(0,len(npp_cht_pftB)), npp_cht_pftB, color='r', label='npp')

    CaxB1.legend(fontsize='small', loc='upper right', fancybox=True)
    

  # Lai subplot...
  lai = dsA.variables['LAI']
  lai_cht_pft = lai[chtidx, :, pftidx]
  LAIax.plot(np.arange(0, len(lai_cht_pft)), lai_cht_pft, label='lai')
  LAIax.legend(fontsize='small', loc='best', fancybox=True)
  if args.compare:
    laiB = dsB.variables['LAI']
    lai_cht_pftB = laiB[chtidx, :, pftidx]
    LAIaxB.plot(np.arange(0, len(lai_cht_pftB)), lai_cht_pftB, label='lai')
    LAIaxB.legend(fontsize='small', loc='best', fancybox=True)

  # Nitrogen subplot...
  avln = dsA.variables['AVLN']
  avln_cht = avln[chtidx, :]
  #nuptake_cht = ??? #<- not sure what variable this is...not in variable list?
  Nax.plot(np.arange(0, len(avln_cht)), avln_cht, label='avln')
  Nax.legend(fontsize='small', loc='best', fancybox=True)
  if args.compare:
    avlnB = dsB.variables['AVLN']
    avln_chtB = avlnB[chtidx, :]
    #nuptake_cht = ??? #<- not sure what variable this is...not in variable list?
    NaxB.plot(np.arange(0, len(avln_chtB)), avln_chtB, label='avln')
    NaxB.legend(fontsize='small', loc='best', fancybox=True)

  
  # Soil C subplot (I have no idea if these are the right variabels...??)
  oshlwc = dsA.variables['OSHLWC']
  oshlwc_cht = oshlwc[chtidx, :]

  odeepc = dsA.variables['ODEEPC']
  odeepc_cht = odeepc[chtidx, :]

  mineac = dsA.variables['MINEAC']
  mineac_cht = oshlwc[chtidx, :]

  SOILCax.plot(np.arange(0, len(oshlwc_cht)), oshlwc_cht, label='oshlwc')
  SOILCax.plot(np.arange(0, len(odeepc_cht)), odeepc_cht, label='odeepc')
  SOILCax.plot(np.arange(0, len(mineac_cht)), mineac_cht, label='mineac')
  SOILCax.legend(fontsize='small', loc='best', fancybox=True)
  if args.compare:
    oshlwcB = dsB.variables['OSHLWC']
    oshlwc_chtB = oshlwcB[chtidx, :]

    odeepcB = dsB.variables['ODEEPC']
    odeepc_chtB = odeepcB[chtidx, :]

    mineacB = dsB.variables['MINEAC']
    mineac_chtB = oshlwcB[chtidx, :]

    SOILCaxB.plot(np.arange(0, len(oshlwc_chtB)), oshlwc_chtB, label='oshlwc')
    SOILCaxB.plot(np.arange(0, len(odeepc_chtB)), odeepc_chtB, label='odeepc')
    SOILCaxB.plot(np.arange(0, len(mineac_chtB)), mineac_chtB, label='mineac')
    SOILCaxB.legend(fontsize='small', loc='best', fancybox=True)

  

  # annual ALD, EET, mean VWC and TS in the mineral layer
  ald = dsA.variables['ALD']
  ald_cht = ald[chtidx, :]

  eet = dsA.variables['EET']
  eet_cht = ald[chtidx, :]

  tshlw = dsA.variables['TSHLW']
  tshlw_cht = tshlw[chtidx, :]

  SOILax.plot(np.arange(0, len(ald_cht)), ald_cht, label='ald')
  SOILax.plot(np.arange(0, len(eet_cht)), eet_cht, label='eet')
  SOILax.plot(np.arange(0, len(tshlw_cht)), tshlw_cht, label='tshlw')
  SOILax.legend(fontsize='small', loc='best')

  if args.compare:
    aldB = dsB.variables['ALD']
    ald_chtB = aldB[chtidx, :]

    eetB = dsB.variables['EET']
    eet_chtB = aldB[chtidx, :]

    tshlwB = dsB.variables['TSHLW']
    tshlw_chtB = tshlwB[chtidx, :]

    SOILaxB.plot(np.arange(0, len(ald_chtB)), ald_chtB, label='ald')
    SOILaxB.plot(np.arange(0, len(eet_chtB)), eet_chtB, label='eet')
    SOILaxB.plot(np.arange(0, len(tshlw_chtB)), tshlw_chtB, label='tshlw')
    SOILaxB.legend(fontsize='small', loc='best')



  # VWC subplot...
  vwcshlw = dsA.variables['VWCSHLW']
  vwcshlw_cht = vwcshlw[chtidx, :]

  vwcdeep = dsA.variables['VWCDEEP']
  vwcdeep_cht = vwcdeep[chtidx, :]

  vwcminea = dsA.variables['VWCMINEA']
  vwcminea_cht = vwcminea[chtidx, :]

  vwcmineb = dsA.variables['VWCMINEB']
  vwcmineb_cht = vwcmineb[chtidx, :]

  vwcminec = dsA.variables['VWCMINEC']
  vwcminec_cht = vwcminec[chtidx, :]

  VWCax.plot(np.arange(0, len(vwcshlw_cht)), vwcshlw_cht, label='vwcshlw')
  VWCax.plot(np.arange(0, len(vwcdeep_cht)), vwcdeep_cht, label='vwcdeep')
  VWCax.plot(np.arange(0, len(vwcminea_cht)), vwcminea_cht, label='vwcmina')
  VWCax.plot(np.arange(0, len(vwcmineb_cht)), vwcmineb_cht, label='vwcminb')
  VWCax.plot(np.arange(0, len(vwcminec_cht)), vwcminec_cht, label='vwcminc')
  VWCax.legend(fontsize='small', loc='best')
  if args.compare:
    vwcshlwB = dsB.variables['VWCSHLW']
    vwcshlw_chtB = vwcshlwB[chtidx, :]

    vwcdeepB = dsB.variables['VWCDEEP']
    vwcdeep_chtB = vwcdeepB[chtidx, :]

    vwcmineaB = dsB.variables['VWCMINEA']
    vwcminea_chtB = vwcmineaB[chtidx, :]

    vwcminebB = dsB.variables['VWCMINEB']
    vwcmineb_chtB = vwcminebB[chtidx, :]

    vwcminecB = dsB.variables['VWCMINEC']
    vwcminec_chtB = vwcminecB[chtidx, :]

    VWCaxB.plot(np.arange(0, len(vwcshlw_chtB)), vwcshlw_chtB, label='vwcshlw')
    VWCaxB.plot(np.arange(0, len(vwcdeep_chtB)), vwcdeep_chtB, label='vwcdeep')
    VWCaxB.plot(np.arange(0, len(vwcminea_chtB)), vwcminea_chtB, label='vwcmina')
    VWCaxB.plot(np.arange(0, len(vwcmineb_chtB)), vwcmineb_chtB, label='vwcminb')
    VWCaxB.plot(np.arange(0, len(vwcminec_chtB)), vwcminec_chtB, label='vwcminc')
    VWCaxB.legend(fontsize='small', loc='best')


  # Set the maximum number of tick marks for ALL axes
  for ax in fig.axes:
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5, prune='upper'))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=8, prune='upper'))


  if args.save:
    saved_file_name = "plot_general_diagnostics.png"
    print "Savging plot as '%s'..." % saved_file_name
    plt.savefig(saved_file_name, dpi=72)
  
  if args.display:
    print "Showing plot..."
    plt.show()

  
  
#
# Utility functions...
#
def validate_outputnc_file(file):
  ds = nc.Dataset(file)

  try:
    # check correct dimensions
    assert set(ds.dimensions.keys()) == set(['PFTS', 'CHTID', 'YEAR', 'YYYYMM'])

  except AssertionError as e:
    print "Problem with NetCDF file shape!", e


def print_file_summary(args):
  print "Loading dataset(s)..."
  dsA = nc.Dataset(args.inputfile)
  if (args.compare != None):
    dsB = nc.Dataset(args.compare)

  print "Summary"
  print "-----------------------------------"

  print "(A): %s" % args.inputfile
  print "  Available CHTIDs: ", 
  for chtid in dsA.variables['CHTID']:
    print chtid,
  print ""
  print "  # of PFTs (zero indexed): ", len(dsA.dimensions['PFTS'])
  print "  length of YYYYMM: ", len(dsA.dimensions['YYYYMM'])
  print ""

  if args.compare:
    print "(B): %s" % args.compare
    print "  Available CHTIDs: ", 
    for chtid in dsB.variables['CHTID']:
      print chtid,
    print ""
    print "  # of PFTs (zero indexed): ", len(dsB.dimensions['PFTS'])
    print "  length of YYYYMM: ", len(dsB.dimensions['YYYYMM'])
    print ""

  print "-----------------------------------"


if __name__ == '__main__':
  main()


# p = plt.Rectangle((0,0),0,0)
# p.set_label('Testing...')
# Nax.add_patch(p)
