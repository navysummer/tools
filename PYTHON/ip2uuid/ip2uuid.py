from pyzabbix import ZabbixAPI, ZabbixAPIException

URL = 'http://127.0.0.1/zabbix'
USERNAME = 'Admin'
PASSWORD = 'zabbix'

class Zabbix(object):
    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password
        self.client = ZabbixAPI(url=url, user=user, password=password)
        
    def get_host_groupid_by_name(self,groupnames):
        params = {
            'ouput':'extend',
            'filter':{
                'name':groupnames,
            }
        }
        try:
            hostgroups = self.client.hostgroup.get(**params)
            if hostgroups:
                return hostgroups
            else:
                return None
        except Exception,e:
            return None
            
    def get_item_by_host_groupid(self,groupids,item):
        params = {
            'ouput':'extend',
            'groupids':groupids,
            'filter':{
                'name':item,
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

    def get_host_by_hostid(self,hostids):
        params = {
            'ouput':'extend',
            'hostids':hostids
        }
        try:
            hosts = self.client.host.get(**params)
            if hosts:
                return hosts
            else:
                return None
        except Exception,e:
            return None
            
def main():
    zabbix = Zabbix(URL, USERNAME, PASSWORD)
    check_ips = ['192.168.66.7']
    not_found_ips = []
    found_ips = []
    groupnames = ['Discovered hosts']
    groups = zabbix.get_host_groupid_by_name(groupnames)
    groupids = [group['groupid'] for group in groups]
    if groupids :
        item_name = 'IPs'
        items = zabbix.get_item_by_host_groupid(groupids,item_name)
        if items :
            info = [{'hostid':item['hostid'],'name':item['name'],'lastvalue':item['lastvalue']} for item in items]
            print(info)
            all_ip = [ i for item in info for i in eval(item['lastvalue']) ]
            print(all_ip)
            for ip in check_ips:
                if ip in all_ip :
                    found_ips.append(ip)
                else:
                    not_found_ips.append(ip)
            #hostips2ids = [ {'ip':eval(i['lastvalue'])[0],'hostid':i['hostid']} for ip in found_ips for i in info if eval(i['lastvalue'])[0] == ip]
            hostips2ids = [ {'ip':i,'hostid':item['hostid']} for ip in found_ips for item in info for i in eval(item['lastvalue']) if i == ip]
            hostids = [ i['hostid'] for i in hostips2ids ] 
            hosts = zabbix.get_host_by_hostid(hostids)
            ids2uuids = [{'hostid':host['hostid'],'uuid':host['host']} for host in hosts ]
            ips2uuids = [ {'ip':i['ip'],'uuid':j['uuid'] } for i in hostips2ids for j in ids2uuids if i['hostid'] == j['hostid'] ]
            print('----------------------------Total:%s------------------------------------------'%(len(check_ips)))
            print('----------------------------found:%s------------------------------------------'%(len(found_ips)))
            print(ips2uuids)
            print('----------------------------not found:%s------------------------------------------'%(len(not_found_ips)))
            print(not_found_ips)
        else:
            print('get item fail')
    else:
         print('get host_group fail')
    

if __name__ == '__main__':
    main()    
