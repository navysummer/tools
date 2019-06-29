#!/bin/bash
getSysInfo(){
	Static_hostname=`hostnamectl status | grep "Static hostname" | awk '{for(i=3;i<=NF;i++) print $i}'`
	Chassis=`hostnamectl status | grep Chassis | awk '{for(i=2;i<=NF;i++) print $i}'`
	MachineID=`hostnamectl status | grep "Machine ID" | awk '{for(i=3;i<=NF;i++) print $i}'`
	BootID=`hostnamectl status | grep "Boot ID" | awk '{for(i=3;i<=NF;i++) print $i}'`
	Virtualization=`hostnamectl status | grep "Virtualization" | awk '{for(i=2;i<=NF;i++) print $i}'`
	OSType=`hostnamectl status | grep "Operating System" | awk '{print $3}'`
	OSVersion=`hostnamectl status | grep "Operating System" | awk '{for(i=4;i<=NF;i++){var=var$i}; print var}'`
	Kernel=`hostnamectl status | grep "Kernel" | awk '{for(i=2;i<=NF;i++){var=var$i}; print var}'`
	Architecture=`hostnamectl status | grep "Architecture" | awk '{for(i=2;i<=NF;i++){var=var$i}; print var}'`
	sysInfo="{\"Static_hostname\":\"$Static_hostname\",\"Chassis\":\"$Chassis\",\"MachineID\":\"$MachineID\",\"BootID\":\"$BootID\",\"Virtualization\":\"$Virtualization\",\"OSType\":\"$OSType\",\"OSVersion\":\"$OSVersion\",\"Kernel\":\"$Kernel\",\"Architecture\":\"$Architecture\"}"
}
getSysInfo
echo $sysInfo
