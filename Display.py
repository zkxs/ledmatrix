#!/usr/bin/python

import Image
import ImageDraw
import time
import sys
import getopt
from rgbmatrix import Adafruit_RGBmatrix
from Pattern import *



class Display:

	def __init__(self, matrix, pattern):
		#self.updateTimer=0
		self.matrix=matrix
		self.patternTimer=0
		self.nextPattern= pattern
		self.currentPattern = pattern
		
	
	def start(self):
		while(True):
			next=True
			self.currentPattern = self.nextPattern()
			while(next):
				next=not (self.update())
				time.sleep(self.currentPattern.getTimeStep())

		
	
	def drawPixels(self, image):
		self.matrix.SetImage(image.im.id, 0,0)
	
	def update(self):
		self.drawPixels(self.currentPattern.getPixels())
		return self.currentPattern.tick()
	
	def shutdown(self):
		self.matrix.Clear()
	
# disp=Display(Adafruit_RGBmatrix(32, 1), lambda: randomPattern())
# try:
	# disp.start()
# except KeyboardInterrupt:
	# disp.shutdown()
	# sys.exit()

