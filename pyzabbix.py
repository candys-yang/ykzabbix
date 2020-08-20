"""
Zabbix API 调用库

by：yk


"""


from urllib import parse, request
import json, requests

class Zabbix_Start(object):
    """
    Zabbix API 的基础访问类

    Example:
        zabbix_api_obj = Zabbix_Start('172.17.26.233','user','password')
        zabbix_api_obj.result( API-Json )   #参考zabbix标准API
        zabbix_token = zabbix_api_obj.token
        zabbix_status = zabbix_api_obj.status
    """

    def __init__(self, ip, user, pwd):
        self.url = 'http://%s/zabbix/api_jsonrpc.php' % ip
        self.headers = {'User-Agent': 'python', "Content-Type": "application/json-rpc"}
        self.auth_data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": user,
                "password": pwd
            },
            "id": 1,
            "auth": None
        }
        try:
            self.token = requests.post(url=self.url, data=json.dumps(self.auth_data).encode(encoding='utf-8'),
                headers=self.headers , timeout=(6,15)).json()['result']
            self.status = "ready"
        except Exception as e:
            self.token = None
            self.status = "error"
            pass

        


    def result(self, data , isauth = True):
        """
        请求 Request Zabbix API

        Args:
            data: Zabbix 标准 api 参数
            isauth: api接口是否需要token
        """
        if isauth:
            data['auth'] = self.token
            pass
        if self.status == "error":
            raise Exception("pyzabbix API Function Connect To Zabbix Server Error.")
        
        res = requests.post(url=self.url, data=json.dumps(data).encode(encoding='utf-8'), headers=self.headers)
        if res.status_code == 200:
            res = res.json()
        else:
            res = {}

        
        
        return res


class ZabbixAPI_ApiInfo(object):
    """
    Zabbix API Info 

    Function:
        Version:返回接口版本信息

    Example:
        zapi = Zabbix_Start('172.17.26.233','Admin','zabbix')
        d = ZabbixAPI_ApiInfo(zapi)
        d.Version()
    """
    zabbixstart = ""
    def __init__(self,obj):
        self.zabbixstart = obj
        pass

    def Version(self): 
        data ={
            "jsonrpc": "2.0",
            "method": "apiinfo.version",
            "params": [],
            "id": 1
        }
        d = self.zabbixstart.result(data,False)
        return d
        pass


class ZabbixAPI_Event(object):
    """
    Zabbix Event 

    Function:
        Get_All:获取所有触发器的数据
    """

    zabbixstart = None
    def __init__(self,obj):
        self.zabbixstart = obj
        pass


    def Get_All(self):
        """
        获取所有触发器的数据。
        如果有大量的问题时，使用该方法获取数据，Zabbix服务器可能会报错。
        如果报错，则返回空值

        Example:
            zapi = Zabbix_Start('172.17.26.233','Admin','zabbix')
            d = ZabbixAPI_Event(zapi)
            s = d.Get_All()

        """
        data = {
            "jsonrpc":"2.0",
            "method":"event.get",
            "params": {
                "output": "extend",
                "selectTags": "extend",
                "sortfield": ["clock"],
                "sortorder": "DESC"
            },
            "auth": "",
            "id": 1
            }
        d = self.zabbixstart.result(data,True)
        return d
    
    def Get_All_LastTime(self,sec = 60):
        """
        获取一定时间内所有触发器的数据。
        如果有大量的问题时，使用该方法获取数据，Zabbix服务器可能会报错。
        如果报错，则返回空值

        Example:
            zapi = Zabbix_Start('172.17.26.233','Admin','zabbix')
            d = ZabbixAPI_Event(zapi)
            s = d.Get_All()

        """

        import time

        data = {
            "jsonrpc":"2.0",
            "method":"event.get",
            "params": {
                "output": "extend",
                "time_from": time.time() - sec,
                "time_till": time.time(),
                "selectTags": "extend",
                "sortfield": ["clock"],
                "sortorder": "DESC"
            },
            "auth": "",
            "id": 1
            }
        d = self.zabbixstart.result(data,True)
        return d


