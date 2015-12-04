#!/usr/bin/python

# A more complex RGBMatrix example works with the Python Imaging Library,
# demonstrating a few graphics primitives and image loading.
# Note that PIL graphics do not have an immediate effect on the display --
# image is drawn into a separate buffer, which is then copied to the matrix
# using the SetImage() function (see examples below).
# Requires rgbmatrix.so present in the same directory.

# PIL Image module (create or load images) is explained here:
# http://effbot.org/imagingbook/image.htm
# PIL ImageDraw module (draw shapes to images) explained here:
# http://effbot.org/imagingbook/imagedraw.htm

import Image
import os#added for gif separation
import getopt
import sys

"""
# Bitmap example w/graphics prims
image = Image.new("1", (32, 32)) # Can be larger than matrix if wanted!!
draw  = ImageDraw.Draw(image)    # Declare Draw instance before prims
# Draw some shapes into image (no immediate effect on matrix)...
draw.rectangle((0, 0, 31, 31), fill=0, outline=1)
draw.line((0, 0, 31, 31), fill=1)
draw.line((0, 31, 31, 0), fill=1)
# Then scroll image across matrix...
for n in range(-32, 33): # Start off top-left, move off bottom-right
	matrix.Clear()
	# IMPORTANT: *MUST* pass image ID, *NOT* image object!
	matrix.SetImage(image.im.id, n, n)
	time.sleep(0.05)
"""

def supermakedirs(path, mode):
    if not path or os.path.exists(path):
        return []
    (head, tail) = os.path.split(path)
    res = supermakedirs(head, mode)
    os.mkdir(path)
    os.chmod(path, mode)
    res += [path]
    return res
	
def extractFrames(inGif):
	frame = Image.open(inGif+".gif")
	outFolder=inGif+"gif"
	if not os.path.exists(outFolder):
		supermakedirs(outFolder, 0777)
	
	nframes = 0
	while frame:
		frame.save( '%s/%s-%s.gif' % (outFolder, os.path.basename(inGif), nframes ) , 'GIF')
		os.chmod('%s/%s-%s.gif' % (outFolder, os.path.basename(inGif), nframes ), 0777)
		nframes += 1
		try:
			frame.seek( nframes )
		except EOFError:
			break
	print(nframes)
	return nframes

	
helpString = 'GifSplitter.py -f <Gif file>'
try:
	opts, args = getopt.getopt(sys.argv[1:], "hf:", ["help","filename="])
except getopt.GetoptError:
	print helpString
	sys.exit(2)

for opt, arg in opts:
	if opt in ("-h", "--help"):
		print helpString
		sys.exit()
	elif opt in ("-f", "--filename"):
		fileName = arg.upper()
		extractFrames(fileName)
		
	
	
