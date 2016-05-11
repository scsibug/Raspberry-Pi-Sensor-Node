#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import smbus
import time
print "Starting HTTP Temperature Server"

bus = smbus.SMBus(1)

def read_temp():
  data = bus.read_i2c_block_data(0x49, 0)
  msb = data[0]
  lsb = data[1]
  return (((msb << 8) | lsb) >> 4) * 0.0625

def read_humidity():
  d = []
  addr = 0x27
  bus.write_quick(addr)
  time.sleep(0.05)
  d = bus.read_i2c_block_data(addr, 0,4)
  status = (d[0] & 0xc0) >> 6
  humidity = (((d[0] & 0x3f) << 8) + d[1])*100/16383
  tempC = ((d[2] << 6) + ((d[3] & 0xfc) >> 2))*165/16383 - 40
  tempF = tempC*9/5 + 32
  #print "Humidity:   ", humidity, "%"
  #print "Temperature:", tempF, "F"
  return humidity

class EnvHTTPRequestHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    try:
      # Get the temperature
      temp = read_temp()
      humidity = read_humidity()
      self.send_response(200)
      # Send header
      self.send_header('Content-type','text/plain; version=0.0.4')
      self.end_headers()

      # Send temperature metrics
      self.wfile.write("# HELP temp_celsius Temperature in celsius.\n")
      self.wfile.write("# TYPE temp_celsius gauge\n")
      self.wfile.write("temp_celsius{location=\"living room\"} %f\n" % temp)

      # Send humidity metrics
      self.wfile.write("# HELP rel_humidity Relative Humidity.\n")
      self.wfile.write("# TYPE rel_humidity gauge\n")
      self.wfile.write("rel_humidity{location=\"living room\"} %f\n" % humidity) 

      return
    except IOError:
      self.send_error(500, 'internal error')
      #self.send_error(500, 'internal server error: %s' % (sys.exc_info()[0]))


def run():
  print('http server is starting...')

  server_address = ('0.0.0.0', 9000)
  httpd = HTTPServer(server_address, EnvHTTPRequestHandler)
  print('http server is running...')
  httpd.serve_forever()

if __name__ == '__main__':
  run()

