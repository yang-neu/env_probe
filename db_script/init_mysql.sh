DB_ROOT_PASS="\!Passw0rd" 
DB_NAME="temp_db" 
DB_USER="alex" \
DB_PASS="\!Passw0rd"

mysqladmin -u root password "${DB_ROOT_PASS}"
echo "CREATE DATABASE IF NOT EXISTS ${DB_NAME} DEFAULT CHARACTER SET utf8;"  >> /tmp/sql
echo "grant all privileges on ${DB_NAME}.* to ${DB_USER}@'%' identified by '${DB_PASS}' with grant option ;" >> /tmp/sql
echo "DELETE FROM mysql.user WHERE User='';" >> /tmp/sql
echo "DROP DATABASE test;" >> /tmp/sql
echo "FLUSH PRIVILEGES;" >> /tmp/sql
cat /tmp/sql | mysql -u root --password="${DB_ROOT_PASS}"
