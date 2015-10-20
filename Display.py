
import Image
import ImageDraw
import time
from rgbmatrix import Adafruit_RGBmatrix
import Pattern

# Rows and chain length are both required parameters:
matrix = Adafruit_RGBmatrix(32, 1)

class Display:
	
	def __init__(self):
		#updateTimer=0
		patternTimer=0
		currentPattern=SMB3()
	
	def start(self):
		while(True)
			next=True
			while(next):
				next=not (update())
				time.sleep(currentPattern.getTimestep)
			self.nextPattern()
	
	def drawPixels(self, image):
		matrix.setImage(image, 0,0)
	
	def update(self):
		drawPixels()
	
	def nextPattern():
		currentPattern=SMB3()
	
	
disp=Display()
disp.start()