#!/usr/bin/env python
# -*- coding: utf-8 -*-

#************************************
# Function:lvs状态监控              *
# Author:ruihua.wang@starcor.com     *
# DATE:2018/07/24                   *
#************************************

import os
import json
import commands
import sys
import time

#指定VIP,如果有多个VIP，即填写多个,例如vip为1.1.1.1, 2.2.2.2 ,则配置为: keepalived_vip = ['1.1.1.1','2.2.2.2']
keepalived_vip = ['192.168.15.20']

#lvs连接数状态存储文件
con_file = "/tmp/lvs_con.txt"
#lvs转发流量速率存储文件
rate_file = "/tmp/lvs_rate.txt"

def command(arg1):
    (status, output) = commands.getstatusoutput(arg1)
    return status,output


def cache(filename,cmd):
	if not os.path.exists(filename):
		res = command(cmd)
		if res[0] == 0:
			with open(filename,'w') as fw:
				fw.write(res[1].strip())
	
	statinfo = os.stat(filename)
	ltime = int(statinfo.st_mtime)
	ntime = int(time.time())-40
	if ltime <= ntime:
		res = command(cmd)
		if res[0] == 0:
			with open(filename,'w') as fw:
				fw.write(res[1].strip())

def lvs_discovery():
	data = []
	res = command(""" /sbin/ipvsadm -Ln |sed -n '4,$p' |awk '{print $1" "$2}' """)
	if res[0] == 0:
		lines = res[1].split('\n')
		for line in lines:
			if line:
				if "TCP" in line or "UDP" in line:
					protocol = line.split()[0].strip() 
					vip = line.split()[1].strip() 
				elif "->" in line:
					rip = line.split()[1].strip() 
					data.append({"{#PROTOCOL}": protocol, "{#VIP}": vip, "{#RIP}": rip})
	return json.dumps({'data':data},sort_keys=True,indent=4,separators=(',',':'))

def lvs_status(function, args, ip):
	if function == "connection":
		cache(con_file, "/sbin/ipvsadm -Ln")
		if args == "ActiveConn":
			res = command(""" cat %s |grep -w "%s"|awk '{print $5}' """ %(con_file, ip))	
			if res[0] == 0:
				if res[1]:
					return res[1].strip()
		elif args == "InActConn":
			res = command(""" cat %s |grep -w "%s"|awk '{print $6}' """ %(con_file, ip))	
			if res[0] == 0:
				if res[1]:
					return res[1].strip()
		elif args == "rip_status":
			res = command(""" cat %s |grep -w "%s" """ %(con_file, ip))	
			if res[0] == 0:
				if res[1]:
					return 1
				else:
					return 0
			else:
				return 0
	elif function == "rate":
		cache(rate_file, "/sbin/ipvsadm -Ln --rate")
		if args == "CPS":
			res = command(""" cat %s |grep -w "%s"|awk '{print $3}' """ %(rate_file, ip))	
			if res[0] == 0:
				if res[1]:
					return res[1].strip()
		if args == "InPPS":
			res = command(""" cat %s |grep -w "%s"|awk '{print $4}' """ %(rate_file, ip))	
			if res[0] == 0:
				if res[1]:
					return res[1].strip()
		if args == "OutPPS":
			res = command(""" cat %s |grep -w "%s"|awk '{print $5}' """ %(rate_file, ip))	
			if res[0] == 0:
				if res[1]:
					return res[1].strip()
		if args == "InBPS":
			res = command(""" cat %s |grep -w "%s"|awk '{print $6}' """ %(rate_file, ip))	
			if res[0] == 0:
				if res[1]:
					return res[1].strip()
		if args == "OutBPS":
			res = command(""" cat %s |grep -w "%s"|awk '{print $7}' """ %(rate_file, ip))	
			if res[0] == 0:
				if res[1]:
					return res[1].strip()
def vip_discovery():
	data = []
	for vip in keepalived_vip: 
		data.append({"{#KEEPALIVED_VIP}": vip})
	return json.dumps({'data':data},sort_keys=True,indent=4,separators=(',',':'))

def vip_status(vip):
	res = command(""" /sbin/ip addr |grep -w "%s" """ %vip)	
	if res[0] == 0:
		if res[1]:
			return 1
		else:
			return 0
	else:
		return 0
	
if __name__ == "__main__":
	if sys.argv[1].strip() == "discovery":
		if sys.argv[2].strip() == "lvs":
			print lvs_discovery()
		elif sys.argv[2].strip() == "vip":
			print vip_discovery()
	if sys.argv[1].strip() == "status":
		if sys.argv[2].strip() == "vip_status":
			print vip_status(sys.argv[3].strip())
		else:
			print lvs_status(sys.argv[2].strip(), sys.argv[3].strip(), sys.argv[4].strip())
