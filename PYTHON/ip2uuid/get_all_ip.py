#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

def get_IP():
    command = "ip a"
    ret = os.popen(command)

    allIP = []
    loIP = ["127.0.0.1", "::1"]
    for line in ret.readlines():
        line = line.strip("\n").strip(" ")
        if line.startswith("inet"):
            ip = line.split(" ")[1].split("/")[0]
            if ip not in loIP:
                allIP.append(line.split(" ")[1].split("/")[0])

    return allIP

if __name__ == '__main__':
    print(get_IP())

