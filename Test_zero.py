# needed for creating timestamp
import time
# needed just for testing
from random import random as rand
# pyLSL module
from pylsl import StreamInfo, StreamOutlet, local_clock

# setting of informations about LSL stream
info = StreamInfo('TestStream', 'Markers', 8, 100, 'int32', 'TestID0605')


outlet = StreamOutlet(info, 32, 360)


print("Now sending data...")
n = 0
while True:
    sample = ''
#    sample = [n, n, n, n, n, n, n, n]
    sample = [0, 0, 0, 0, 0, 0, 0, 0]
    stamp = local_clock()
    outlet.push_sample(sample, stamp)
    time.sleep(0.01)
#    n = n + 1

