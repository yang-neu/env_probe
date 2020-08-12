CREATE DATABASE IF NOT EXISTS device_db DEFAULT CHARACTER SET utf8;
grant all privileges on device_db.* to alex@'%' identified by 'Passw0rd' with grant option ;
FLUSH PRIVILEGES;
create table if not exists device_info (id int(11), type varchar(255), location varchar(255), remark varchar(255));
create table if not exists device_status (id int(11), probe_date datetime DEFAULT NULL, cpu_temp  float(4,1) DEFAULT 0, cpu_usage int(4) DEFAULT 0, mem_usage int(4) DEFAULT 0, storage_usage int(4) DEFAULT 0);
