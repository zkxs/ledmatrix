import math

maxColor = 16777216
maxSound = 65565
noiseThreshold = 8000
multiplier = (maxColor / float(maxSound))
byteSize = 256

def soundToColor(soundAmplitude):
	if (soundAmplitude < noiseThreshold):
		upscaledSound = 0
	else:
		upscaledSound = (soundAmplitude * multiplier) % maxColor
	

	blue   = int(upscaledSound % byteSize)
	upscaledSound /= 255
	
	if(upscaledSound%2==1):
		blue=255-blue
		
	green = int(upscaledSound % byteSize)
	upscaledSound /= 255
	
	if(upscaledSound%2==1):
		green=255-green
		
	red  = int(upscaledSound % byteSize)

	
	#print("R"+str(red)+"G"+str(green)+"B"+str(blue))
	return (red, green, blue)
