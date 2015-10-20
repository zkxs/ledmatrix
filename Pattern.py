
import Image
import ImageDraw
import time
from rgbmatrix import Adafruit_RGBmatrix

# Rows and chain length are both required parameters:
matrix = Adafruit_RGBmatrix(32, 1)

class Patttern:
	
	def __init__(self, maxStates):
		currentState=0
		self.maxStates=maxStates
		timeStep=1.0 #ms
	
	def tick(self):
		currentState+=1
		return currentState>=maxStates
	
	def getPixels(self):
		return
		
	def getTimeStep(self):
		return timeStep
		
class SMB3(Pattern):
	
	
	def __init__(self)
		super().__init__(55)
		timeStep=.5
		image=Image.open("SMB3gif/SMB3-"+str(currentState)+".gif")
	
	def tick(self):
		currentState+=1
		image=Image.open("SMB3gif/SMB3-"+str(currentState)+".gif")
		return currentState>=maxStates
	
	def getPixels(self):
		return image