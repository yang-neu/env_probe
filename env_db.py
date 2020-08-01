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

            self.logLevel = logging.DEBUG
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
            self.log.error("__init__; error pymysql %d: %s" %(e.args[0], e.args[1]))
            sys.exit(1)
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None
                self.log.info('__init__ closed db')

    def __del__(self):
        try:
            if self.conn:
                self.conn.close()
        except pymysql.Error as e:
            print("could not add internal evn data; error pymysql %d: %s" %(e.args[0], e.args[1]))


    def _conn_db(self):
        self.conn = pymysql.connect(
                user='alex',
                passwd='!Passw0rd',
                host='192.168.11.48',
                db='temp_db'
                )
        return self.conn

    def getLatestInternalData(self):
        try:
            self._conn_db()
            sql = 'select * from {} limit 1;'.format(self.internalEnvTable)
            self.log.debug(sql)

            with self.conn.cursor() as curs:
                curs.execute(sql)
                row = curs.fetchone()
                curs.close()
                # id, probe_date, temp, humi
                return row[0],row[1],row[2],row[3]
        except pymysql.Error as e:
            self.log.error("getLatestInternalData; error pymysql %d: %s" %(e.args[0], e.args[1]))
            sys.exit(1)
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None
                self.log.info('getLatestInternalData closed db in init')

    def addInternalEnvData(self, sensor_id, date, humidity, temperature):
        try:
            if self.curs is not None:
                sql = "insert into dht11_sensor values ({}, '{}', {}, {});".format(sensor_id, date.strftime('%Y-%m-%d %H:%M:%S'), temperature, humidity )
                print(sql)
        except pymysql.Error as e:
            print("could not add internal evn data; error pymysql %d: %s" %(e.args[0], e.args[1]))


def main():

    # unit test
    db = env_db()

    #logger.debug(db.__class__.__name__)
    sensor_id,probe_date,temp,humi = db.getLatestInternalData()
    print('No:', sensor_id, probe_date, temp, humi)


if __name__ == '__main__':
    main()
