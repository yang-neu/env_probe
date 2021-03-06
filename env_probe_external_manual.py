#!/usr/bin/env python3
import time
import datetime
import pymysql.cursors
import logging as log
import sys
import argparse

from env_db import env_db
from bme280 import Bme280

def main():

    parser = argparse.ArgumentParser(description='Usage...')
    parser.add_argument('-s','--sensor', type=int, help='The ID of sensor')
    args = parser.parse_args()
    print (args.sensor)
    if args.sensor is None:
        parser.print_help(sys.stderr)
        exit(1)

    db = env_db()
    db.debugOn()

    # i2c_address=0x76, bus_number=1
    bme280 = Bme280(0x76, 1)

    try:
        while True:
            # Try to grab a sensor reading.  Use the read_retry method which will retry up
            # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
            print('Reading...')
            temperature, humidity, barometric = bme280.get_data()
            if humidity is not None and temperature is not None and barometric is not None:
                date = datetime.datetime.now()
                print("Last valid input: " + str(date))
                print("Temperature: %-3.1f C" % temperature)
                print("Humidity: %-3.1f %%" % humidity)
                print("Pressure: %-3.1f hPa"% barometric)
                db.addExternalEnvData(args.sensor, date, temperature, humidity, barometric)
            time.sleep(6)

    except KeyboardInterrupt:
        print("Cleanup")

      
if __name__ == '__main__':
    main()
