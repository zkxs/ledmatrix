#!/usr/bin/python

import Image
import ImageDraw
import time
import random
import sys
import getopt
from rgbmatrix import Adafruit_RGBmatrix
from Pattern import Pattern
from Pattern import SMB3
from Pattern import SMB4
from Pattern import TULogo

# Rows and chain length are both required parameters:
#matrix = Adafruit_RGBmatrix(32, 1)

def randomPattern():
		rand=random.random()
		if rand<.33 :
			return SMB3()
		elif rand<.66 :
			return SMB4()
		else:
			return TULogo()

class Display:

	def __init__(self):
		#self.updateTimer=0
		self.matrix=Adafruit_RGBmatrix(32, 1)
		self.patternTimer=0
		self.nextPattern=None
		
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
		
		if patternString == "SMB3":
			self.nextPattern = lambda: SMB3()
			print "selected SMB3 pattern"
		elif patternString == "SMB4":
			self.nextPattern = lambda: SMB4()
			print "selected SMB4 pattern"
		elif patternString == "TULOGO":
			self.nextPattern = lambda: TULogo()
			print "selected TULOGO pattern"
		elif patternString == "":
			self.nextPattern = lambda: randomPattern()
				
			print "selected random pattern"
		else:
			print "Invalid pattern, options are: SMB3, SMB4, TULogo"
			sys.exit(3)
	
	def start(self):
		try:
			while(True):
				next=True
				self.currentPattern = self.nextPattern()
				while(next):
					next=not (self.update())
					time.sleep(self.currentPattern.getTimeStep())
				
		except KeyboardInterrupt:
			self.matrix.Clear()
			sys.exit()
		
	
	def drawPixels(self, image):
		self.matrix.SetImage(image.im.id, 0,0)
	
	def update(self):
		self.drawPixels(self.currentPattern.getPixels())
		return self.currentPattern.tick()

disp=Display()
disp.start()
