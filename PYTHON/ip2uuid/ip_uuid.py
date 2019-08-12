import re
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
        
    def get_hosts(self):
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

    def get_items(self,hostids,item_name):
        params = {
            'output':['name','lastvalue','hostid'],
            'hostids':hostids,
            'filter':{
                'name':item_name
            }
        }
        try:
            items = self.client.item.get(**params)
            if items:
                return items
            else:
                return None
        except Exception,e:
            return None


def main():
    Found = []
    NotFound = []
    search_ips = ['135.175.12.17', '135.175.12.18', '135.175.12.19', '135.175.12.20', '135.175.12.21', '135.175.12.22', '135.175.12.23', '135.175.12.24', '135.175.12.25', '135.175.12.26', '135.175.4.9', '135.175.4.10', '135.175.4.11', '135.175.4.12', '135.175.4.13']
    NoIphosts = []
    zabbix = Zabbix(URL, USERNAME, PASSWORD)
    hosts = zabbix.get_hosts()
    if hosts:
        hostid2host = [{'hostid':host['hostid'],'uuid':host['host']}for host in hosts]
        #print(hostid2host)
        hostids = [host['hostid']for host in hosts]
        item_name = 'IPs'
        items = zabbix.get_items(hostids,item_name)
        if items:
            hostid2ip = [{'hostid':item['hostid'],'IPs':eval(item['lastvalue'])}for item in items]
            uuid2ip = [{'uuid':i['uuid'],'IPs':j['IPs']} for i in hostid2host for j in hostid2ip if i['hostid'] == j['hostid']]
            #print(hostid2ip)
            all_ips = []
            for i in uuid2ip:
                if i['IPs'] == 0:
                    NoIphosts.append(i['uuid'])
                else:
                    all_ips.extend(i['IPs'])
            #print(all_ips)
            for ip in search_ips:
                if ip not in all_ips:
                    NotFound.append(ip)
                else:
                    for i in uuid2ip:
                        if i['IPs']:
                            if ip in i['IPs']:
                                Found.append({'uuid':i['uuid'],'IPs':i['IPs']})
            print('---------------------------Total:%s------------------------------------------'%(len(search_ips)))
            print('---------------------------Found:%s------------------------------------------'%(len(Found)))
            print(Found)
            print('---------------------------NotFound:%s------------------------------------------'%(len(NotFound)))
            print(NotFound)
            print('---------------------------NoIphosts:%s------------------------------------------'%(len(NoIphosts)))
            print(NoIphosts)
        else:
        	print('get items fail')
    else:
    	print('get hosts fail')

if __name__ == '__main__':
    main()
