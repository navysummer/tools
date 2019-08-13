# -*- coding: UTF-8 -*-
from pyzabbix import ZabbixAPI, ZabbixAPIException

URL = 'http://127.0.0.1/zabbix'
USERNAME = 'Admin'
PASSWORD = 'O2rIBG5AQyh2U28Q'

class ZabbixUser(object):
    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password
        self.client = ZabbixAPI(url=url, user=user, password=password)

    def get_usergroupid_by_name(self, usergroupname='Zabbix administrators'):
        params = {
            'ouput':'extend',
            'search':{
                'name':usergroupname,
            }
        }

        try:
            usergroupitems = self.client.usergroup.get(**params)
            if usergroupitems:
                return usergroupitems[0]['usrgrpid']
            else:
                return None
        except Exception,e:
            return None
    def hgroup(self):
       params = {
          "output" : ["groupid"]
       }
       result_group = self.client.hostgroup.get(**params) 
       return result_group

    def create_usergroup(self,group_name,rights):
        params = {
            'name':group_name,
            'rights':rights
        }
        try:
            group = self.client.usergroup.create(**params)
            if group:
                return group
            else:
                return None
        except Exception,e:
            return None
        
    def update_usergroup(self,usrgrpid,rights):
        params = {
            'usrgrpid':usrgrpid,
            'rights':rights
        }
        try:
            group = self.client.usergroup.update(**params)
            if group:
                return group
            else:
                return None
        except Exception,e:
            return None    
        
    def user_add(self, username, password, group_id,userType):
        self.group_id = group_id
        params = {
            "alias": username,
            "passwd": password,
            "type": userType,
            "usrgrps": [
                {
                    "usrgrpid": self.group_id
                }
            ]
        }

        user = self.client.user.create(**params)
        print(user)
        
    def update_user_type(self, userid, userType):
        params = {
            "userid": userid,
            "type": userType
        }

        self.client.user.update(**params)
        
    def get_useid_by_username(self, username):
        params = {
            "output": "extend",
            "filter": {
                "name":username
            }
        }

        useid = self.client.user.get(**params)
        return useid

    def user_login(self, user, password):
        params = {
            "user": user,
            "password": password
        }

        print(self.client.user.login(**params))

    def use_get(self,useids):
        params ={
            "output": "userid",
            "userids":useids
        }
        print(self.client.user.get(**params))

def main():
    zabbix_user = ZabbixUser(URL, USERNAME, PASSWORD)
    Read_write_group_name = 'Zabbix administrators'
    Read_group_name = 'Zabbix Only Read'
    # permission:0 - access denied; 2 - read-only access;3 - read-write access.
    # id:ID of the host group to add permission to.
    permission = 2
    resulth = zabbix_user.hgroup()
    Read_group_rights = [{'permission':permission,'id':i["groupid"]} for i in resulth]
    host_group_id = '2'
    ywUsername = 'Admin_yw'
    ywPassword = 'Sb9cdaGaNFafeZ2v'
    qdUsername = 'Admin_qd'
    qdPassword = '0IkVUiQYJJY3BX6c'
    osUsername = 'Admin_os'
    osPassword = 'EmEeoLvjaN12M1Ao'
    neUsername = 'neutron'
    nePassword = 'yhMY0TGySUqiHVZk'
    Read_write_group_id = zabbix_user.get_usergroupid_by_name(Read_write_group_name)
    zabbix_user.user_add(ywUsername, ywPassword, Read_write_group_id,3)
    zabbix_user.user_add(qdUsername, qdPassword, Read_write_group_id,3)
    zabbix_user.user_add(neUsername, nePassword, Read_write_group_id,3)
    Read_group = zabbix_user.create_usergroup(Read_group_name,Read_group_rights)
    if Read_group :
    	Read_group_id = zabbix_user.get_usergroupid_by_name(Read_group_name)
    	zabbix_user.user_add(osUsername, osPassword, Read_group_id,1)
   

if __name__ == '__main__':
    main()
    
        
