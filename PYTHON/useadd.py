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

    def get_usergroup_by_name(self, usergroupname):
        params = {
            'ouput':'extend',
            'search':{
                'name':usergroupname,
            }
        }

        try:
            usergroupids = self.client.usergroup.get(**params)
            if usergroupids:
                return usergroupids
            else:
                return None
        except Exception,e:
            return None
        
    def user_add(self, username, password, group_id):
        self.group_id = group_id
        params = {
            "alias": username,
            "passwd": password,
            "type": 3,
            "usrgrps": [
                {
                    "usrgrpid": self.group_id
                }
            ]
        }

        self.client.user.create(**params)

    def user_login(self, user='', password=''):
        params = {
            "user": user,
            "password": password
        }

        print(self.client.user.login(**params))

def main():
    atuhuser = "test" 
    authpwd = "1234"   

    zabbix_user = ZabbixUser(URL, USERNAME, PASSWORD)
    groups = zabbix_user.get_usergroup_by_name('Zabbix administrators')
    group_id = groups[0]['usrgrpid']
    
    zabbix_user.user_add(atuhuser, authpwd, group_id)
    zabbix_user.user_login(atuhuser, authpwd)

if __name__ == '__main__':
    main()
    
        
