# ykzabbix
Zabbix API 调用库


verinfo:

  0.0.0.6 2020-08-20
    更新 Zabbix_Start 方法的底层信息。

  0.0.0.5 2020.05-14
    修复 Get_History 无法根据监控项id获取数据的问题

  0.0.0.4 2020-4-13
    新增函数：ZabbixAPI_Event.Get_All_LastTime(sec = 60)
    用于从Zabbix服务器获取最近时间的事件数据（单位：秒）。

    已知问题：
    1.  PHP默认的线程大小是 128M ，如果获取事件的数量过大，Zabbix会返回500状态码。
        当Zabbix返回500错误时，   ZabbixAPI_Event 的函数将返回 {} ，业务开发请自行处理空值问题。

  0.0.0.3 2020-4-6
    完善历史数据获取。支持：监控项、主机id获取历史数据

  0.0.0.2 
    新增历史数据获取

  0.0.0.1 
    编写了一些基础库

    Example:
        zapi = Zabbix_Start('196.168.173.162','Switch','zabbix')
        d = ZabbixAPI_Item(zapi)
        s = d.Get_Hostids('10274')
        print(s)
