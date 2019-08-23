#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import time

def main():
    file = open(r"uuid")
    uuid_newHost = []
    for line in file:
        line = line.split()
        uuid_real = line[0].lower()
        uuid_newHost.append(uuid_real)
        print(uuid_real)
    file.close()
    print(uuid_newHost)
    print(len(uuid_newHost))
    print(len(set(uuid_newHost)))


if __name__ == "__main__":
    main();
