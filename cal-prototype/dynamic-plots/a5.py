#!/usr/bin/env python

import matplotlib
matplotlib.use('TkAgg')       # works, disfunctionally slow w/ blit=False
#matplotlib.use('GTKCairo')    # no gtk
#matplotlib.use('QT4Agg')      # not sure?
#matplotlib.use('GTKAgg')      # I dont have pygtk
#matplotlib.use('MacOSX')      # cant do blit, shows plots, not traces...

import sys
import collections
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

M = 100

x = np.arange(0,M)
y = np.ones(M)
#y[:] = np.NAN

fig, axes = plt.subplots(nrows=2)

for ax in axes:
  ax.set_ylim(0,100)

styles = ['r-', 'g-']#, 'y-', 'm-', 'k-', 'c-']
def plot(ax, style):
    return ax.plot(x, y, style, animated=True)[0]
lines = [plot(ax, style) for ax, style in zip(axes, styles)]

ydec = collections.deque(y,M)



def animate(i):
    #print "In animate..."
    new_data = sys.stdin.readline()
    if new_data == '':
      print "Got an empty line ...exiting.."
      exit(0)

    if len(ydec) >= M:
      ydec.popleft()
    ydec.append(float(new_data.split()[0]))

    for j, line in enumerate(lines, start=1):
      if j == 1:
        line.set_ydata(np.array(ydec))
        print "===================================="
        #print "Just plotted line %i with this data:"%j
        print "animate frame: ", i
        #print "x: ", x
        #print "np.array(ydec): ", np.array(ydec)
        print "float(new_data.split()[0]): ", float(new_data.split()[0])
        print "int(new_data.split()[1]): ", int(new_data.split()[1])
        #print "-------------------------------------"
        #print line.get_data()
        print "====================================="
        print 
    return lines
    
  

# We'd normally specify a reasonable "interval" here...
ani = animation.FuncAnimation(fig, animate, interval=200,#frames=100, interval=20, 
                             blit=True)
plt.show()