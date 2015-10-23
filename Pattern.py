
import Image
import ImageDraw

class Pattern:
	
	def __init__(self, maxStates):
		self.currentState=0
		self.maxStates=maxStates
		self.timeStep=1.0 #ms
	
	def tick(self):
		self.currentState+=1
		return self.currentState>=self.maxStates
	
	def getPixels(self):
		return
		
	def getTimeStep(self):
		return self.timeStep
		
class SMB3(Pattern):
	def __init__(self):
		Pattern.__init__(self, 55)
		self.timeStep=.09
		self.image=Image.open("SMB3gif/SMB3-"+str(self.currentState)+".gif")
		self.image.load()
	
	def tick(self):
		self.currentState+=1
		self.image=Image.open("SMB3gif/SMB3-"+str(self.currentState)+".gif")
		self.image.load()
		return self.currentState>=self.maxStates
	
	def getPixels(self):
		return self.image
		
class SMB4(Pattern):
	def __init__(self):
		Pattern.__init__(self, 116)
		self.timeStep=.05
		self.image=Image.open("SMB4gif/SMB4-"+str(self.currentState)+".gif")
		self.image.load()
	
	def tick(self):
		self.currentState+=1
		self.image=Image.open("SMB4gif/SMB4-"+str(self.currentState)+".gif")
		self.image.load()
		return self.currentState>=self.maxStates
	
	def getPixels(self):
		return self.image
		
class TULogo(Pattern):
	def __init__(self):
		Pattern.__init__(self, 100)
		self.timeStep=.1
		self.image=Image.open("TU.png")
		self.image.load()
	
	def tick(self):
		self.currentState+=1
		return self.currentState>=self.maxStates
	
	def getPixels(self):
		return self.image