import sys
import usb.core
import usb.util

dev = usb.core.find(idVendor=0x067b, idProduct=0x2303)

if dev is None:
        raise ValueError('Neco je spatne, zkus to znovu (Device not found)')

cfg = dev.get_active_configuration()

interface = 0
endpoint = dev[0][(0,0)][0]

if dev.is_kernel_driver_active(interface) is True:
	dev.detach_kernel_driver(interface)
	usb.util.claim_interface(dev, interface)
collected = 0
attempts = 50

while True:
	try:
		data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
		collected += 1
		print(str(data))
	except usb.core.USBError as e:
		data = None
		if e.args == ('Operation timed out',):
			continue

usb.util.release_interface(dev, interface)
dev.attach_kernel_driver(interface)
