import alsaaudio as aa
import audioop
from Display import Display
from Pattern import *
import util
import time
import numpy as np
from collections import deque

class AudioProcessor:
	
	BUFFER_SIZE = 128
	
	def __init__(self, display):
		self.terminateFlag=False
		self.data_in = aa.PCM(aa.PCM_CAPTURE)
		self.data_in.setchannels(1)
		self.data_in.setrate(44100)
		self.data_in.setformat(aa.PCM_FORMAT_S16_LE)
		self.data_in.setperiodsize(64)
		self.audioPlaying=False
		self.display=display
		
		#self.sampleBuffer = np.zeros(5, dtype=np.int)
		self.sampleBuffer = deque(maxlen=self.BUFFER_SIZE)
		for i in range(self.BUFFER_SIZE):
			self.sampleBuffer.append(0)
			
	
	def start(self):#not set to terminate cleanly
		audioPattern=Circles()
		print("audioStarting")
		while (not self.terminateFlag):
			# Read data from device
			l,data = self.data_in.read()
			print(data)
			print("\n\n\n\n")
			if l:
				# catch frame error
				try:
					max_vol=audioop.max(data,4)#2 Bytes filter below 5000 369038784 1417630784
					#400000000

					#print(max_vol)
					audioPattern.addAmplitudePoint(max_vol)
					if(max_vol>util.noiseThreshold):#be extra sure here to avoid static (formerly 6000)
						if(not self.audioPlaying):
							self.audioPlaying=True
							self.display.currentPattern=audioPattern
					else:
						if(self.audioPlaying):
							self.audioPlaying=False
				except audioop.error, e:
					if e.message !="not a whole number of frames":
						raise e
			time.sleep(1)#let other threads work
		print ("Audio Thread Ending")
	
	def shutdown(self):
		self.terminateFlag=True