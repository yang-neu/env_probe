#!/usr/bin/env python3
import time
import datetime
import pymysql.cursors
import logging 
import sys


class env_db():
    def __init__(self,user='alex',passwd='!Passw0rd',host='192.168.11.48',db='temp_db'):
        try:
            self._user=user
            self._passwd=passwd
            self._host=host
            self._db=db
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
        self.log.debug('{} {} {} {}'.format(self._user,self._passwd,self._host,self._db))
        self.conn = pymysql.connect(
                user=self._user,
                passwd=self._passwd,
                host=self._host,
                db=self._db
                )
        self.log.debug('Open db')
        return self.conn

    def debugOn(self):
        self.logLevel = logging.DEBUG
        self.log.setLevel(self.logLevel)

    def createSensorInforTable(self):
        try:
            self._conn_db()
            sql = 'CREATE TABLE IF NOT EXISTS sensor_info (id int(11), type varchar(255), location varchar(255));'
            self.log.debug(sql)

            with self.conn.cursor() as curs:
                curs.execute(sql)
            self.conn.commit()

            sql = 'select count(*) from sensor_info;'
            self.log.debug(sql)

            with self.conn.cursor() as curs:
                curs.execute(sql)
                (number_of_rows,)=curs.fetchone()
                if number_of_rows > 0:
                    return

            sql_array = ["INSERT INTO sensor_info values (1, 'DHT11', 'Main bedroom');",
                         "INSERT INTO sensor_info values (2, 'DHT11', 'Niuniu bedroom');",
                         "INSERT INTO sensor_info values (3, 'DHT11', 'Doudou bedroom');",
                         "INSERT INTO sensor_info values (4, 'DHT11', 'Toilet');",
                         "INSERT INTO sensor_info values (5, 'DHT11', 'Storage room');",
                         "INSERT INTO sensor_info values (6, 'DHT11', 'Living room');",
                         "INSERT INTO sensor_info values (7, 'DHT11', 'Shore cabinet');",
                         "INSERT INTO sensor_info values (10, 'BME280', 'South balcony');",
                        ]
            self.log.debug(sql)
            with self.conn.cursor() as curs:
                for sql in sql_array:
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

    def getLatestExternalData(self):
        try:
            self._conn_db()
            sql = 'select * from {} order by probe_date desc limit 1;'.format(self.externalEnvTable)
            self.log.debug(sql)

            with self.conn.cursor() as curs:
                curs.execute(sql)
                row = curs.fetchone()
                curs.close()
                # id, probe_date, temp, humi, bar
                return row[0],row[1],row[2],row[3],row[4]
        except pymysql.Error as e:
            self.log.error("pymysql %d: %s" %(e.args[0], e.args[1]))
            sys.exit(1)
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None
                self.log.debug('closed db')

    def addInternalEnvData(self, sensor_id, date, temperature, humidity):
        try:
            self._conn_db()
            sql = "insert into {} values ({}, '{}', {}, {});".format(self.internalEnvTable, sensor_id, date.strftime('%Y-%m-%d %H:%M:%S'), temperature, humidity )
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

    def addExternalEnvData(self, sensor_id, date, temperature, humidity, barometric):
        try:
            self._conn_db()
            sql = "insert into {} values ({}, '{}', {}, {}, {});".format(self.externalEnvTable, sensor_id, date.strftime('%Y-%m-%d %H:%M:%S'), temperature, humidity, barometric )
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
    # db = env_db()
    db = env_db('alex','Passw0rd','192.168.11.53','temp_db')
    db.debugOn()

    sensor_id = 999
    temperature = 20.0
    humidity = 50.1
    bar = 1003.5
    date = datetime.datetime.now()
    db.addInternalEnvData(sensor_id, date, temperature, humidity)
    sensor_id,probe_date,temp,humi = db.getLatestInternalData()
    print('No:', sensor_id, probe_date, temp, humi)

    db.addExternalEnvData(998, date, temperature, humidity, bar)
    sensor_id,probe_date,temp,humi,bar = db.getLatestExternalData()
    print('No:', sensor_id, probe_date, temp, humi, bar)

    db.createSensorInforTable()


if __name__ == '__main__':
    main()
