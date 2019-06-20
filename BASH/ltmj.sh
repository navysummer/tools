#!/usr/bin/bash

#----------------------------------------1.install tomcat-------------------------------------------
yum -y install tomcat 2>&1 &&
echo -e "\e[1;32m ------>yum install tomcat success \e[0m"
service tomcat start 2>&1 &&
if [ $? -eq 0 ];then
	echo -e "\e[1;32m ------>start tomcat success \e[0m"
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
#----------------------------------------4.install jdk-------------------------------------------
jdk=`yum -y list java* | grep java | wc -l`
if [ $jdk -eq 0 ]; then
	echo -e "\e[1;32m ------>jdk source not exist Unable to install \e[0m"
else
	yum -y install java-1.8.0-openjdk* 2>&1 &&
	jdkinfo=`java -version`
	echo -e "\e[1;32m jdk info \e[0m\n$jdkinfo"
fi

