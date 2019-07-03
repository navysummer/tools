r=`rpm -qa | grep openssh | wc -l`
if [ $r -eq 0 ]
then
    yum install -y openssh-clients openssh-server
fi
echo 'please input username for hadoop:'
read user
us=`egrep "^$user:" /etc/passwd | wc -l`
if [ $us -eq 0 ]
then
    useradd -m $user -s /bin/bash 2>1 &&
    echo -e "\e[4;36m ------>$user create success\e[0m"
    echo 'please input hadoop password'
    read pd
    echo $pd | passwd $user --stdin  &>/dev/null
    if [ $? -eq 0 ]
    then
        echo -e "\e[4;36m ------>$user's password is $pd \e[0m"
    else
        echo -e "\e[4;36m ------>$user's password create fail \e[0m"
else
    echo -e "\e[4;36m ------>$user has existed \e[0m"
fi
usermod -g $user root 2>1 &&
echo -e "\e[4;36m ------>$user's group is root \e[0m"
jdk=`yum -y list java* | grep java | wc -l`
if [ $jdk -eq 0 ]
then
    echo -e "\e[4;36m ------>jdk source not exist Unable to install jdk\e[0m"
    exit
else
    yum -y install java-1.8.0-openjdk* 2>&1 &&
    jdkinfo=`java -version`
    echo -e "\e[4;36m jdk info \e[0m\n$jdkinfo"
fi
echo 'please input JAVA_HOME:'
read jh
java_env="JAVA_HOME=$jh\nJRE_HOME=\$JAVA_HOME/jre\nCLASSPATH=\$JAVA_HOME/lib/dt.jar:\$JAVA_HOME/lib/tools.jar\nPATH=\$JAVA_HOME/bin:\$PATH\nexport PATH JAVA_HOME JRE_HOME CLASSPATH"
echo $java_env >> /etc/profile
source /etc/profile
if [ -z $JAVA_HOME ]
then
    echo -e "\e[4;36m ------>JAVA_HOME set fail\e[0m"
else
    echo -e "\e[4;36m ------>JAVA_HOME set success\e[0m"
su $user
cd ~
curl -O http://mirrors.hust.edu.cn/apache/hadoop/common/hadoop-3.2.0/hadoop-3.2.0.tar.gz
file_path="~/hadoop-3.2.0.tar.gz"
sudo tar -zxf $file_path -C /usr/local
cd /usr/local/
sudo chown -R hadoop:hadoop ./hadoop-3.2.0 
hd_env="HADOOP_HOME=/usr/local/hadoop-3.2.0\nPATH=\$PATH:\$HADOOP_HOME/bin"
echo $hd_env >> /etc/profile
source /etc/profile
echo -e "\e[4;36m ------>HADOOP install success \nHADOOP_HOME=/usr/local/hadoop-3.2.0 \e[0m"
hadoop_info=`hadoop version`
echo "hadoop version:\n$hadoop_info"
echo 
