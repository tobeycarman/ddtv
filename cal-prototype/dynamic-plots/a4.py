#!/usr/bin/env python

import sys
import collections
import numpy as np
import matplotlib.pyplot as plt


MAXSZ = 10000

def main():
#     if sys.stdin.isatty():
#         print "Please use a pipe as stdin\nExample: ping stackoverflow.com | python script.py"
#         return 0
#     regex = re.compile('time=(\d+.\d+)')

    #dataq = Queue.Queue(maxsize=1000)
    data = collections.deque([],MAXSZ)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #l1, = ax.plot(data)
    fig.show()

    pltlines = []

    while True:
        if len(pltlines) > 0:
          pltlines.pop(0).remove()

        line = sys.stdin.readline()
        if line == '':
            break
        
        
        if len(data) >= MAXSZ:
          data.popleft()
        
        data.append(line.split()[0])
          
        #add number to array, plot the data
        #data.append( line.split()[0] )
        
        pltlines = ax.plot(data, 'r')
        plt.draw()
    return 0

if __name__ == '__main__':
        sys.exit(main())