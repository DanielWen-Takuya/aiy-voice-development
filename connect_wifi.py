#!/usr/bin/python
from __future__ import print_function

from wifi import Cell, Scheme

scheme = Scheme.find('wlan0', 'Bbox-ABEDB871')

if scheme is None:
	# create a scheme and save it
	print('failed to find the saved wifi, creating and connecting')
	cell = Cell.all('wlan0')[0]
	scheme = Scheme.for_cell('wlan0','Bbox-ABEDB871',cell, 'DC12E15225D23FF5F2A5FAD3496134')
	scheme.save()

scheme.activate()