import alsaaudio as aa
import audioop
from Display import Display
import util
import time
import numpy as np
import sys
from collections import deque
import threading

class AudioProcessor:
	
	BUFFER_SIZE = 1024
	PERIOD_SIZE = 128 #128
	
	SAMPLE_FORMAT = aa.PCM_FORMAT_S16_LE
	SAMPLE_BYTES = 2 # must match the number of bytes in sample format
	MAX_AMPLITUDE = 2 ** (8 * SAMPLE_BYTES) - 1
	
	def __init__(self):
		self.terminateFlag=False
		self.data_in = aa.PCM(aa.PCM_CAPTURE)
		self.data_in.setchannels(1)
		self.data_in.setrate(44100)
		self.data_in.setformat(self.SAMPLE_FORMAT)
		self.data_in.setperiodsize(self.PERIOD_SIZE)
		self.audioPlaying=False
		self.display=None
		self.lock = threading.Lock()
		
		self.maxVolume = None
		self.fft = None
		self.fftDirty = True
		
		#self.sampleBuffer = np.zeros(5, dtype=np.int)
		#self.sampleBuffer = deque(maxlen=self.BUFFER_SIZE)
		#for i in range(self.BUFFER_SIZE):
		#	self.sampleBuffer.append(0)
		
	def attachDisplay(self, display):
		self.display=display
			
	
	def start(self):#not set to terminate cleanly
		print("audioStarting")
		while (not self.terminateFlag):
			# Read data from device
			l,data = self.data_in.read()
			
			if (l == self.PERIOD_SIZE): # sometimes ALSA returns a negative error code. I ignore this.
				arr = self.MAX_AMPLITUDE - np.fromstring(data, dtype='<u2') # little endian unsigned 2-byte numbers
				assert arr.size == self.PERIOD_SIZE, "unexpected array size: " + str(arr.size)
				
				self.maxVolume = np.amax(arr)
				
				localFFT = np.absolute(np.fft.rfft(arr))
				localFFT = localFFT[1:]
				
				self.lock.acquire()
				self.fftDirty = True
				self.fft = localFFT
				self.lock.release()
				
				time.sleep(0.01)
			
			
					
			###audioPattern.addAmplitudePoint(self.maxVolume)
			if(self.maxVolume>util.noiseThreshold): # be extra sure here to avoid static
				if(not self.audioPlaying):
					self.audioPlaying=True
					if (self.display is not None):
						self.display.notifyAudioPlaying()
			else:
				if(self.audioPlaying):
					self.audioPlaying=False
							
			time.sleep(.001) #let other threads work
			
		print ("Audio Thread Ending")
		
	def getAmplitude(self):
		return self.maxVolume
		
	def getFFT(self):
		self.lock.acquire()
		if self.fftDirty:
			fftCopy = np.copy(self.fft)
			self.fftDirty = False
		self.lock.release()
		return fftCopy
	
	def shutdown(self):
		self.terminateFlag=True
