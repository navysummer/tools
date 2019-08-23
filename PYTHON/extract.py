# -*- coding: utf-8 -*-

def extract(filename):
    fopen = open(filename,'r',encoding='utf-8')
    lines = fopen.readlines()
    ip = []
    uuid = []
    for line in lines:
        index = lines.index(line)
        data = line.strip()
        if index % 2 == 0:
            ip.append(data)
        else:
            uuid.append(data)
    fopen.close()
    print('-------------Total lines is %s----------------'%(len(lines)))
    print('-------------IP number is %s----------------'%(len(ip)))
    print(ip)
    print('-------------uuid number is %s----------------'%(len(uuid)))
    print(uuid)
    

def main():
    filename = '上海x批'
    extract(filename)

if __name__ =='__main__':
    main()
