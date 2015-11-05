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
		self.matrix=matrix
		self.patternTimer=0
		self.nextPattern= pattern
		self.currentPattern = pattern
		self.terminateFlag=False
	
	def start(self):
		while(not self.terminateFlag):
			next=True
			self.currentPattern = self.nextPattern()
			while(next):
				next=not (self.update())
				time.sleep(self.currentPattern.getTimeStep())
		self.matrix.Clear()
		print ("Display Thread Ending")
	
	def drawPixels(self, image):
		self.matrix.SetImage(image.im.id, 0, 0)
	
	def update(self):
		self.drawPixels(self.currentPattern.getPixels())
		return self.currentPattern.tick()
	
	def shutdown(self):
		self.terminateFlag=True
