#!/usr/bin/python
import redis
import sys
import hmac
import hashlib
import json
import decimal
import urllib2
import time
import argparse
import os
from settings import *
r = redis.StrictRedis(host='localhost', port=6379, db=0)

print "using "+os.environ['EVENT_SECRET_KEY']

parser = argparse.ArgumentParser(description='Write sensor value to remote server.')
parser.add_argument('--host', help='remote host to send updates to')
args = parser.parse_args()

# move all failed_readings back onto the sensor_readings list
failed_count = 0
while True:
  failed_msg = r.rpoplpush('failed_readings', 'sensor_readings')
  if failed_msg is None:
    break
  else:
   failed_count += 1 

if failed_count > 0:
  print("Recovered "+str(failed_count)+" readings")
else:
  print("No cleanup necessary from previous run")

# take all the current items from the redis list
#sensor_readings = r.lrange('sensor_readings',0,-1)
# each of these results is a json string
while True:
  reading_json = r.rpoplpush('sensor_readings', 'failed_readings')
  if reading_json is None:
    break;
  #{"float": "27.0", "monitor": "dajeil.BMP085.temp.1", "time": 1379569873.699045}
  print "Raw JSON is: "+reading_json
  reading = json.loads(reading_json, parse_float=decimal.Decimal)
  # This second parse is temporary, as some early values were loaded as strings, and this serves to strip them
  fv = str(reading["float"])
  monitor = reading["monitor"].strip()
  epoch = reading["time"]
  # create json with new format
  data = json.dumps({"type": "float", "value": fv, "monitor": monitor, "time": float(epoch)})
  print data
  authz = "HMAC "+hmac.new(os.environ['EVENT_SECRET_KEY'],data,hashlib.sha256).hexdigest()
  req = urllib2.Request(args.host, data, {'Content-Type': 'application/json', 'Authorization': authz})
  f = urllib2.urlopen(req)
  response = f.read()
  print response
  f.close() 
  # Commit completed, drop the message from redis
  r.lrem('failed_readings', 1, reading_json)
#print r.lrange('sensor_readings',0,-1)
