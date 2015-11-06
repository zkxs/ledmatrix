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
from AudioProcessor import AudioProcessor

class Driver:
	def __init__(self):
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
		
		
		self.audioProcessor=self.initAudio()
		print("Hello")
		
		
	
	def initDisplay(self, pattern):
		newDisplay=Display(Adafruit_RGBmatrix(32, 1), pattern)
		
		return newDisplay;
		
	def initAudio(self):
		newAudio=AudioProcessor(self.display);
		return newAudio
	
		
	
	def shutdown(self):
		self.display.shutdown()
		self.audioProcessor.shutdown()
	
	def start(self):
		dispThread=Thread(target=self.display.start)
		audioThread=Thread(target=self.audioProcessor.start)#also wrong input
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
	
	driver.shutdown()
