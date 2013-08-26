#!/usr/bin/env python

# Tobey Carman
# Spatial Ecology Lab
# Aug 2013

try:
  import os
  import sys
  import argparse

  import netCDF4 as nc
  import numpy as np
  import matplotlib.pyplot as plt
  from mpl_toolkits.basemap import Basemap
except ImportError as e:
  print "%s" % e
  sys.exit()


def main():
  parser = argparse.ArgumentParser(description='''Displays a dot on a map for 
  each cohort's location.''')

  parser.add_argument('-d', '--display', action='store_true', help="Display the plot")
  parser.add_argument('-s', '--save', default=False, help="Save the plot to simple-plot.png")
  parser.add_argument('-c', '--cohortid', required=True, help="A cohortid.nc file with cohort list.")
  parser.add_argument('-g', '--gridid', required=True, help="A grid.nc file that maps cohort ids to lat/lons")

  args = parser.parse_args()
  #print args

  cohortid = nc.Dataset(args.cohortid)
  grid = nc.Dataset(args.gridid)
  
  chtlist = cohortid.variables['GRIDID'][:]
  lons = []
  lats = []
  for cohort in chtlist:
    lons.append(grid.variables['LON'][cohort])
    lats.append(grid.variables['LAT'][cohort])

  
  x,y = map(lons, lats)
  
  map = Basemap(resolution='c',projection='ortho',lat_0=60.,lon_0=-60.)
  map.scatter(x, y)
  map.drawcoastlines() # draw coastlines
  map.drawparallels(np.arange(-90.,120.,30.),labels=[1,0,0,0]) # draw parallels
  map.drawmeridians(np.arange(0.,420.,60.),labels=[0,0,0,1]) # draw meridians

  if (args.display):
    print "Displaying..."
    plt.show()

  if (args.save):
    outputfile = args.save
    print "Saving %s..." % outputfile
    plt.savefig(outputfile, dpi=300)

  
    
if __name__ == "__main__":
  main()

