#!/usr/bin/env python

import json
import random
import time
import sys
import zmq
from random import randrange

def main():

  context = zmq.Context()
  socket = context.socket(zmq.PUSH)
  socket.set_hwm(5)
  socket.bind("tcp://*:5556")

  with open('format1.json') as infile:
    d = json.load(infile)
  

  for yr in range(0,100):
    for m in range(0,12):
      
      d['pft0']['vegcL'] = random.random()
      d['pft0']['vegcW'] = random.random()
      d['pft0']['vegcR'] = random.random()
      d['pft0']['cmax'] = random.random()
      d['pft1']['vegcL'] = random.random()
      d['pft1']['vegcW'] = random.random()
      d['pft1']['vegcR'] = random.random()
      d['pft1']['cmax'] = random.random()
      d['gpp'] = random.random()
      d['npp'] = random.random()
      d['month'] = m
      d['year'] = yr
      
      #print d
      print "[DVMDOSTEM] writing d to pass thru file. Year: %s Month: %s" % (yr, m)
      with open('pass_thru.json', 'w') as outfile:
        json.dump(d, outfile)

      print "[DVMDOSTEM] sending data to socket..."
      socket.send_string(json.dumps(d))

      print "[DVMDOSTEM] sleeping..."
      #time.sleep(0.1)
      

if __name__ == '__main__':
  main()
