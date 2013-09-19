import time
import smbus
from Adafruit_I2C import Adafruit_I2C

# ===========================================================================
# TMP102 Class
# ===========================================================================

class TMP102:
  #i2c = None


  # Constructor
  def __init__(self, address=0x48, debug=False):
    #self.i2c = Adafruit_I2C(address)
    #self.address = address
    self.debug = debug
    # Make sure the specified mode is in the appropriate range

  def readTemperature(self):
    bus = smbus.SMBus(1)
    data = bus.read_i2c_block_data(0x49, 0)
    msb = data[0]
    lsb = data[1]
    return (((msb << 8) | lsb) >> 4) * 0.0625

