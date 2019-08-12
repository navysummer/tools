import sys
from pyzabbix import ZabbixAPI, ZabbixAPIException


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


def convert(URL,USERNAME,PASSWORD,search_ips):
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
        
        
def proInfo(provinces=None):
    public = {"ip":"http://10.129.133.205/", "username":"Admin", "password":"O2rIBG5AQyh2U28Q"}
    prolist = [
        #1新疆
        { "proname": "新疆", "areaname" : "system/c0c58ef59e384950a9ec826c4e178985", "hardareaname" : "system/9f7da356ba844a70b30949c4ee39e48b" },
        #2甘肃
        { "proname": "甘肃", "areaname" : "system/9cbb64ca3fdb4d96a79530b705e5c01b", "hardareaname" : "system/08ddf6c9f1e7482a9634e77ef82bd906" },
        #3重庆
        { "proname": "重庆", "areaname" : "system/5294f8fd81a54462a8456c1bc55a6d3c", "hardareaname" : "system/9739033d29524c059a27fced7ae64611" },
        #4陕西
        { "proname": "陕西", "areaname" : "system/bce15bb9e2a94dec8a1678b3356169fd", "hardareaname" : "system/83587da071504756a0ccb0f63ae14e36" },
        #5海南
        { "proname": "海南", "areaname" : "system/6215516ca9a04b15a10afb3aee17ca9f", "hardareaname" : "system/b1d7d18b289f4bb8a094c77fddcc7363" },
        #6河北
        { "proname": "河北", "areaname" : "system/7f802155b7bd4176b49a8659f41daa26", "hardareaname" : "system/d651a19ddda8439383aae8335b9f136e" },
        #7云南
        { "proname": "云南", "areaname" : "system/209039c05e274217baedb2526fa630d6", "hardareaname" : "system/009cf2f3932f43c6a3bf95ed38c8eafc" },
        #8山西
        { "proname": "山西", "areaname" : "system/f96ecbf385e541a090ffdab7acc75d28", "hardareaname" : "system/1ebc6b85d5424898af84e0085718f3bd" },
        #9江西
        { "proname": "江西", "areaname" : "system/0a446af7a27748efb92c97c318067fa4", "hardareaname" : "system/5eccd87b67644238bfc6332973d10ef0" },
        #10上海IT上云
        { "proname": "上海", "areaname" : "system/5fcb35fe60044b96935bb79e276c78c2", "hardareaname" : "system/512b86fe3d934c40bb26cb119b24c3ef" },
        #11宁夏
        { "proname": "宁夏", "areaname" : "system/0e25f501cab645bba1bd5d1b3732e128", "hardareaname" : "system/497235f991084506977ae37841844763" },
        #12北京
        { "proname": "北京", "areaname" : "system/49de602a2fbd43eea6ac5bb5a0c8f1b7", "osareaname" : "system/da116b1e1a864a5db017469cf6a27760" },
        #13天津
        { "proname": "天津", "areaname" : "system/63c9c461c6e246268c0734b8803080d9", "osareaname" : "system/63646ff479b9426baea3305e0e34d10a" },
        #14山东
        { "proname": "山东", "areaname" : "system/72c523e201964f4f82a989468de0dce2", "osareaname" : "system/f25a3f6dce654a14aa5db77b9cccdd04" },
        #15黑龙江
        { "proname": "黑龙江", "areaname" : "system/561ae493ad0c4018a9545c0f908a0942", "osareaname" : "system/b91a46dd29f54bdea0b31f8e9db2b376" },
        #16河南
        { "proname": "河南", "areaname" : "system/ed95406b78894e25b40241a41969d2b8", "osareaname" : "system/b21dff217f2d4fa3a98f0a339b46a9b2" },
        #17拉萨
        { "proname": "拉萨", "areaname" : "system/0306d9799a9c471c99d7489297860374", "osareaname" : "system/353cf68eb6e74c7a843ecb2125d0652b" },
        #18贵州
        { "proname": "贵州", "areaname" : "system/fe03a64eb4374e78952fbcd7b53b952a", "osareaname" : "system/651a5172d724451b934bd82edfc4ad9a" },
        #19内蒙
        { "proname": "内蒙", "areaname" : "system/042584dd24a7437cad32ae49aae0ebb7", "osareaname" : "system/1cd071561ab949dd80c8cdb46d4a6697" },
        #20青海
        { "proname": "青海", "areaname" : "system/2467d4f5cb1b46eb88389bd36ab0675e", "osareaname" : "system/d62664a8f0824e17bbc685d5a784b6d2" },
        #21湖北
        { "proname": "湖北", "areaname" : "system/51479f9785d1444ca39047bc4d7efb1b", "osareaname" : "system/220ee426e4fc484b8a375813cfc560b8" }
    ]
    pronames = [i["proname"] for i in prolist]
    if provinces != None:
        proids = []
        for i in provinces:
            proid = None
            try:
                proid = int(i)
            except:
                try:
                    proid = pronames.index(i)
                except:
                    proid = None
            if proid:
                proids.append(proid)
            else:
                print('参数:%s是有问题的'%(i))
        new_prolist = [prolist[j] for j in proids]
    else:
        new_prolist = prolist 
    return public,new_prolist
        

    
def main():
    search_ips = []
    params = sys.argv
    if len(params) == 1:
        public,new_prolist = proInfo()
    else:
        public,new_prolist = proInfo(params[2:])
    for i in new_prolist:
        print('------------------current province:%s---------------------------'%(i['proname']))
        print('********current cluster:user********')
        URL = public['ip'] + i['areaname']
        USERNAME = public['username']
        PASSWORD = public['password']
        convert(URL,USERNAME,PASSWORD,search_ips)
        if i.has_key('hardareaname'):
            print('********current cluster:hard********')
            URL = public['ip'] + new_prolist['hardareaname']
            convert(URL,USERNAME,PASSWORD,search_ips)
        elif i.has_key('osareaname'):
            print('********current cluster:os********')
            URL = public['ip'] + new_prolist['osareaname']
            convert(URL,USERNAME,PASSWORD,search_ips)
    

if __name__ == '__main__':
    main()
