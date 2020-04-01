#!/usr/bin/python
# coding=utf-8
"""
desc:   zabbix 接口封装
author: lu.luo
date:   2017-1-22

"""
import requests
import json
#import traceback
import sys


zabbix_url = 'http://192.168.94.37/zabbix'
zabbix_user = 'admin'
zabbix_passwd = 'Starcor@2015'
interface_url = "%s/api_jsonrpc.php" % zabbix_url


def login(user, password, url):
    interface_url = "%s/api_jsonrpc.php" % url
    login_info = {"user": user, "password": password}
    data = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": login_info,
        "id": 1}
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json-rpc", "User-Agent": "python/ZabbixAPI"})
    response = session.post(interface_url, json.dumps(data))
    response.raise_for_status()
    try:
        auth = response.json()["result"]
    except Exception:
        #traceback.print_exc()
        sys.exit(1)
    return auth

def export(auth):
    data = {
        "jsonrpc": "2.0",
        "method": "configuration.export",
        "params": {
            "options": {
                "hosts": [
                    "10161","11520"
                ]
            },
            "format": "xml"
        },
        "auth": auth,
        "id": 1
    }
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json-rpc", "User-Agent": "python/ZabbixAPI"})
    response = session.post(interface_url, json.dumps(data))
    try:
        info = response.json()
    except Exception:
        #traceback.print_exc()
        sys.exit(1)
    return info

auth = login(zabbix_user, zabbix_passwd, zabbix_url)
#conf = sys.argv[1]
info = export(auth)
with open('1.xml','w') as fw:
    fw.write(info['result'])
    

