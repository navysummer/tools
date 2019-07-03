#!/bin/bash

YumLog=/var/log/update.log
lamplog=/var/log/lamp.log
#yum update
# yum -y update 1>>$YumLog 2>&1 &&
# echo -e "\e[4;36m ------>1.yum update success \e[0m"

#install lamp
yum install -y httpd mariadb-server mariadb php php-mysql php-gd libjpeg* php-ldap php-odbc php-pear php-xml php-xmlrpc php-mhash 1>>$lamplog 2>&1 &&
echo -e "\e[4;36m ------>2.LAMP install success \e[0m"

#httpd.conf

sed -i "/date.timezone =/a\date.timezone = PRC" /etc/php.ini

systemctl start httpd
systemctl enable httpd
systemctl start mariadb
systemctl enable mariadb

mysql -uroot -padmin -e "create database zabbix character set utf8 collate utf8_bin; 
						GRANT all ON zabbix.* TO 'zabbix'@'%' IDENTIFIED BY 'zabbix';
						flush privileges;
						exit" &&
echo -e "\e[4;36m ------>3.mariadb set OK \e[0m"

yum -y install net-snmp net-snmp-devel curl curl-devel libxml2 libxml2-devel libevent-devel.x86_64 javacc.noarch  javacc-javadoc.noarch javacc-maven-plugin.noarch javacc*

yum install php-bcmath php-mbstring -y

rpm -ivh http://repo.zabbix.com/zabbix/4.0/rhel/7/x86_64/zabbix-release-4.0-1.el7.noarch.rpm

yum install zabbix-server-mysql zabbix-web-mysql -y

zcat /usr/share/doc/zabbix-server-mysql-4.0.7/create.sql.gz | mysql -uroot -padmin zabbix

sed -i "s#\# CacheSize=8M#CacheSize=1024M#g" /etc/zabbix/zabbix_server.conf
sed -i "s#\# DBHost=localhost#DBHost=localhost#g" /etc/zabbix/zabbix_server.conf
sed -i "s#\# DBPassword=#DBPassword=zabbix#g" /etc/zabbix/zabbix_server.conf

sed -i 's@# php_value date.timezone Europe/Riga@php_value date.timezone Asia/Shanghai@g' /etc/httpd/conf.d/zabbix.conf
sed -i 's@        php_value memory_limit 128M@        php_value memory_limit 1024M@g' /etc/httpd/conf.d/zabbix.conf
sed -i 's@        php_value upload_max_filesize 2M@        php_value upload_max_filesize 5M@g' /etc/httpd/conf.d/zabbix.conf

systemctl enable zabbix-server
systemctl start zabbix-server

systemctl restart httpd