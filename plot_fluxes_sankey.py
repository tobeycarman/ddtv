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
  from matplotlib.sankey import Sankey

except ImportError as e:
  print "%s" % e
  sys.exit()



def main(args):
  print "Loading dataset..."
  dsA = nc.Dataset(args.inputfile)
  
  print '(A): ', args.inputfile
  year = args.year
  month = args.month
  cht = args.cohort
  
  numpfts = len(dsA.dimensions['PFTS'])
  
  # needs to have one value per pft
  litterfall = dsA.variables['LTRFALC'][cht,year*month,:]
  
  # needs to be a single value (for whole soil pool)
  rh = dsA.variables['RH'][0,year*month]
  
  # one value per pft
  gpp = dsA.variables['GPP'][cht, year*month,:]
  
  # one value per pft
  npp = dsA.variables['NPP'][cht, year*month, :]
  ra = (npp-gpp)  

  pfts = []
  for i in range(numpfts):
    pfts.append({'gpp': gpp[i],
                 'ltfl': litterfall[i],
                 'Ra': ra[i],
                })
                
  for pft in pfts:
    print pft
  
  fig = plt.figure(figsize=(18,6))
  ax = fig.add_subplot(1, 1, 1, xticks=[], yticks=[], title="Veg and Soil Fluxes")

  sankey = Sankey(ax=ax, 
                  tolerance=1e-23,
                  #scale=1.00,
                  offset=-1.75,
                  head_angle=130,
                  gap=3.0,
                  radius=0.5,
                  unit='gC/m2',
                  format='%.0f',
                  )
  
  soil_flows = np.append(litterfall, rh)
                      # [gpp1, gpp2, ... rh, ]


  print "litterfall: ", litterfall
  print "rh: ", rh
  print "gpp: ", gpp
  print "ra: ", ra
  print "soil_flows: ", soil_flows

  # make each pft a bit longer
  pathlens = [1+(numpfts-i) for i,x in enumerate(gpp)]
  pathlens.append(0.5) # make the departing rh flow shorter
  
  # make all the pft flows come in from top
  orients = [1 for i in range(len(pathlens))]
  orients[-1] = 0 # change the lasts one (rh) to a side flow
  
  labels = ['pft%s'%i for i, v in enumerate(soil_flows)]
  labels[-1] = 'RH'
  
  sankey.add(patchlabel="Soil",
             flows=soil_flows, 
             fc='brown', label='soil',
             labels=labels,
             orientations=orients,
             #pathlengths=1.0,
             pathlengths=pathlens,
             rotation=0,
             trunklength=7.0,
             )

  print "[PFT ]: gpp    ltrfl    ra"
  for pft, val in enumerate(gpp):
    print "[PFT%s]: %.05f %.05f %.05f"%(pft, gpp[pft], -1.0*litterfall[pft], ra[pft])
  print "-------"
  
#   pft = 1
#   print gpp[pft]
#   print -1.0*litterfall[pft]
#   print ra[pft]
#   
#   sankey.add(flows=[gpp[pft], -1.0*litterfall[pft], ra[pft]], 
#              fc=(0.0, 0.8, 0.0), # rgb 
#              label='pft%s' % (pft),
#              labels=['gpp%s'%pft, 'lf%s'%pft, 'ra%s'%pft,],
#              orientations=[-1,1,0], # 1(top), 0(l/r), -1(bottom)
#                                     # seems to be in relation to prev. diagram...
#              pathlengths=[1,pft*10,1],
#              trunklength=12.0,
#              prior=0, connect=(pft,1)
#              )

  # VEGETATION FLOWS
  for pft, val in enumerate(gpp):
    if (-1.0*litterfall[pft] < 0) or (-1.0*litterfall[pft] > 0):
    
      sankey.add(flows=[gpp[pft], -1.0*litterfall[pft], ra[pft]], 
                 fc=(0.0, 0.8, 0.0), # rgb 
                 label='pft%s' % (pft),
                 labels=['gpp%s'%pft, 'lf%s'%pft, 'ra%s'%pft,],
                 orientations=[-1,1,-1], # 1(top), 0(l/r), -1(bottom)
                                        # seems to be in relation to prev. diagram...
                 #pathlengths=[1,pft+10,1],
                 trunklength=12.0,
                 prior=0, connect=(pft,1)
                 )
    else:
     pass
#       sankey.add(flows=[gpp[pft], -1.0*litterfall[pft], ra[pft]], 
#                  fc=(0.0, 0.8, 0.0), # rgb 
#                  label='pft%s' % (pft),
#                  labels=['gpp%s'%pft, 'lf%s'%pft, 'ra%s'%pft,],
#                  orientations=[-1,1,-1], # 1(top), 0(l/r), -1(bottom)
#                                         # seems to be in relation to prev. diagram...
#                  pathlengths=[1,6,1],
#                  #trunklength=2.0,
#                  #prior=0, connect=(pft,1)
#                  )

  diagrams = sankey.finish()
  #print diagrams
  #diagrams[-1].patch.set_hatch('/')  
  plt.legend(loc='best')
  plt.title("The default settings produce a diagram like this.")




  wrapup(args)
  


def wrapup(args):
  if (args.display):
    print "Displaying..."
    plt.show()

  if (args.save):
    outputfile = args.save
    print "Saving %s..." % outputfile
    plt.savefig(outputfile, dpi=300)

  
    
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='''Plots a Sankey diagram of
the fluxes from an output-*.nc file from dvm-dos-tem.

This plot captured only one timestep. There might be a way to animate it to
cover the time range?

Another option might be some sort of yearly averaging...
''')

  #group = parser.add_mutually_exclusive_group()
  #group.add_argument('-n', '--normal', action="store_true")
  #group.add_argument('-e', '--explorer', action="store_true")

  parser.add_argument('-d', '--display', action='store_true', help="Display the plot")
  parser.add_argument('-s', '--save', default=False, help="Save the plot to simple-plot.png")

  parser.add_argument('-c', '--cohort', required=True, type=int, help='Which cohort to plot')
  parser.add_argument('-y', '--year', required=True, type=int, help='Which year to plot.')
  parser.add_argument('-m', '--month', required=True, type=int, help='Which month to plot.')
      
  parser.add_argument('inputfile', help='path to a NetCDF file to read from (A).')

  args = parser.parse_args()
  #print args

  main(args)

