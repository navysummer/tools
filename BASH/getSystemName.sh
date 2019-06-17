#!/bin/bash
sysInfo=`cat /etc/issue`
getSysName(){
        if [ $(echo $sysInfo | grep -i ubuntu | wc -l) = "1" ]
        then
                SysName="ubuntu"
        elif [ $(echo $sysInfo | grep -i kernel | wc -l) = "1" ]
        then
            if [ $(cat /etc/redhat-release | grep -i centos | wc -l) = "1" ]
            then
                SysName="centos"
            elif [ $(cat /etc/redhat-release | grep -i "Red Hat" | wc -l) = "1" ]
            then
                SysName="redhat"
            fi
        elif [  $(echo $sysInfo | grep -i kali | wc -l) = "1" ]
        then
        	SysName="kali"
        fi
}
getSysName
echo $SysName
