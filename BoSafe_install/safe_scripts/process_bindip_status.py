#!/usr/bin/python
# -*- coding: utf-8 -*-

#******************************************
# Function:检查进程绑定ip是否为内网地址   *
# Author:ruihua.wang@starcor.cn           *
# DATE:2017/11/09                         *
#******************************************

import os
import json
import commands
import sys
import re

#需要监控的进程名称
process_name = ['mysqld','redis-server','mongod','memcached']

def command(arg1):
    (status, output) = commands.getstatusoutput(arg1)
    return status,output

def discovery_process():
	ports = []
	for name in process_name:
		res = command(""" ss -tpnl|grep -w "%s" >/dev/null """ %name)
		if res[0] == 0:
			ports.append({'{#PROCESSNAME}':name})
	return json.dumps({'data':ports},sort_keys=True,indent=4,separators=(',',':'))

def ip_into_int(ip):
    # 先把 192.168.1.13 变成16进制的 c0.a8.01.0d ，再去了“.”后转成10进制的 3232235789 即可。
    # (((((192 * 256) + 168) * 256) + 1) * 256) + 13
    return reduce(lambda x,y:(x<<8)+y,map(int,ip.split('.')))

def is_internal_ip(ip):
    ip = ip_into_int(ip)
    net_a = ip_into_int('10.255.255.255') >> 24
    net_b = ip_into_int('172.31.255.255') >> 20
    net_c = ip_into_int('192.168.255.255') >> 16
    return ip >> 24 == net_a or ip >>20 == net_b or ip >> 16 == net_c

def bindip_status(args):
	#获取服务器所有网卡绑定的ip地址
	res = command(""" /sbin/ip addr show|grep -w "inet"|grep "brd"|awk '{print $2}'|awk -F "/" '{print $1}' """)
	if res[0] == 0:
		local_host = res[1].split('\n')
	flag = 0 
	#判断服务器是否有外网地址
	for i in local_host:
		if re.search('^127',i):
			pass
		elif is_internal_ip(i):
			pass
		else:
			flag = 1
	res = command(""" /bin/netstat -tpnl|grep -w "%s"|awk '{print $4}'|awk -F ":" '{print $1}'|uniq|grep -v "^$"|head -1 """ %args)
	if res[0] == 0:
		if not res[1]:
			if flag == 0:
				return 1
			else:
				return 0
		elif re.search('^127',res[1].strip()):
			return 1
		elif is_internal_ip(res[1].strip()):
			return 1
		elif res[1].strip() == "0.0.0.0":
			if flag == 0:
				return 1
			else:
				return 0
		else:
			return 0
	

if __name__ == '__main__':
	if sys.argv[1] == "discovery":
		print discovery_process()
	else:
		print bindip_status(sys.argv[1])
