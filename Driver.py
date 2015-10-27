#!/usr/bin/python

import time
import random
import sys
import getopt
from rgbmatrix import Adafruit_RGBmatrix
from Display import Display
from Pattern import *
from threading import Thread
import threading
import util
import alsaaudio as aa
import audioop

class Driver:
	def __init__(self):
		self.terminateFlag=False
		patternString = ''
		helpString = 'Display.py -p <pattern>'

		try:
			opts, args = getopt.getopt(sys.argv[1:], "hp:", ["pattern"])
		except getopt.GetoptError:
			print helpString
			sys.exit(2)

		for opt, arg in opts:
			if opt == '-h':
				print helpString
				sys.exit()
			elif opt in ("-p", "--pattern"):
				patternString = arg.upper()
		
		pattern=getPatternFromString(patternString)
		if(pattern is None):
			print "Invalid pattern, options are: SMB3, SMB4, TULogo"
			sys.exit(3)
		self.display=self.initDisplay(pattern)
		
		self.audioPlaying=False
		self.audioProcessor=self.initAudio()
		print("Hello")
		
		
	
	def initDisplay(self, pattern):
		newDisplay=Display(Adafruit_RGBmatrix(32, 1), pattern)
		
		return newDisplay;
		
	def initAudio(self):
		#TODO Fix everything here. I did this quick and dirty, not up to documentation
		#very hacked here
		# Set up audio
		print("Begin audio 1")
		data_in = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NONBLOCK)
		data_in.setchannels(1)
		data_in.setrate(44100)
		data_in.setformat(aa.PCM_FORMAT_S16_LE)

		data_in.setperiodsize(256)
		
		
		
		return data_in#wrong return
	
	def runAudio(self, data_in):#not set to terminate cleanly
		audioPattern=Circles()
		print("audioStarting")
		while (not self.terminateFlag):
			# Read data from device
			l,data = data_in.read()
			if l:
				# catch frame error
				try:
					max_vol=audioop.max(data,2)#2 Bytes filter below 5000
					audioPattern.addAmplitudePoint(max_vol)
					if(max_vol>7000):#be extra sure here to avoid static (formerly 6000)
						if(not self.audioPlaying):
							self.audioPlaying=True
							self.display.currentPattern=audioPattern
					else:
						if(self.audioPlaying):
							self.audioPlaying=False
				except audioop.error, e:
					if e.message !="not a whole number of frames":
						raise e
			time.sleep(0)#let other threads work
		print ("Audio Thread Ending")
		
	
	def shutdown(self):
		self.display.shutdown()
		#self.audioProcessor.shutdown()
	
	def start(self):
		dispThread=Thread(target=self.display.start)
		audioThread=Thread(target=self.runAudio, args=(self.audioProcessor,))#also wrong input
		dispThread.start()
		audioThread.start()
		print("Blocking")
		
			
	
driver=Driver()
try:
	driver.start()
	while (True):
		time.sleep(2147483647)#Sleep forever... Join was problematic for some reason
except KeyboardInterrupt:
	print ("Exiting")
	driver.terminateFlag=True
	driver.shutdown()
	sys.exit()