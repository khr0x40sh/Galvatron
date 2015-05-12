#!/bin/sh

mkdir /var/www/upload
cp access.php /var/www
cp access1.php /var/www
cp login.php /var/www
cp -r bot/ /var/www

cp -r client/ /var/www

mysql -u root < bot1.sql

echo "Client files can be found in /var/www/client/"
