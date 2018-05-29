# PySerial module for interaction with USB devices
import serial
# needed for creating timestamp
import time
# pyLSL module
from pylsl import StreamInfo, StreamOutlet, local_clock

# sets device to be read (e.g. /dev/ttyUSB0)
port = input('type SerialPort to use:')
rate = input('set sampling rate of the connected device:')

"""
setting of informations about LSL stream.
Order of arguments: name of the stream, content type, number of channels, sampling rate,
and stream indentifier (useful for auto-recovering interrupted connections
"""
info = StreamInfo('EMG_Stream', 'EMG', 1, rate, 'int32', 'ZSWI')

# appending metadata to stream
info.desc().append_child_value("owner", "EEGLab KIV ZCU")
channels = info.desc().append_child("channels")
channels.append_child("channel") \
        .append_child_value("label", "emg") \
        .append_child_value("unit", "int") \
        .append_child_value("type", "EMG data")

# creating outlet with given info, with chunk size 32 samples and
# buffer size set to 360 seconds
outlet = StreamOutlet(info, 32, 360)

print("Now sending data...")
with serial.Serial(port, 115200, timeout=1) as ser:
	while True:
		line = ser.readline()
#		print(str(line))
		length = len(line)
		try:
			stamp = local_clock()
			sample = int(line.decode('utf-8'))
			print(sample)
			outlet.push_sample([sample], stamp)
		except ValueError as e:
			print('No Value: {0}'.format(e))
