#!/usr/bin/python
import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)
print r.lrange('sensor_readings',0,-1)
