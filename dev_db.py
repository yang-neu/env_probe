#!/usr/bin/env python3
import time
import datetime
import pymysql.cursors
import logging
import sys


class dev_db():
    def __init__(self,user='alex',passwd='Passw0rd',host='192.168.11.48',db='device_db'):
        try:
            self._user=user
            self._passwd=passwd
            self._host=host
            self._db=db
            self.devTable= "device_status"

            self.logLevel = logging.INFO
            console = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter('%(asctime)s [%(module)-12s %(funcName)-12s] %(levelname)-8s %(message)s')
            console.setFormatter(formatter)
            self.log = logging.getLogger(self.__module__)
            self.log.addHandler(console)
            self.log.setLevel(self.logLevel)

            # if not exist create table
            sql = ("CREATE TABLE IF NOT EXISTS {} (id int(11) DEFAULT NULL, " 
                     "probe_date datetime DEFAULT NULL,"
                     "cpu_temp float(4,1) DEFAULT 0,"
                     "cpu_usage int(4),"
                     "mem_usage int(4),"
                     "storage_usage int(4)"
                     ");").format(self.devTable)
            self.log.debug(sql)

            conn = self._conn_db()
            with self.conn.cursor() as curs:
                curs.execute(sql)
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
            self.log.error("Error pymysql %d: %s" %(e.args[0], e.args[1]))


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

    def getLatestDevData(self):
        try:
            self._conn_db()
            sql = 'select * from {} order by probe_date desc limit 1;'.format(self.devTable)
            self.log.debug(sql)

            with self.conn.cursor() as curs:
                curs.execute(sql)
                row = curs.fetchone()
                curs.close()
                # dev_id, probe_date, cpu_temp, cpu_usage, mem_usage, storeage_usage
                return row[0],row[1],row[2],row[3],row[4],row[5]
        except pymysql.Error as e:
            self.log.error("pymysql %d: %s" %(e.args[0], e.args[1]))
            sys.exit(1)
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None
                self.log.debug('closed db')

    def addDevData(self, dev_id, probe_date, cpu_temp, cpu_usage, mem_usage, storeage_usage):
        try:
            self._conn_db()
            sql = "insert into {} values ({}, '{}', {}, {}, {}, {});".format(self.devTable, dev_id, probe_date.strftime('%Y-%m-%d %H:%M:%S'), cpu_temp, cpu_usage, mem_usage, storeage_usage)
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
    db = dev_db('alex','Passw0rd','192.168.11.48','device_db')
    db.debugOn()

    dev_id = 999
    cpu_temp = 44.0
    probe_date = datetime.datetime.now()
    cpu_usage = 30
    mem_usage = 55
    storeage_usage = 16
    db.addDevData(dev_id, probe_date, cpu_temp, cpu_usage, mem_usage, storeage_usage)
    dev_id, probe_date, cpu_temp, cpu_usage, mem_usage, storeage_usage = db.getLatestDevData()
    print('Get:', dev_id, probe_date, cpu_temp, cpu_usage, mem_usage, storeage_usage)


if __name__ == '__main__':
    main()
