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

    def get_hostgroups_by_name(self, hostgroupname):
        params = {
            'ouput':'extend',
            'filter':{
                'name':hostgroupname,
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
        
    def get_hosts_by_hostgroupId(self, hostgroupId):
        params = {
            "output": "extend",
            "groupids": hostgroupId
        }
        try:
            hosts = self.client.host.get(**params)
            if hosts:
                return hosts
            else:
                return None
        except Exception,e:
            return None

    def get_hosts_by_name(self,hostname):
        params = {
            "output": "extend",
            "filter": {
                "host":hostname
            }
        }
        try:
            hosts = self.client.host.get(**params)
            if hostIds:
                return hosts
            else:
                return None
        except Exception,e:
            return None

    def get_items_by_hostId(self, hostId, item):
        params = {
            "output": "extend",
            "hostids": hostId
            "search":{
                "key_":item
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
    zabbix = Zabbix(URL, USERNAME, PASSWORD)

if __name__ == '__main__':
    main()