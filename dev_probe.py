#!/usr/bin/env python3
import datetime
import psutil
import argparse
from dev_db import dev_db

def main():

    parser = argparse.ArgumentParser(description='Usage...')
    parser.add_argument('-d','--device', type=int, help='The ID of device')
    args = parser.parse_args()
    if args.device is None:
        parser.print_help(sys.stderr)
        exit(1)

    db = dev_db('alex','Passw0rd','192.168.11.48','device_db')
    db.debugOn()

    probe_date = datetime.datetime.now()

    # gives a single float value
    cpu_usage = psutil.cpu_percent(5)

    # you can have the percentage of used RAM
    mem_usage = psutil.virtual_memory().percent

    storage_usage = psutil.disk_usage('/').percent

    cpu_temp = psutil.sensors_temperatures()['cpu_thermal'][0].current

    db.addDevData(args.device, probe_date, cpu_temp, cpu_usage, mem_usage, storage_usage) 


if __name__ == '__main__':
    main()
