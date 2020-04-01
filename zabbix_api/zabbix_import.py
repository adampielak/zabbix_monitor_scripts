#!/usr/bin/python
# coding=utf-8
"""
desc:   zabbix 接口封装
author: lu.luo
date:   2017-1-22

"""
import requests
import json
import traceback
import sys


zabbix_url = 'http://192.168.94.152/zabbix'
zabbix_user = 'admin'
zabbix_passwd = 'zabbix'
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
        traceback.print_exc()
        sys.exit(1)
    return auth


def import_conf(conf, auth):
    with open(conf, 'rb') as f:
        content = f.read()
    data = {
        "jsonrpc": "2.0",
        "method": "configuration.import",
        "params": {
            "format": "xml",
            "rules": {
                "applications": {
                    "createMissing": True,
                    "updateExisting": True,
                    "deleteMissing": True
                },
                "discoveryRules": {
                    "createMissing": True,
                    "updateExisting": True,
                    "deleteMissing": True
                },
                "screens": {
                    "createMissing": True,
                    "updateExisting": True,
                    "deleteMissing": True
                },
                "maps": {
                    "createMissing": True,
                    "updateExisting": True,
                    "deleteMissing": True
                },
                "templateScreens": {
                    "createMissing": True,
                    "updateExisting": True,
                    "deleteMissing": True
                },
                "graphs": {
                    "createMissing": True,
                    "updateExisting": True,
                    "deleteMissing": True
                },
                "images": {
                    "createMissing": True,
                    "updateExisting": True,
                    "deleteMissing": True
                },
                "groups": {
                    "createMissing": True,
                    "updateExisting": True,
                    "deleteMissing": True
                },
                "hosts": {
                    "createMissing": True,
                    "updateExisting": True
                },
                "items": {
                    "createMissing": True,
                    "updateExisting": True,
                    "deleteMissing": True
                },
                "templates": {
                    "createMissing": True,
                    "updateExisting": True,
                    "deleteMissing": True
                },
                "triggers": {
                    "createMissing": True,
                    "updateExisting": True,
                    "deleteMissing": True
                }
            },
            "source": content,
        },
        "auth": auth,
        "id": 1
    }
    print json.dumps(data, indent=4)
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json-rpc", "User-Agent": "python/ZabbixAPI"})
    response = session.post(interface_url, json.dumps(data))
    try:
        info = response.json()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
    return info
auth = login(zabbix_user, zabbix_passwd, zabbix_url)
conf = sys.argv[1]
info = import_conf(conf, auth)
print info
