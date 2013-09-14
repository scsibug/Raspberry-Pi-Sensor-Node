#!/usr/bin/python

from Adafruit_BMP085 import BMP085
bmp = BMP085(0x77, 3)  # ULTRAHIRES Mode
temp = bmp.readTemperature()
pressure = bmp.readPressure()

print "Temperature: %.2f C" % temp
print "Pressure:    %.2f hPa" % (pressure / 100.0)
