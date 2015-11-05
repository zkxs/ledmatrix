import alsaaudio as aa
import audioop
from Display import Display
from Pattern import *
import time

class AudioProcessor:
	def __init__(self, display):
		self.terminateFlag=False
		self.data_in = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NONBLOCK)
		self.data_in.setchannels(1)
		self.data_in.setrate(44100)
		self.data_in.setformat(aa.PCM_FORMAT_S16_LE)

		self.data_in.setperiodsize(256)
		self.audioPlaying=False
		self.display=display
	
	def start(self):#not set to terminate cleanly
		audioPattern=Circles()
		print("audioStarting")
		while (not self.terminateFlag):
			# Read data from device
			l,data = self.data_in.read()
			if l:
				# catch frame error
				try:
					max_vol=audioop.max(data,2)#2 Bytes filter below 5000
					audioPattern.addAmplitudePoint(max_vol)
					if(max_vol>7000):#be extra sure here to avoid static (formerly 6000)
						if(not self.audioPlaying):
							self.audioPlaying=True
							self.display.currentPattern=audioPattern
					else:
						if(self.audioPlaying):
							self.audioPlaying=False
				except audioop.error, e:
					if e.message !="not a whole number of frames":
						raise e
			time.sleep(0)#let other threads work
		print ("Audio Thread Ending")
	
	def shutdown(self):
		self.terminateFlag=True