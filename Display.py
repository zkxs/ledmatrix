#!/usr/bin/python

import Image
import ImageDraw
import time
import sys
import getopt
from rgbmatrix import Adafruit_RGBmatrix
from Pattern import *

class Display:

	def __init__(self, matrix, patternFactory, audioProcessor):
		self.matrix = matrix
		self.patternTimer = 0
		self.nextPattern = patternFactory
		self.currentPattern = patternFactory
		self.audioProcessor = audioProcessor
		self.terminateFlag = False
		self.audioPlaying = False
	
	def start(self):
		while (not self.terminateFlag):
			
			next = True
			
			if (self.audioPlaying):
				self.currentPattern=Circles(self.audioProcessor)
				while (next and not self.terminateFlag):
					next = not self.update()
					time.sleep(self.currentPattern.getTimeStep())
				self.audioPlaying = False
			
			self.currentPattern = self.nextPattern()
			while(next and not self.terminateFlag and not self.audioPlaying):
				next = not self.update()
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

	def notifyAudioPlaying(self):
		self.audioPlaying = True
