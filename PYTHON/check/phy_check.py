#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from pyzabbix import ZabbixAPI, ZabbixAPIException

URL = 'http://127.0.0.1/zabbix'
USERNAME = 'Admin'
PASSWORD = 'O2rIBG5AQyh2U28Q'

class Zabbix(object):
    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password
        self.client = ZabbixAPI(url=url, user=user, password=password)
        
    def get_hosts(self,uuids):
        if uuids:
            params = {
                'output':['hostid','host'],
                'filter':{
                    'host':uuids,
                }
            }
        else:
            params = {
                'output':['hostid','host']
            }
        try:
            hosts = self.client.host.get(**params)
            if hosts:
                return hosts
            else:
                return None
        except Exception,e:
            return None
            
    def get_items(self,hostids):
        params = {
            'output':['hostid','name','lastclock','lastvalue','state'],
            'hostids':hostids
        }
        try:
            items = self.client.item.get(**params)
            if items:
                return items
            else:
                return None
        except Exception,e:
            return None

           
def handle(uuids):
    FoundHost = []
    NotFoundHost = []
    zabbix = Zabbix(URL, USERNAME, PASSWORD)
    hosts = zabbix.get_hosts(uuids)
    all_uuids = [i['host'] for i in hosts]
    for uuid in uuids:
        if uuid not in all_uuids:
            NotFoundHost.append(uuid)
        else:
            for i in hosts:
                if uuid == i['host']:
                    FoundHost.append(i)
    print('----------------------------------NotFoundHost:%s-------------------------------------'%(len(NotFoundHost)))
    print(NotFoundHost)
    FoundHostids = [ host['hostid'] for host in FoundHost]
    hostsitems = zabbix.get_items(FoundHostids)
    time_now = float(time.time())
    # 检测host
    hosts_all_items = [{'hostid':i['hostid'],'items':[item['name'] for item in hostsitems if i['hostid'] == item['hostid'] ]}for i in hosts]
    hosts_items_len = {i['hostid']:len(i['items']) for i in hosts_all_items }
    hosts_error_items = [{'hostid':i['hostid'],'items':[item['name'] for item in hostsitems if time_now - float(item['lastclock']) > 300 and i['hostid'] == item['hostid'] ]}for i in hosts]
    hosts_error = [host['host'] for i in hosts_error_items if len(i['items']) == hosts_items_len[i['hostid']] for host in hosts if host['hostid']==i['hostid']]
    hosts_warn_items = [{'hostid':i['hostid'],'items':[item['name'] for item in hostsitems if time_now - float(item['lastclock']) < 300 and i['hostid'] == item['hostid'] and item['state'] == '1' ]}for i in hosts]
    hosts_warn = [{'uuid':host['host'],'items':i['items']} for i in hosts_error_items if len(i['items']) for host in hosts if host['hostid']==i['hostid']]
    hosts_warn_uuid = [i['uuid'] for i in hosts_warn ]
    print('----------------------------------hosts_error:%s-------------------------------------'%(len(hosts_error)))
    print(hosts_error)
    print('----------------------------------hosts_warn_uuid:%s-------------------------------------'%(len(hosts_warn_uuid)))
    print(hosts_warn_uuid)
    #print('----------------------------------hosts_warn:%s-------------------------------------'%(len(hosts_warn)))
    #print(hosts_warn)
    # 检测磁盘
    diskitems = [{'hostid':item['hostid'],'name':item['name'],'lastclock':item['lastclock'],'lastvalue':item['lastvalue'],'state':item['state']} for item in hostsitems if item['name'] == 'disk.processregister']
    disks = [{'hostid':i['hostid'],'disk':eval(i['lastvalue'])} for i in diskitems if i['lastvalue']]
    disk_uuid_error = [{'hostid':i['hostid'],'disk':eval(i['lastvalue'])} for i in diskitems if not i['lastvalue']]
    print('----------------------------------hosts_not_support_disk.processregister:%s-------------------------------------'%(len(disk_uuid_error)))
    print(disk_uuid_error)
    all_disk_uuids = [diskuuid for disk in disks for item in disk if item == 'disk' for diskuuid in disk[item] ]
    disksinfo = zabbix.get_hosts(all_disk_uuids)
    FoundDisk = [disk for disk in disksinfo if disk['host'] in all_disk_uuids]
    NotFoundDisk = [disk for disk in disksinfo if disk['host'] not in all_disk_uuids]
    FoundDiskids = [ disk['hostid'] for disk in FoundDisk]
    NotFoundDiskuuids = [ disk['host'] for disk in NotFoundDisk]
    disks_items = zabbix.get_items(FoundDiskids)
    time_now = float(time.time())
    disks_all_items = [{'hostid':i['hostid'],'items':[item['name'] for item in disks_items if i['hostid'] == item['hostid'] ]}for i in disksinfo]
    disks_items_len = {i['hostid']:len(i['items']) for i in disks_all_items }
    disks_error_items = [{'hostid':i['hostid'],'items':[item['name'] for item in disks_items if time_now - float(item['lastclock']) > 300 and i['hostid'] == item['hostid'] ]}for i in disksinfo]
    disks_error = [host['host'] for i in disks_error_items if len(i['items']) == disks_items_len[i['hostid']] for host in disksinfo if host['hostid']==i['hostid']]
    disks_warn_items = [{'hostid':i['hostid'],'items':[item['name'] for item in disks_items if time_now - float(item['lastclock']) < 300 and i['hostid'] == item['hostid'] and item['state'] == '1' ]}for i in disksinfo]
    disks_warn = [{'uuid':host['host'],'items':i['items']} for i in disks_warn_items if len(i['items']) for host in hosts if host['hostid']==i['hostid']]
    disks_warn_uuid = [i['uuid'] for i in disks_warn ]
    print('----------------------------------disk_error:%s-------------------------------------'%(len(disks_error)))
    print(disks_error)
    print('----------------------------------disks_warn_uuid:%s-------------------------------------'%(len(disks_warn_uuid)))
    print(disks_warn_uuid)
    #print('----------------------------------disk_warn:%s-------------------------------------'%(len(disks_warn)))
    #print(disks_warn)
    
    
    
    
    
    
        
    

def main():
    uuids = []
    handle(uuids)

if __name__ == '__main__':
    main()
        
    