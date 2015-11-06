import pygame, sys
from pygame.locals import *
import Image
import ImageDraw
import random
import util
import threading
from collections import deque
import pong
import numpy as np

class Pattern:
	
	def __init__(self, maxStates, timeStep):
		self.currentState=0
		self.maxStates=maxStates
		self.timeStep=timeStep # seconds
	
	def tick(self):
		self.currentState+=1
		return self.currentState>=self.maxStates
	
	def getPixels(self):
		# child classes override this behavior
		return
		
	def getTimeStep(self):
		return self.timeStep

def randomPattern():
	rand=random.random()
	if rand<.33 :
		return StaticImage(10, "Luigi.png")#Animated(55, .09, "SMB3")
	elif rand<.66 :
		return Animated(116, .05, "SMB4")
	else:
		return PongPattern()#return StaticImage(10, "TU.png")

def randomAudioPattern(audioProcessor):
	rand=random.random()
	if rand<.5 :
		return lambda: Circles(audioProcessor)
	else:
		return lambda: Bars(audioProcessor)
		
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
	elif patternString == "PONG":
		print "selected Pong pattern"
		return lambda: PongPattern()
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
		self.currentState= -1 # this is actually correct
		
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
	def __init__(self, maxStates, timeStep, audioProcessor):
		Pattern.__init__(self, maxStates, timeStep)#adjust second term to change timeout
		self.audioProcessor = audioProcessor
		self.ticksSinceAudio=0
		self.avalibleSamples=0
		self.image = Image.new("RGB", (32, 32))
		self.draw  = ImageDraw.Draw(self.image)
		self.lastVolume=0
	
	def getPixels(self):
		return self.image
		
	def tick(self):
		volume = self.audioProcessor.getAmplitude()
		self.lastVolume=(volume+self.lastVolume*self.avalibleSamples
			)//(self.avalibleSamples+1) # Weighted average
		self.avalibleSamples+=1
		if(volume>util.noiseThreshold):
			self.ticksSinceAudio=0
			
		self.ticksSinceAudio+=1 # concurrency on this variable is not vital
			
		return self.ticksSinceAudio > self.maxStates

		
		
class Circles(VolumePattern):
	def __init__(self, audioProcessor):
		VolumePattern.__init__(self, 75, .025, audioProcessor)
		self.pastData=deque()
		for i in range(23):
			self.pastData.append( (0, 0, 0) )
			
	def tick(self):
		toReturn = VolumePattern.tick(self)
		if(self.avalibleSamples!=0):
			self.pastData.popleft()
			self.pastData.append(util.soundToColor(self.lastVolume))
			self.avalibleSamples=0
		
		for r in range(23, 0, -1):
			color=self.pastData.popleft()
			self.draw.ellipse((16-r, 16-r, 16+r, 16+r), fill=color)
			self.pastData.append(color)
		
		return toReturn
		
