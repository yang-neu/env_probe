#!/usr/bin/env python3
import Adafruit_DHT
import time
import datetime
import pymysql.cursors
import logging as log
import sys

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.DHT11

# Using a Raspberry Pi 0 with DHT11 sensor
# connected to GPIO14.
pin = 14

class env_db():
    def __init__(self):
        try:
            self.internalEnvTable = "dth11_sensor"
            self.externalEnvTable = "bme280_sensor"

            # if not exist create table
            sql = "CREATE TABLE IF NOT EXISTS {} ('id' int(11) DEFAULT NULL, " 
                + "                               'probe_date' datetime DEFAULT NULL,"
                + "                               'temp' float(4,1) DEFAULT 0,"
                + "                               'hum' float(4,1) DEFAULT 0,"
                + "                               'bar' float(6,1) DEFAULT 0,"
                + " ); ".format(self.externalEnvTable)
            print (sql)

            self.conn_db()
            with self.conn.cursor() as curs
                curs.execute(sql)
                curs.commit()
                curs.close()
        except pymysql.Error as e:
            log.error("__init__; error pymysql %d: %s" %(e.args[0], e.args[1]))
            sys.exit(1)
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None
                log.info('__init__ closed db in init')


    def conn_db(self):
        self.conn = pymysql.connect(
                user='alex',
                passwd='!Passw0rd',
                host='192.168.11.48',
                db='temp_db'
                )
        return self.conn

    def getLatestInternalData(self):
        try:
            self.conn_db()
            sql = 'select * from {} limit 1;'.format(self.internalEnvTable)
            log.debug(sql)

            with self.conn.cursor() as curs
                curs.execute(sql)
                curs.commit()
                curs.close()
        except pymysql.Error as e:
            log.error("getLatestInternalData; error pymysql %d: %s" %(e.args[0], e.args[1]))
            sys.exit(1)
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None
                log.info('getLatestInternalData closed db in init')

    def addInternalEnvData(self, date, humidity, temperature):
        try:
            if self.curs is not None:
                sql = "insert into dht11_sensor values ({}, '{}', {}, {});".format(2, date.strftime('%Y-%m-%d %H:%M:%S'), temperature, humidity )
                print(sql)
        except pymysql.Error as e:
            print("could not add internal evn data; error pymysql %d: %s" %(e.args[0], e.args[1]))

    def __del__(self)
        try:
            if self.curs:
                self.curs.close()
            if self.conn:
                self.conn.close()
        except pymysql.Error as e:
            print("could not add internal evn data; error pymysql %d: %s" %(e.args[0], e.args[1]))


def main():

    db = env_db()
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

if __name__ == '__main__':
    main()
