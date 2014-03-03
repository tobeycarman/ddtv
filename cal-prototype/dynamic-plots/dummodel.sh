#!/bin/bash

i=0
#while [ $i -lt 10000 ]
while :
do
  # send a random number, followed by a sequence number...
  echo $(( ( RANDOM % 100 )  + 1 )) $i
  sleep 0
  i=$[$i+1]
done
