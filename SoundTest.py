#!/usr/bin/python

import alsaaudio as aa
import audioop
import time
import Image
import ImageDraw
import util
from collections import deque

from rgbmatrix import Adafruit_RGBmatrix
# Bitmap example w/graphics prims
image = Image.new("RGB", (32, 32)) # Can be larger than matrix if wanted!!
draw  = ImageDraw.Draw(image)    # Declare Draw instance before prims
pastData=deque()
for i in range(23):
	pastData.append( (0, 0, 0) )
matrix = Adafruit_RGBmatrix(32, 1)

# Set up audio
data_in = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NONBLOCK)
data_in.setchannels(1)
data_in.setrate(44100)
data_in.setformat(aa.PCM_FORMAT_S16_LE)

data_in.setperiodsize(256)

while True:
	# Read data from device
	l,data = data_in.read()
	if l:
		# catch frame error
		try:
			max_vol=audioop.max(data,2)
			#scaled_vol = max_vol//4680      
			print(max_vol)
			pastData.popleft()
			pastData.append(util.soundToColor(max_vol))
			for r in range(23, 0, -1):
				color=pastData.popleft()
				draw.ellipse((16-r, 16-r, 16+r, 16+r), outline=color)
				pastData.append(color)
				
			matrix.SetImage(image.im.id, 0, 0)
			time.sleep(0.025)



		except audioop.error, e:
			if e.message !="not a whole number of frames":
				raise e
