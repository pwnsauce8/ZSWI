# PySerial module for interaction with USB devices
import serial
# needed for creating timestamp
import time
# needed just for testing
from random import random as rand
# pyLSL module
from pylsl import StreamInfo, StreamOutlet, local_clock

port = input('type SerialPort to use:')

# setting of informations about LSL stream
info = StreamInfo('TestStream', 'EMG', 1, 100, 'int32', 'ZSWI')

# appending metadata to stream
info.desc().append_child_value("owner", "EEGLab KIV ZCU")
channels = info.desc().append_child("channels")
channels.append_child("channel") \
        .append_child_value("label", "emg") \
        .append_child_value("unit", "int") \
        .append_child_value("type", "EMG data")

outlet = StreamOutlet(info, 32, 360)

print("Now sending data...")
with serial.Serial(port, 115200, timeout=1) as ser:
	while True:
		line = str(ser.readline())
		print(line)
		length = len(line)
		sample = int(line[2:length-5])
		print(sample)
		stamp = local_clock()
		outlet.push_sample([sample], stamp)
