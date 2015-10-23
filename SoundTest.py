#!/usr/bin/python

import alsaaudio as aa
import audioop
from time import sleep

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


# Set up audio
data_in = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NONBLOCK)
data_in.setchannels(1)
data_in.setrate(44100)
data_in.setformat(aa.PCM_FORMAT_S16_LE)

data_in.setperiodsize(256)

while True:
   # Read data from device
   l,data = data_in.read()
   if l:
      # catch frame error
      try:
         max_vol=audioop.max(data,2)
         scaled_vol = max_vol//4680      
         print(scaled_vol)
            
            
      except audioop.error, e:
         if e.message !="not a whole number of frames":
            raise e