class Bars(VolumePattern):
	def __init__(self, audioProcessor):
		VolumePattern.__init__(self, 75, .025, audioProcessor)
		self.numberOfBars = 16 # should probably be a factor of 32
		self.barWidth = 32 / self.numberOfBars
		
		self.barTops = np.zeros(self.numberOfBars)
		self.barCaps = np.zeros(self.numberOfBars)
		
		self.barTopVel = np.zeros(self.numberOfBars)
		self.barCapVel = np.zeros(self.numberOfBars)
		
		self.barTopAccel = 40
		self.barCapAccel = 10
		
		self.maxAmplitude = 5000
		self.minAmplitude = 0
		
		self.color_background = (  0,   0,   0)
		self.color_bar        = ( 15, 120,  15)
		self.color_bar_dark   = ( 10,  60,  10)
		self.color_cap        = (130,  30,  30)
		
	def scale(self, array):
		# scaled range is (32 - 0) = 32
		unscaledRange = self.maxAmplitude - self.minAmplitude
		return np.rint(np.clip((array - self.minAmplitude) * 32 / unscaledRange, 0, 32)).astype(int)
		
	def tick(self):
		toReturn = VolumePattern.tick(self)
		
		
		# get the FFT from the audio processor (drop the first item because it's pretty garbage)
		fft = (self.audioProcessor.getFFT())[0:self.numberOfBars]
		
		
		# update bar and cap positions and velocities
		for i in range(0, self.numberOfBars):
			if (fft[i] > self.barTops[i]):
				self.barTops[i] = fft[i]
				self.barTopVel[i] = 0
			else:
				self.barTopVel[i] += self.barTopAccel
			self.barTops[i] -= self.barTopVel[i]
				
			if (fft[i] > self.barCaps[i]):
				self.barCaps[i] = fft[i]
				self.barCapVel[i] = 0	
			else:
				self.barCapVel[i] += self.barCapAccel
			self.barCaps[i] -= self.barCapVel[i]
			
			
		# handle scaling of maximums
		maximum = np.amax(self.barCaps)
		if   (maximum > (self.maxAmplitude * 1.20)):
			self.maxAmplitude += 0.050 * (maximum - self.maxAmplitude)
		elif (maximum < (self.maxAmplitude * 0.10)):
			self.maxAmplitude += 0.010 * (maximum - self.maxAmplitude)	

		
		# draw bars
		self.draw.rectangle([(0, 0), (31, 31)], fill=self.color_background)
		scaledBars = self.scale(self.barTops)
		scaledCaps = self.scale(self.barCaps)
		
		for i in range(0, self.numberOfBars):
			
			x1 =  i * self.barWidth
			x2 = x1 + self.barWidth - 1
			y1Bar = 32 - scaledBars[i]
			y1Cap = 32 - scaledCaps[i]
			if (y1Cap >= 32):
				y1Cap = 31
			
			barColor = None
			if (i % 2 == 0):
				barColor = self.color_bar
			else:
				barColor = self.color_bar_dark
			
			self.draw.rectangle([(x1, y1Bar), (x2, 31   )], fill = barColor)
			self.draw.rectangle([(x1, y1Cap), (x2, y1Cap)], fill = self.color_cap)
		
		return toReturn
		
		
		
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
		toReturn = VolumePattern.tick(self)

		self.prevColor=util.soundToColor(self.lastVolume)
		self.avalibleSamples=0
		
		self.pastData.popleft()
		self.pastData.append(self.prevColor)
		
		for r in range(0, 1024, 1):
			color=self.pastData.popleft()
			self.draw.point((31-(r%32) , 31-(r//32)), fill=color)
			self.pastData.append(color)
		
		return toReturn

#Global Variables to be used through our program

# pong.WINDOWWIDTH = 32
# pong.WINDOWHEIGHT = 32
# pong.LINETHICKNESS = 2
# pong.PADDLESIZE = 10
# pong.PADDLEOFFSET = 1

# # Set up the colours
# pong.BLACK     = (0  ,0  ,0  )
# pong.WHITE     = (255,255,255)


class PongPattern(Pattern):
	def __init__(self):
		Pattern.__init__(self, 2500, .025)
		self.image = Image.new("RGB", (32, 32))
		self.draw  = ImageDraw.Draw(self.image)
		
		#Initiate variable and set starting positions
		#any future changes made within rectangles
		self.ballX = float(pong.WINDOWWIDTH/2 - pong.LINETHICKNESS/2)
		self.ballY = float(pong.WINDOWHEIGHT/2 - pong.LINETHICKNESS/2)
		self.playerOnePosition = (pong.WINDOWHEIGHT - pong.PADDLESIZE) /2
		self.playerTwoPosition = (pong.WINDOWHEIGHT - pong.PADDLESIZE) /2
		self.score = 0
		
	
		
		#Keeps track of ball direction
		self.ballDirX = 2*random.random()-1 ## -1 = left 1 = right
		self.ballDirY = 2*random.random()-1 ## -1 = up 1 = down
		
		#print ("dx,dy "+str(self.ballDirX)+", "+str(self.ballDirY))
		
		
		#Creates Rectangles for ball and paddles.
		self.paddle1 = pygame.Rect(pong.PADDLEOFFSET,self.playerOnePosition, pong.LINETHICKNESS,pong.PADDLESIZE)
		self.paddle2 = pygame.Rect(pong.WINDOWWIDTH - pong.PADDLEOFFSET - pong.LINETHICKNESS, self.playerTwoPosition, pong.LINETHICKNESS,pong.PADDLESIZE)
		self.ball = pygame.Rect(self.ballX, self.ballY, pong.LINETHICKNESS, pong.LINETHICKNESS)
		
		self.ballX=15.0;
		self.ballY=15.0;
		
		#Draws the starting position of the Arena
		self.drawArena()
		self.drawPaddle(self.paddle1)
		self.drawPaddle(self.paddle2)
		self.drawBall(self.ball)
	
	#Draws the arena the game will be played in. 
	def drawArena(self):
		self.draw.rectangle( ((-1,-1),(31,31)), fill=(0,0,0))
		#Draw centre line
		#self.draw.line((((pong.WINDOWWIDTH/2),0),((pong.WINDOWWIDTH/2),pong.WINDOWHEIGHT)), width=(pong.LINETHICKNESS), fill=pong.WHITE)


	#Draws the paddle
	def drawPaddle(self, paddle):
		#Stops paddle moving too low
		if paddle.bottom > pong.WINDOWHEIGHT - pong.LINETHICKNESS:
			paddle.bottom = pong.WINDOWHEIGHT - pong.LINETHICKNESS
		#Stops paddle moving too high
		elif paddle.top < pong.LINETHICKNESS:
			paddle.top = pong.LINETHICKNESS
		#Draws paddle
		self.draw.rectangle(((paddle.x,paddle.y),(paddle.x+pong.LINETHICKNESS,paddle.y+pong.PADDLESIZE)), fill=pong.WHITE)


	#draws the ball
	def drawBall(self, ball):
		self.draw.rectangle(((ball.x,ball.y),(ball.x+pong.LINETHICKNESS,ball.y+pong.LINETHICKNESS)), fill=pong.WHITE)

	#moves the ball returns new position
	def moveBall(self, ball, ballDirX, ballDirY):
		self.ballX += ballDirX
		self.ballY += ballDirY
		ball.x = int(self.ballX)
		ball.y = int(self.ballY)
		return ball

	def tick(self):
		self.drawArena()
		self.drawPaddle(self.paddle1)
		self.drawPaddle(self.paddle2)
		self.drawBall(self.ball)

		self.ball = self.moveBall(self.ball, self.ballDirX, self.ballDirY)
		self.ballDirX, self.ballDirY = pong.checkEdgeCollision(self.ball, self.ballDirX, self.ballDirY)
		self.score = pong.checkPointScored(self.paddle1, self.ball, self.score, self.ballDirX)
		self.ballDirX = self.ballDirX * pong.checkHitBall(self.ball, self.paddle1, self.paddle2, self.ballDirX)
		self.paddle1 = pong.artificialIntelligence1 (self.ball, self.ballDirX, self.paddle1)
		self.paddle2 = pong.artificialIntelligence2 (self.ball, self.ballDirX, self.paddle2)
		
		# print ("P1: "+str(self.playerOnePosition))
		# print ("P2: "+str(self.playerOnePosition))
		#print("Ball X,Y = "+str(self.ballX)+", "+str(self.ballY))
		#print (self.ball.centery)
		
		self.currentState+=1
		if((self.score)>0 or self.currentState>=self.maxStates):
			return True
		return False
	
	def getPixels(self):
		return self.image
