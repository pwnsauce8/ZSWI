# PyUSB module for interaction with USB devices
import usb.core
import usb.util
# needed for creating timestamp
import time
# needed just for testing
from random import random as rand
# pyLSL module
from pylsl import StreamInfo, StreamOutlet, local_clock

# setting of informations about LSL stream
info = StreamInfo('TestStream', 'EEG', 8, 100, 'float32', 'TestID0605')

# appending metadata to stream
info.desc().append_child_value("manufacturer", "Kalivoda")
channels = info.desc().append_child("channels")
for c in ["x", "y"]:
    channels.append_child("channel") \
        .append_child_value("label", c) \
        .append_child_value("unit", "Coords") \
        .append_child_value("type", "TestData")

outlet = StreamOutlet(info, 32, 360)

print("now sending data...")
n = 0
while True:
#    sample = [n, n, n, n, n, n, n, n]
    sample = [0, 0, 0, 0, 0, 0, 0, 0]
    stamp = local_clock()
    outlet.push_sample(sample, stamp)
    time.sleep(0.01)
    n = n + 1

