#!/usr/bin/bash

#----------------------------------------1.install nginx-------------------------------------------
yum -y install nginx 2>&1 &&
echo -e "\e[1;32m ------>yum install nginx success \e[0m"
service nginx start 2>&1 &&
if [ $? -eq 0 ];then
	echo -e "\e[1;32m ------>start nginx success \e[0m"
fi
#----------------------------------------2.install mysql-------------------------------------------
yum -y localinstall http://dev.mysql.com/get/mysql57-community-release-el7-7.noarch.rpm 2>&1 &&
echo -e "\e[1;32m ------>yum install mysql57 source success \e[0m"
yum -y install mysql-community-server 2>&1 &&
echo -e "\e[1;32m ------>yum install mysql57 success \e[0m"
service mysqld start 2>&1 &&
if [ $? -eq 0 ];then
	echo -e "\e[1;32m ------>start mysql success \e[0m"
fi
pwd=`grep 'temporary password' /var/log/mysqld.log | awk -F ":" '{print $NF}'`
str1="\e[1;32m mysql password:"
str2="\e[0m"
str3=$str1$pwd$str2
echo -e $str3
#----------------------------------------3.alter mysql password-------------------------------------------
#way 1
# newpwd=''
# mysql -uroot -p`echo $pwd` -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '$newpwd';
# 							   GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '$newpwd' WITH GRANT OPTION;
# 							   flush privileges;
# 							   exit"
#way 2
# mysqladmin -u root -p`echo $pwd` password $newpwd
# echo -e "\e[1;32m ------>alter mysql password success \e[0m"
#----------------------------------------4.install php-------------------------------------------
rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm 2>&1 &&
rpm -Uvh https://mirror.webtatic.com/yum/el7/webtatic-release.rpm 2>&1 &&
echo -e "\e[1;32m ------>install php source success \e[0m"
yum -y install php php-gd php-xml php-mbstring php-ldap php-pear php-xmlrpc php-devel php-mysql php-fpm php-common php-pdo 2>&1 &&
service php-fpm start 2>&1 &&
if [ $? -eq 0 ];then
	echo -e "\e[1;32m ------>start php-fpm success \e[0m"
fi
service nginx restart
if [ $? -eq 0 ];then
	echo -e "\e[1;32m ------>restart nginx success \e[0m"
fi

