import math

maxColor = 16777216
maxSound = 1500000000#22000
noiseThreshold = 450000000#6000
multiplier = (maxColor / float(maxSound))
byteSize = 256

def soundToColor(soundAmplitude):
	if (soundAmplitude < noiseThreshold):
		upscaledSound = 0
	else:
		upscaledSound = (soundAmplitude * multiplier) % maxColor
	

	red   = int(upscaledSound % byteSize)
	upscaledSound /= 255
	
	if(upscaledSound%2==1):
		red=255-red
		
	green = int(upscaledSound % byteSize)
	upscaledSound /= 255
	
	if(upscaledSound%2==1):
		green=255-green
		
	blue  = int(upscaledSound % byteSize)

	
	#print("R"+str(red)+"G"+str(green)+"B"+str(blue))
	return (red, green, blue)