#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************
# Function:iptables状态监控脚本     *
# Author:ruihua.wang@starcor.cn     *
# DATE:2017/10/26                   *
#************************************

import os
import json
import commands
import sys

#需要监控的进程名称
process_name = ['mysql','redis-server','sshd','mongod','memcached']

def command(arg1):
    (status, output) = commands.getstatusoutput(arg1)
    return status,output

def discovery_port():
	ports = []
	for name in process_name:
		res = command(""" ss -tpnl|grep -w "%s"|awk '{print $4}'|awk -F ":" '{print $NF}'|uniq|head -1 """ %name)
		if res[0] == 0:
			if res[1]:
				ports.append({'{#PORTNAME}':res[1]})
	return json.dumps({'data':ports},sort_keys=True,indent=4,separators=(',',':'))

def iptable_status(args):
	if args == "status":
		res = command(""" /sbin/iptables -L -n|wc -l """)
		if res[0] == 0:
			if int(res[1]) > 8:
				return 1
			else:
				return 0
	elif args == "rule":
		res = command(""" /sbin/iptables -L -n|grep -w "%s" >/dev/null """ %sys.argv[2])
		if res[0] == 0:
			return 1
		else:
			return 0
			

if __name__ == '__main__':
	if sys.argv[1] == "discovery":
		print discovery_port()
	elif sys.argv[1] == "status":
		print iptable_status('status')
	elif sys.argv[1] == "rule":
		print iptable_status('rule')
