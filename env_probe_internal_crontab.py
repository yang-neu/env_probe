#!/usr/bin/env python3
import Adafruit_DHT
import time
import datetime
import pymysql.cursors
import logging as log
import sys
import argparse

from env_db import env_db

# run this script from the crontab every minute
# m h d M W
# * * * * * ~/env_probe/env_probe_internal_crontab.py -s <sensor_id> >> /tmp/env_probe_internal.log

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.DHT11

# Using a Raspberry Pi 0 with DHT11 sensor
# connected to GPIO14.
pin = 14


def main():

    parser = argparse.ArgumentParser(description='Usage...')
    parser.add_argument('-s','--sensor', type=int, help='The ID of sensor')
    args = parser.parse_args()
    if args.sensor is None:
        parser.print_help(sys.stderr)
        exit(1)

    db = env_db('alex','Passw0rd','192.168.11.53','temp_db')
    db.debugOn()

    # Try to grab a sensor reading.  Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    print('Reading...')
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        date = datetime.datetime.now()
        print("Last valid input: " + str(date))
        print("Temperature: %-3.1f C" % temperature)
        print("Humidity: %-3.1f %%" % humidity)
        #sql = "insert into dht11_sensor values ({}, '{}', {}, {});".format(2, date.strftime('%Y-%m-%d %H:%M:%S'), temperature, humidity )
        db.addInternalEnvData(args.sensor, date, temperature, humidity)


if __name__ == '__main__':
    main()
