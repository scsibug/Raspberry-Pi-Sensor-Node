#!/usr/bin/python
import redis
import psycopg2
import json
import decimal
from settings import *
r = redis.StrictRedis(host='localhost', port=6379, db=0)

find_monitor_id_SQL = "select name,id from monitor_points"
insert_value_SQL = "insert into point_values (id, monitor_point, numeric_val, tstamp) values (DEFAULT, %(monitor_id)s, %(val)s, timestamptz 'epoch' + %(tstamp)s * INTERVAL '1 second')"
conn = psycopg2.connect(pg_conn_str)
curs = conn.cursor() 
curs.execute(find_monitor_id_SQL)    
monitor_lookup = dict(curs.fetchall())

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
  reading = json.loads(reading_json, parse_float=decimal.Decimal)
  # This second parse is temporary, as some early values were loaded as strings, and this serves to strip them
  fv = decimal.Decimal(reading["float"])
  monitor = reading["monitor"].strip()
  epoch = reading["time"]
  monitor_id = decimal.Decimal(monitor_lookup[monitor])
  if monitor_id is None:
    print("Monitor not found: "+monitor)
  print("Need to insert for monitor "+str(monitor_id)+" value "+str(fv))
  curs.execute(insert_value_SQL,{'monitor_id':monitor_id, 'val':fv, 'tstamp':epoch}) 
  conn.commit()
  # Commit completed, drop the message from redis
  r.lrem('failed_readings', 1, reading_json)
conn.commit()
curs.close()
conn.close()
#print r.lrange('sensor_readings',0,-1)
