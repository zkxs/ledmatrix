
import Image
import ImageDraw
import random
import util
import threading
from collections import deque

class Pattern:
	
	def __init__(self, maxStates, timeStep):
		self.currentState=0
		self.maxStates=maxStates
		self.timeStep=timeStep #s
	
	def tick(self):
		self.currentState+=1
		return self.currentState>=self.maxStates
	
	def getPixels(self):
		return
		
	def getTimeStep(self):
		return self.timeStep

def randomPattern():
	rand=random.random()
	if rand<.33 :
		return Animated(55, .09, "SMB3")
	elif rand<.66 :
		return Animated(116, .05, "SMB4")
	else:
		return StaticImage(10, "TU.png")

def getPatternFromString(patternString):	
	if patternString == "SMB3":
		print "selected SMB3 pattern"
		return lambda: Animated(55, .09, "SMB3")
	elif patternString == "SMB4":
		print "selected SMB4 pattern"
		return lambda: Animated(116, .05, "SMB4")
	elif patternString == "TULOGO":
		print "selected TULOGO pattern"
		return lambda: StaticImage(10, "TU.png")
	elif patternString == "":
		print "selected random pattern"
		return lambda: randomPattern()
	else:
		return None

class Animated(Pattern):
	def __init__(self, numFrames, timeStep, fileName):
		Pattern.__init__(self, numFrames, timeStep)
		self.fileName=fileName
		self.image=Image.open(
			fileName+"gif/"+fileName+"-"+str(self.currentState)+".gif")
		self.image.load()
	
	def tick(self):
		self.currentState+=1
		self.image=Image.open(
			self.fileName+"gif/"+self.fileName+"-"+str(self.currentState)+".gif")
		self.image.load()
		return self.currentState>=self.maxStates
	
	def getPixels(self):
		return self.image
	
	def restart(self):
		self.currentState=0
		
class StaticImage(Pattern):
	def __init__(self, maxTime, fileName):
		Pattern.__init__(self, maxTime, (maxTime/10))
		self.image=Image.open(fileName)
		self.image.load()
	
	def tick(self):
		self.currentState+=1
		return self.currentState>=self.maxStates
	
	def getPixels(self):
		return self.image

class VolumePattern(Pattern):
	def __init__(self, maxStates, timeStep):
		Pattern.__init__(self, maxStates, timeStep)#adjust second term to change timeout
		self.ticksSinceAudio=0
		self.avalibleSamples=0
		self.image = Image.new("RGB", (32, 32))
		self.draw  = ImageDraw.Draw(self.image)
		self.audioLock=threading.Lock()
		self.newVolume=0
		
	def addAmplitudePoint(self, volume):
		if (self.audioLock.acquire(0)==0):
			return False#will ignore data input in this case
		else:
			self.newVolume=(volume+self.newVolume*self.avalibleSamples
				)//(self.avalibleSamples+1)#Weighted average
			self.avalibleSamples+=1
			self.audioLock.release()
			if(volume>6000):
				self.ticksSinceAudio=0#concurrency on this variable is not important
			return True
	
	def getPixels(self):
		return self.image

		
		
class Circles(VolumePattern):
	def __init__(self):
		VolumePattern.__init__(self, 100, .025)
		self.pastData=deque()
		for i in range(23):
			self.pastData.append( (0, 0, 0) )
			
	def tick(self):
		self.audioLock.acquire(1)
		if(self.avalibleSamples!=0):
			self.pastData.popleft()
			self.pastData.append(util.soundToColor(self.newVolume))
			self.avalibleSamples=0
		self.audioLock.release()
		
		for r in range(23, 0, -1):
			color=self.pastData.popleft()
			self.draw.ellipse((16-r, 16-r, 16+r, 16+r), fill=color)
			self.pastData.append(color)
		
		self.ticksSinceAudio+=1#concurrency on this variable is not vital
		
		return self.ticksSinceAudio>=self.maxStates
		
class BoringLines(VolumePattern):# I was bored this is bad do not use
	"""I'm really not sure what this is doing, but it stalls noticeably
	and randomly reverses direction"""
	def __init__(self):
		VolumePattern.__init__(self, 500, 0)
		self.prevColor=(0,0,0)
		self.pastData=deque()
		for i in range(1024):
			self.pastData.append( (0, 0, 0) )
			
	def tick(self):
		locked=self.audioLock.acquire(0)
		if(locked==1):
			self.prevColor=util.soundToColor(self.newVolume)
			self.avalibleSamples=0
			self.audioLock.release()
		else:
			self.pastData.append(self.prevColor)
		
		self.pastData.popleft()
		self.pastData.append(self.prevColor)
		
		for r in range(0, 1024, 1):
			color=self.pastData.popleft()
			self.draw.point((31-(r%32) , 31-(r//32)), fill=color)
			self.pastData.append(color)
		
		self.ticksSinceAudio+=1#concurrency on this variable is not vital
		
		return self.ticksSinceAudio>=self.maxStates