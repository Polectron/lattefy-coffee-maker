#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from serial import Serial
 
ser = Serial('/dev/ttyACM0', 9600)
 
x=ser.readline()
ser.write("1")
print(x)
def cleanup( str ):
  result = ""
 
  for c in str:
    if( (c >= "0") and (c <= "9") ):
       result += c
 
  return result
 
print( cleanup(x))
#ser.write("1") 
