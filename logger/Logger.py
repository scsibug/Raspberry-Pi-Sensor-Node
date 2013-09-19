#!/usr/bin/python
from time import sleep
from Adafruit_BMP085 import BMP085
from TMP102 import TMP102
from subprocess import check_output

bmp = BMP085(0x77, 3, debug=False)  # ULTRAHIRES Mode
temp = bmp.readTemperature()
pressure = bmp.readPressure()

#print "Temperature: %.2f C" % temp
#print "Temperature: %.2f F" % (9.0/5.0 * temp  + 32)
#print "Pressure:    %.2f hPa" % (pressure / 100.0)

#log = open("data_log.csv", "a")

epoch = check_output(["date", "+%s"]).rstrip()
print("  at time "+epoch)
print "BMP085 Pressure/Temperature Sensor"

print("\tTemperature: "+str(bmp.readTemperature())+" C")
print("\tPressure: "+str(bmp.readPressure())+" hPa")
print("\n")

tmp102 = TMP102(0x49)
tmp102_temp = tmp102.readTemperature()
print "TMP102 Temperature Sensor"
print("\tTemperature: "+str(tmp102_temp)+" C")
