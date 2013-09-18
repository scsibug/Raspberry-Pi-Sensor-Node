import smbus
import time
b = smbus.SMBus(1)
d = []
addr = 0x27
b.write_quick(addr)
time.sleep(0.05)
d = b.read_i2c_block_data(addr, 0,4)
status = (d[0] & 0xc0) >> 6
humidity = (((d[0] & 0x3f) << 8) + d[1])*100/16383
tempC = ((d[2] << 6) + ((d[3] & 0xfc) >> 2))*165/16383 - 40
tempF = tempC*9/5 + 32
print "Data:       ", "%02x "*len(d)%tuple(d)
print "Status:     ", status
print "Humidity:   ", humidity, "%"
print "Temperature:", tempF, "F"
