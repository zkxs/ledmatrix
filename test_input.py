#!/usr/bin/python3

# aplay -D plughw:CARD=ALSA,DEV=0 darude.wav
# aplay -D plughw:CARD=AUDIO,DEV=0 -f S16_LE -c 2 -r 44100 darude.wav
# arecord -D plughw:CARD=AUDIO,DEV=0 out.wav

from ctypes import *
import pyaudio
import sys
import time

WIDTH = 2
CHANNELS = 1
RATE = 8000

CHUNK = 1024
FORMAT = pyaudio.paInt8

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
	None #print('messages are yummy')
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = cdll.LoadLibrary('libportaudio.so.2')
asound.snd_lib_error_set_handler(c_error_handler)
pa = pyaudio.PyAudio()
asound.snd_lib_error_set_handler(None)

def find_input_device():
	for i in range( pa.get_device_count() ):
		devinfo = pa.get_device_info_by_index(i)
		print( "Device %d: %s"%(i,devinfo["name"]) )

		for keyword in ["usb"]:
			if keyword in devinfo["name"].lower():
				print( "Found an input: device %d - %s"%(i,devinfo["name"]) )
				device_index = i
				return device_index


device_index = find_input_device()

def callback(in_data, frame_count, time_info, status):
	data = wf.readframes(frame_count)
	return (data, pyaudio.paContinue)

stream = pa.open(   format = FORMAT,
					channels = CHANNELS,
					rate = RATE,
					input = True,
					input_device_index = device_index)

frames = []

while stream.is_active():
	time.sleep(0.1)
	
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	data = stream.read(CHUNK)
	frames.append(data)
	print(data)

stream.stop_stream()
stream.close()
pa.terminate()





