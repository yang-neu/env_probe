#!/usr/bin/env python3

from bme280 import Bme280

def main():
  bme280 = Bme280(0x76, 1)
  temp, humid, press = bme280.get_data()
  print("Temp:", temp, "C")
  print("Humid:", humid, "%")
  print("Pressure:", press, "[%]")
      
if __name__ == '__main__':
    main()
