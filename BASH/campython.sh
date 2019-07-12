#!/usr/bin/bash
#----------------------------------------1.install nginx-------------------------------------------
yum -y install httpd 2>&1 &&
echo -e "\e[1;32m ------>yum install httpd success \e[0m"
service httpd start 2>&1 &&
if [ $? -eq 0 ];then
	echo -e "\e[1;32m ------>start httpd success \e[0m"
	echo -e "httpd version:\n`httpd -v`"
fi
#----------------------------------------2.install mysql-------------------------------------------
mysql_source=`ls /etc/yum.repos.d | grep mysql | wc -l`
if [ $mysql_source -eq 0 ];then
	yum -y localinstall http://dev.mysql.com/get/mysql57-community-release-el7-7.noarch.rpm
fi
echo -e "\e[1;32m ------>yum install mysql source success \e[0m"
yum -y install mysql-community-server 2>&1 &&
echo -e "\e[1;32m ------>yum install mysql success \e[0m"
echo -e "mysql version:\n`mysql --version`"
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
#----------------------------------------4.install django and flask-------------------------------------------
check_curl=`command -v curl | wc -l`
if [ $check_curl -eq 0 ];then
	yum -y install curl
fi
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py 2>&1 &&
check_python=`command -v python | wc -l`
if [ $check_python -eq 0 ];then
	yum -y install python
fi
echo -e "python version:`python -V`"
python get-pip.py 2>&1 &&
echo -e "\e[1;32m ------>install pip success \e[0m"
rm -rf get-pip.py
version=`python -V 2>&1|awk '{print $2}'|awk -F '.' '{print $1}'`
if [ $version -eq 2 ];then
	python -m pip install "django<2" 2>&1 &&
	echo -e "\e[1;32m ------>install django success \e[0m"
	echo -e "django version:`python -m django --version`"
elif [ $version -eq 3 ];then
	pip install django 2>&1 &&
	echo -e "\e[1;32m ------>install django success \e[0m"
	echo -e "django version:`python -m django --version`"
else
	echo -e "\e[1;32m ------>install django fail \e[0m"
fi
pip install flask 2>&1 &&
echo -e "\e[1;32m ------>install flask success \e[0m"
echo -e "flask version:`flask --version | grep -i flask`"
