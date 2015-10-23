import math

maxColor = 16777216
maxSound = 22000
noiseThreshold = 6000
multiplier = maxColor / maxSound
byteSize = 256

def soundToColor(soundAmplitude):
	if (soundAmplitude < noiseThreshold):
		upscaledSound = 0
	else:
		upscaledSound = (soundAmplitude * multiplier) % maxColor
	
	
	red   = upscaledSound % byteSize
	upscaledSound /= 255
	green = upscaledSound % byteSize
	upscaledSound /= 255
	blue  = upscaledSound % byteSize