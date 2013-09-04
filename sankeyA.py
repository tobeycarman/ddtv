#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.sankey import Sankey


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, xticks=[], yticks=[], title="Veg and Soil Fluxes")

sankey = Sankey(ax=ax, unit=None, tolerance=1e-6, )

# SOIL INPUT FLOWS
            # pft1  pft2  pft3  
litterfall = [0.15, 0.01, 0.10,]

# SOIL OUTPUT FLOWS
rh = [-0.65]

soil_flows = np.append(litterfall, rh)
                    # [gpp1, gpp2, ... rh, ]

sankey.add(flows=soil_flows, 
           fc='brown', label='soil',
           labels=['','','','Rh'],
           orientations=[1, 1, 1, 1],
           #pathlengths=1.0,
           pathlengths=[1.0, 2.0, 3.0, 0.5],
           rotation=0,
           trunklength=1.0
           )


# VEGETATION FLOWS

# INPUTS:
     # pft1, pft2, ...]
gpp = [0.12, 0.35, 0.07]

# OUTPUTS
ra =  [-0.10, -0.05, -0.09]

for pft, val in enumerate(gpp):
                  # gpp0     ltfl0             Ra0
  sankey.add(flows=[gpp[pft], -1*litterfall[pft], ra[pft]], 
             fc=(0.0, 0.8, 0.0), # rgb 
             label='pft%s' % (pft),
             labels=['gpp%s'%pft, 'lf%s'%pft, 'ra%s'%pft,],
             orientations=[-1,1,-1], # 1(top), 0(l/r), -1(bottom)
                                    # seems to be in relation to prev. diagram...
             #pathlengths=[],
             #trunklength=2.0,
             prior=0, connect=(pft,1))

diagrams = sankey.finish()

#diagrams[-1].patch.set_hatch('/')  
plt.legend(loc='best')
plt.title("The default settings produce a diagram like this.")

plt.show()