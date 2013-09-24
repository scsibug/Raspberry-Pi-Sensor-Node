#!/usr/bin/python
import time
import json
import redis
from Adafruit_BMP085 import BMP085
from TMP102 import TMP102
from subprocess import check_output
import re

def main():
  # BMP085
  bmp_tpoint = "dajeil.BMP085.temp.1"
  bmp_ppoint = "dajeil.BMP085.pressure.1"
  bmp = BMP085(0x77, 3, debug=False)  # ULTRAHIRES Mode
  temp = bmp.readTemperature()
  publish_metric(bmp_tpoint, str(temp), "float")
  pressure = bmp.readPressure()
  publish_metric(bmp_ppoint, str(pressure), "float")
  # TMP102
  tmp_point = "dajeil.TMP102.temp.1"
  tmp102 = TMP102(0x49)
  tmp102_temp = tmp102.readTemperature()
  publish_metric(tmp_point, tmp102_temp, "float")
  print("TMP102 Temperature Sensor")
  print("\tTemperature: "+str(tmp102_temp)+" C")
  # SOC Temp
  get_soc_temp()

def get_soc_temp():
  tempre = re.compile("temp=")
  temprec = re.compile("'C")  
  tempstr = check_output(["/opt/vc/bin/vcgencmd", "measure_temp"]).rstrip()
  tempstr = tempre.sub("",tempstr)
  tempc = temprec.sub("",tempstr) 
  publish_metric("dajeil.SOC.temp.1",tempc, "float")

def publish_metric(name, value, type):
  """Record a metric for a given name, with value, for type.  Valid types are float, string, int."""
  t = time.time()
  m = json.dumps({'monitor':name, type:value, 'time':t})
  r = redis.StrictRedis(host='localhost', port=6379, db=0)  
  r.lpush('sensor_readings',m)


main()
