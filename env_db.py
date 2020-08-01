#!/usr/bin/env python3
import time
import datetime
import pymysql.cursors
import logging 
import sys


class env_db():
    def __init__(self):
        try:
            self.internalEnvTable = "dht11_sensor"
            self.externalEnvTable = "bme280_sensor"

            self.logLevel = logging.INFO
            console = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter('%(asctime)s [%(module)-12s %(funcName)-12s] %(levelname)-8s %(message)s')
            console.setFormatter(formatter)
            self.log = logging.getLogger(self.__module__)
            self.log.addHandler(console)
            self.log.setLevel(self.logLevel)

            # if not exist create table
            sql_ex = ("CREATE TABLE IF NOT EXISTS {} (id int(11) DEFAULT NULL, " 
                     "probe_date datetime DEFAULT NULL,"
                     "temp float(4,1) DEFAULT 0,"
                     "hum float(4,1) DEFAULT 0,"
                     "bar float(6,1) DEFAULT 0"
                     ");").format(self.externalEnvTable)
            self.log.debug(sql_ex)

            sql_in = ("CREATE TABLE IF NOT EXISTS {} (id int(11) DEFAULT NULL, " 
                     "probe_date datetime DEFAULT NULL,"
                     "temp float(4,1) DEFAULT 0,"
                     "hum float(4,1) DEFAULT 0"
                     ");").format(self.internalEnvTable)
            self.log.debug(sql_in)

            conn = self._conn_db()
            with self.conn.cursor() as curs:
                curs.execute(sql_in)
                curs.execute(sql_ex)
                curs.close()
            conn.commit()
        except pymysql.Error as e:
            self.log.error("pymysql %d: %s" %(e.args[0], e.args[1]))
            sys.exit(1)
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None
                self.log.debug('Closed db')

    def __del__(self):
        try:
            if self.conn:
                self.conn.close()
        except pymysql.Error as e:
            self.log.debug("could not add internal evn data; error pymysql %d: %s" %(e.args[0], e.args[1]))


    def _conn_db(self):
        self.conn = pymysql.connect(
                user='alex',
                passwd='!Passw0rd',
                host='192.168.11.48',
                db='temp_db'
                )
        self.log.debug('Open db')
        return self.conn

    def debugOn(self):
        self.logLevel = logging.DEBUG
        self.log.setLevel(self.logLevel)

    def getLatestInternalData(self):
        try:
            self._conn_db()
            sql = 'select * from {} order by probe_date desc limit 1;'.format(self.internalEnvTable)
            self.log.debug(sql)

            with self.conn.cursor() as curs:
                curs.execute(sql)
                row = curs.fetchone()
                curs.close()
                # id, probe_date, temp, humi
                return row[0],row[1],row[2],row[3]
        except pymysql.Error as e:
            self.log.error("pymysql %d: %s" %(e.args[0], e.args[1]))
            sys.exit(1)
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None
                self.log.debug('closed db')

    def addInternalEnvData(self, sensor_id, date, humidity, temperature):
        try:
            self._conn_db()
            sql = "insert into dht11_sensor values ({}, '{}', {}, {});".format(sensor_id, date.strftime('%Y-%m-%d %H:%M:%S'), temperature, humidity )
            self.log.debug(sql)

            with self.conn.cursor() as curs:
                curs.execute(sql)
            self.conn.commit()
        except pymysql.Error as e:
            self.log.error("pymysql %d: %s" %(e.args[0], e.args[1]))
            sys.exit(1)
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None
                self.log.debug('closed db')


def main():

    # unit test
    db = env_db()
    db.debugOn()

    sensor_id = 999
    temperature = 20.0
    humidity = 50
    date = datetime.datetime.now()
    db.addInternalEnvData(sensor_id, date, temperature, humidity)
    sensor_id,probe_date,temp,humi = db.getLatestInternalData()
    print('No:', sensor_id, probe_date, temp, humi)


if __name__ == '__main__':
    main()
