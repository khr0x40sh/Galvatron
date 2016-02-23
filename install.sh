#!/bin/sh
#generic "install script". Adjust as needed.

mkdir /var/www/upload
chmod 777 /var/www/upload
cp access.php /var/www
cp access1.php /var/www
cp search.php /var/www
cp -r servers/web/bot /var/www

cp -r client/ /var/www

mysql -u root < bot1.sql

echo "Client files can be found in /var/www/client/"
echo "The DNS / ICMP Servers are in the servers directory"