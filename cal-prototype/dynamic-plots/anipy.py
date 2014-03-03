#!/usr/bin/env python

# lifted from here:
# http://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

import sys

fig = plt.figure()
ax = plt.axes(xlim=(0,2), ylim=(-2,2))
line, = ax.plot([],[], lw=2)

def init():
  line.set_data([],[])
  return line
  
def animate(i):
  data = sys.stdin.readline()
  data = data.split()
  x = data[0]
  y = i
  line.set_data(x,y)
#   for idx, line in enumerate(sys.stdin):
#     data = line.split()
#     x = data[0]
#     y = idx
#     line = set_data(x,y)
#   x = np.linspace(0,2,1000)
#   y = np.sin(2 * np.pi * (x - 0.01 * i))
#   line.set_data(x,y)
  return line
  
anim = animation.FuncAnimation(fig, animate, init_func=init,
    frames=200, interval=20, blit=False) # looks like on osx blit has to be false
                                         # or might need a diff. backend.

# while True:
#   print sys.stdin.readline(),

# for line in sys.stdin:
#   print line                                         


#plt.show()

# # Called graph_script.py
# import matplotlib.pyplot as plt
# import numpy as np
# import sys
# 
# def setup_backend(backend="TkAgg"):
#    del sys.modules['matplotlib.backends']
#    del sys.modules['matplotlib.pyplot']
#    import matplotlib as mpl
#    mpl.use(backend)
#    import matplotlib.pyplot as plt
#    return plt
# 
# def update_line(hl, y):
#    hl.set_ydata(np.append(hl.get_ydata(),y))
#    hl.set_xdata(np.append(hl.get_xdata(),len(hl.get_ydata()) -1))
#    ax.set_ylim(0,np.amax(hl.get_ydata()) + 1)
#    ax.set_xlim(0,len(hl.get_xdata()))
#    fig.canvas.draw()
# 
# def animate():
#    # sys.stdin takes data from standard input and uses it in the Python program as the constantly updating variable line
#    hl, = ax.plot(np.zeros(1),np.zeros(1))
#    for line in sys.stdin:
#       # Write a conditional to get only the fields that are important for the plot            
#       sets = line.split()   #separate elements by space
#       if len(sets) > 0:
#          #if sets[0] == 'GPP':
#             y = eval(sets[0])
#             update_line(hl, y)
# 
# #plt = setup_backend()
# fig = plt.figure()
# ax = fig.add_subplot(111)
# win = fig.canvas.manager.window
# win.after(10, animate)
# plt.show()
#fig.show()
