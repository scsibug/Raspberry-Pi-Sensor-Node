#!/usr/bin/python
from time import sleep
from Adafruit_BMP085 import BMP085
from subprocess import check_output
bmp = BMP085(0x77, 3, debug=False)  # ULTRAHIRES Mode
temp = bmp.readTemperature()
pressure = bmp.readPressure()

#print "Temperature: %.2f C" % temp
#print "Temperature: %.2f F" % (9.0/5.0 * temp  + 32)
#print "Pressure:    %.2f hPa" % (pressure / 100.0)

log = open("data_log.csv", "a")

while True:
  bmp_temp = bmp.readTemperature()
  bmp_pressure = bmp.readPressure()
  epoch = check_output(["date", "+%s"]).rstrip()
  log.write("BMP085_temp,"+epoch+","+str(bmp_temp)+"\n")
  log.write("BMP085_pressure,"+epoch+","+str(bmp_pressure)+"\n")
  sleep(10)
