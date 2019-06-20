#!/usr/bin/python
# -*- coding: utf-8 -*-
import commands
import socket
import fcntl
import struct

CMD_VIR_NETCARD = "ls /sys/devices/virtual/net/"
CMD_ALL_NETCARD = "cat /proc/net/dev | awk '{i++; if(i>2){print $1}}' | sed 's/^[\t]*//g' | sed 's/[:]*$//g'"

def get_ip_address(netcard_name):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,
        struct.pack('256s', netcard_name[:15])
    )[20:24])

def get_netcard(CMD):
    return_code, output = commands.getstatusoutput(CMD)
    vnic_list = output.split('\n')
    return set(vnic_list)

def main():
    vir_netcard_name = get_netcard(CMD_VIR_NETCARD)
    all_netcard_name = get_netcard(CMD_ALL_NETCARD)
    rel_netcard = [{item:get_ip_address(item)} for item in all_netcard_name if item not in vir_netcard_name]
    vir_netcard = [{item:get_ip_address(item)} for item in all_netcard_name if item  in vir_netcard_name]
    print(rel_netcard)
    print(vir_netcard)

if __name__ == '__main__':
    main()
