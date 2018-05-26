# PySerial module for interaction with USB devices
import serial
# needed for creating timestamp
import time
# needed just for testing
from random import random as rand
# pyLSL module
from pylsl import StreamInfo, StreamOutlet, local_clock

# setting of informations about LSL stream
info = StreamInfo('TestStream', 'Markers', 1, 0, 'string', 'TestID0605')

# appending metadata to stream
info.desc().append_child_value("owner", "EEGLab KIV ZCU")
channels = info.desc().append_child("channels")
channels.append_child("channel") \
        .append_child_value("label", "emg") \
        .append_child_value("unit", "String") \
        .append_child_value("type", "EMG data")

outlet = StreamOutlet(info, 32, 360)


ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

if ser is None:
        raise ValueError('Neco je spatne, zkus to znovu (Device not found)')

print("Now sending data...")
while True:
    sample = ser.readline()
    print(sample)
    stamp = local_clock()
    outlet.push_sample(sample, stamp)

