#!/usr/bin/env python3
import pymysql.cursors
import logging as log
import sys

def main():

    externalEnvTable = "bme280_sensor"

    try:
        conn_i = pymysql.connect(
                user = 'alex',
                passwd = '!Passw0rd',
                host = '192.168.11.48',
                db ='temp_db'
                )

        conn_o = pymysql.connect(
                user = 'alex',
                passwd = 'Passw0rd',
                host = '192.168.11.53',
                db ='temp_db'
                )

        sql = 'select * from {} order by probe_date desc;'.format(externalEnvTable)
        print(sql)

        with conn_i.cursor() as curs:
            curs.execute(sql)
            rows = curs.fetchall()
            print(len(rows))
            curs.close()


        with conn_o.cursor() as curs:
        # id, probe_date, temp, humi, bar
            for row in rows:
                sql = "insert into {} values ({},'{}',{},{},{});".format(externalEnvTable, row[0], row[1], row[2], row[3], row[4])
                print(sql)
                curs.execute(sql)
            conn_o.commit()
            curs.close()

    except pymysql.Error as e:
        print("pymysql %d: %s" %(e.args[0], e.args[1]))
        sys.exit(1)
    finally:
        if conn_i:
            conn_i.close()
            conn_i = None

        if conn_o:
            conn_o.close()
            conn_o = None
            
        print('Closed db')
      
if __name__ == '__main__':
    main()
