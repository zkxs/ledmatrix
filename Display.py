
import Image
import ImageDraw
import time
import random
from rgbmatrix import Adafruit_RGBmatrix
from Pattern import Pattern
from Pattern import SMB3
from Pattern import SMB4

# Rows and chain length are both required parameters:
#matrix = Adafruit_RGBmatrix(32, 1)

class Display:
	
	def __init__(self):
		#self.updateTimer=0
		self.matrix=Adafruit_RGBmatrix(32, 1)
		self.patternTimer=0
		self.currentPattern=SMB3()
	
	def start(self):
		while(True):
			next=True
			while(next):
				next=not (self.update())
				time.sleep(self.currentPattern.getTimeStep())
			self.nextPattern()
	
	def drawPixels(self, image):
		self.matrix.SetImage(image.im.id, 0,0)
	
	def update(self):
		self.drawPixels(self.currentPattern.getPixels())
		return self.currentPattern.tick()
	
	def nextPattern(self):
		if random.random()<.5 :
			self.currentPattern=SMB3()
		else :
			self.currentPattern=SMB4()
	
	
disp=Display()
disp.start()