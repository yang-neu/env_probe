#!/usr/bin/env python3
import Adafruit_DHT
import time
import datetime
import pymysql.cursors

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.DHT11

# Using a Raspberry Pi 0 with DHT11 sensor
# connected to GPIO14.
pin = 14

conn = pymysql.connect(
        user='alex',
        passwd='!Passw0rd',
        host='192.168.11.48',
        db='temp_db'
    )
c = conn.cursor()

sql = 'select * from dht11_sensor limit 1;'
c.execute(sql)
print('* Show table dht11_sensor\n')
for row in c.fetchall():
    print('No:', row[0], 'Content:', row[1])

try:
    while True:
        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
        print('Reading...')
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        if humidity is not None and temperature is not None:
            date = datetime.datetime.now()
            print("Last valid input: " + str(date))
            print("Temperature: %-3.1f C" % temperature)
            print("Humidity: %-3.1f %%" % humidity)
            sql = "insert into dht11_sensor values ({}, '{}', {}, {});".format(2, date.strftime('%Y-%m-%d %H:%M:%S'), temperature, humidity )
            print(sql)
            c.execute(sql)
            conn.commit()
        time.sleep(6)

except KeyboardInterrupt:
    print("Cleanup")
    conn.close()
