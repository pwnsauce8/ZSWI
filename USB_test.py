#!/usr/bin/python

import sys
import usb.core
import usb.util

dev = usb.core.find(idVendor=0x062a, idProduct=0x4101)

if dev is None:
        raise ValueError('Něco je špatně, zkus to znovu (Device not found)')

cfg = dev.get_active_configuration()

interface = 0
endpoint = dev[0][(0,0)][0]

if dev.is_kernel_driver_active(interface) is True:
	dev.detach_kernel_driver(interface)
	usb.util.claim_interface(dev, interface)
collected = 0
attempts = 50

while collected < attempts:
	try:
		data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
		collected += 
		print data
	except usb.core.USBError as e:
		data = None
		if e.args == ('Operation timed out',):
			continue

usb.util.release_interface(dev, interface)
dev.attach_kernel_driver(interface)
