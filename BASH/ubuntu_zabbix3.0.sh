#! /usr/bin/bash
apt-get install libcurl3 selinux-utils
apt-get install apache2 2>&1 &&
systemctl start apache2 2>&1 &&
echo -e "\e[4;36m ------>apache2 install and start success \e[0m"
apt-get install mysql-server mysql-client 2>&1 &&
systemctl start mysql 2>&1 &&
echo -e "\e[4;36m ------>mysql install and start success \e[0m"
echo -e "\e[4;36m ------>please set mysql root password \e[0m"
mysql_secure_installation
echo -e "\e[4;36m ------>set mysql root password success \e[0m"
apt-get install php php-mysql php-mbstring php-xml php-bcmath libapache2-mod-php php-gd 2>&1 &&
echo -e "\e[4;36m ------>php install success \e[0m"
systemctl restart apache2 2>&1 &&
echo -e "\e[4;36m ------>apache2 restart success \e[0m"
wget https://repo.zabbix.com/zabbix/3.0/debian/pool/main/z/zabbix-release/zabbix-release_3.0-2+stretch_all.deb 2>&1 &&
dpkg -i zabbix-release_3.0-2+stretch_all.deb 2>&1 &&
apt-get update 2>&1 &&
echo -e "\e[4;36m ------>add zabbix sourece success \e[0m"
apt-get -y install zabbix-server-mysql zabbix-frontend-php zabbix-agent 2>&1 &&
echo -e "\e[4;36m ------>install zabbix-server zabbix-frontend-php zabbix-agent success \e[0m"
mysql -uroot -p -e "set global validate_password_policy=0;
                    set global validate_password_length=1;
                    create database zabbix character set utf8 collate utf8_bin;
                    grant all privileges on zabbix.* to zabbix@localhost identified by 'zabbix';
		    quit" 2>&1 &&
zcat /usr/share/doc/zabbix-server-mysql*/create.sql.gz | mysql -uzabbix -p zabbix 2>&1 &&
echo -e "\e[4;36m ------>create mysql user zabbix success \e[0m"

sed -i "s#\# CacheSize=8M#CacheSize=1024M#g" /etc/zabbix/zabbix_server.conf
sed -i "s#\# DBHost=localhost#DBHost=localhost#g" /etc/zabbix/zabbix_server.conf
sed -i "s#\# DBPassword=#DBPassword=zabbix#g" /etc/zabbix/zabbix_server.conf

sed -i 's@# php_value date.timezone Europe/Riga@php_value date.timezone Asia/Shanghai@g' /etc/zabbix/apache.conf
sed -i 's@        php_value memory_limit 128M@        php_value memory_limit 1024M@g' /etc/zabbix/apache.conf
sed -i 's@        php_value upload_max_filesize 2M@        php_value upload_max_filesize 5M@g' /etc/zabbix/apache.conf
chkzsenable=`systemctl list-unit-files | grep zabbix-server | wc -l`
chkzaenable=`systemctl list-unit-files | grep zabbix-agent | wc -l`
chkapenable=`systemctl list-unit-files | grep apche2 | wc -l`
if [ $chkzsenable -eq 0 ]
then
	systemctl enable zabbix-server
fi
if [ $chkzaenable -eq 0 ]
then
	systemctl enable zabbix-agent
fi
if [ $chkapenable -eq 0 ]
then
	systemctl enable apache2
fi
systemctl restart zabbix-server zabbix-agent apache2
