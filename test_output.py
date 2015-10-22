#!/usr/bin/python3

# aplay -D plughw:CARD=ALSA,DEV=0 darude.wav
# aplay -D plughw:CARD=AUDIO,DEV=0 -f S16_LE -c 2 -r 44100 darude.wav

from ctypes import *
import pyaudio
import wave
import sys
import time

CHUNK = 2048

if len(sys.argv) < 2:
	print("Plays a wave file.\n\nUsage: %s filename.wav" + sys.argv[0])
	sys.exit(-1)

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


# begin file

print("\nSHIT IS NOW STARTING FOR REAL\n")

wf = wave.open(sys.argv[1], 'rb')

device_index = find_input_device()

def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)

stream = pa.open(   format = pa.get_format_from_width(wf.getsampwidth()),
					channels = wf.getnchannels(),
					rate = wf.getframerate(),
					output = True,
					stream_callback=callback)

#data = wf.readframes(CHUNK)

while stream.is_active():
	time.sleep(0.1)

stream.stop_stream()
stream.close()
wf.close()

pa.terminate()