class ZabbixAPI_Problem(object):
    """
    Zabbix Problem

    Function:
        Get_All:获取当前的问题，对应web：检测 - 问题 里的默认显示
    """

    zabbixstart = None
    def __init__(self,obj):
        self.zabbixstart = obj
        pass

    def Get_All(self):
        """
        获取当前的触发问题。

        Example:
            zapi = Zabbix_Start('172.17.26.233','Admin','zabbix')
            d = ZabbixAPI_Problem(zapi)
            s = d.Get_All()

        """
        data = {
            "jsonrpc": "2.0",
            "method": "problem.get",
            "params": {
                "output": "extend",
                "selectAcknowledges": "extend",
                "selectTags": "extend",
                "recent": "true",
                "sortfield": ["eventid"],
                "sortorder": "DESC"
            },
            "auth": "",
            "id": 1
            }
        d = self.zabbixstart.result(data,True)
        return d

    def Get_Severity(self,leve):
        """
        获取当前的触发问题并筛选等级

        Example:
            zapi = Zabbix_Start('172.17.26.233','Admin','zabbix')
            d = ZabbixAPI_Problem(zapi)
            s = d.Get_Severity(4)
            print(s)

        """

        data = {
            "jsonrpc": "2.0",
            "method": "problem.get",
            "params": {
                "output": "extend",
                "selectAcknowledges": "extend",
                "selectTags": "extend",
                "severities":leve,
                "sortfield": ["eventid"],
                "sortorder": "DESC"
            },
            "auth": "",
            "id": 1
            }

        d = self.zabbixstart.result(data,True)
        return d
    pass


class ZabbixAPI_Hosts(object):

    """
    Zabbix Hosts 

    Function:
        Get_Hosts_All：获取当前所有主机的信息
        Search_Hosts：搜索匹配主机的信息

    """

    zabbixstart = None

    def __init__(self,obj):
        self.zabbixstart = obj
        pass

    def Get_Hosts_All(self):
        """
        获取当前所有的主机信息
        """
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "filter": {
                    "search": [
                        ''
                    ]
                }
            },
            "auth": "",
            "id": 1
        }
        d = self.zabbixstart.result(data,True)
        return d
        pass

    def Search_Hosts(self,name):
        """
        模糊搜索主机名，输出匹配主机信息
        """
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "search": {
                    "host":name
                }
            },
            "auth": "038e1d7b1735c6a5436ee9eae095879e",
            "id": 1
        }
        d = self.zabbixstart.result(data,True)
        return d
        pass

    pass


class ZabbixAPI_Item(object):
    """
    Zabbix Item

        Get_Hostids：获取指定主机的所有监控项
    """

    zabbixstart = None
    def __init__(self,obj):
        self.zabbixstart = obj
        pass

    def Get_Hostids(self,hostid):
        """
        获取指定主机id的监控项
        """
        data = {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
               "output": "extend",
               "hostids": hostid
            },
            "auth": "",
            "id": 1
        }
        d = self.zabbixstart.result(data,True)
        return d
        pass


    #def Add_HostItem(self,hostid,name,key,):
    #    """
    #    新增一个监控项
    #    """
    #    data ={
    #        "jsonrpc": "2.0",
    #        "method": "item.create",
    #        "params": {
    #            "name": name,
    #            "key_": key,
    #            "hostid": hostid,
    #            "type": 0,
    #            "value_type": 3,
    #            "interfaceid": "30084",
    #            "applications": [
    #                "609",
    #                "610"
    #            ],
    #            "delay": "30s"
    #        },
    #        "auth": "038e1d7b1735c6a5436ee9eae095879e",
    #        "id": 1
    #    }
    #    pass

    pass


class ZabbixAPI_History(object):

    """
    Zabbix History  

    Function:
       Get_History：获取指定监控项的历史数据
    """

    zabbixstart = None

    def __init__(self,obj):
        self.zabbixstart = obj
        pass

    def Get_History(self,itemids,limit = 100,sortorder = "DESC"):
        """
        根据指定参数返回监控项的历史数据。（按监控项id）
          itemids：监控项id
          limit：返回数据的量
        """
        data = {
            "jsonrpc": "2.0",
            "method": "history.get",
            "params": {
                "output": "extend",
                "itemids": itemids,
                "limit": limit,
                "history":0,
                "sortorder":sortorder
            },
            "auth": "",
            "id": ""
        }
        d = self.zabbixstart.result(data,True)
        return d
        pass

    def Get_History_Host(self,hostid,limit = 100):
        """
        根据指定的参数返回监控项的历史数据。（按主机id）
        """
        data = {
            "jsonrpc":"2.0",
            "method":"history.get",
            "params":{
                "output":"extend",
                "hostids":hostid,
                "limit":limit,
                },
            "auth":"",
            "id":""
            }
        d = self.zabbixstart.result(data,True)
        return d
        pass

    pass




