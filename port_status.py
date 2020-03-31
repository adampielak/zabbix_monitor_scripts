#!/usr/bin/env python
# -*- coding: utf-8 -*-

#************************************
# Function:服务器端口存活监控       *
# Author:ruihua.wang@starcor.cn     *
# DATE:2017/12/31                   *
#************************************

import os
import json
import commands
import sys
import time

#进程存储文件
port_file = "/tmp/port_discovery.txt"
#ss结果存储文件
status_file = "/tmp/port_status.txt"
#需要监控的进程名称
process_name = ['sshd', 'nginx', 'httpd', 'php-fpm', 'mysqld', 'redis-server', 'memcached', 'mongod', 'haproxy', 'ora', 'epmd','ncds', 'nsms','tvs', 'tom3u8', 'nn_daemon_64', 'beam.smp','rsync' ,'xinetd','java','tnslsnr']

def command(arg1):
    (status, output) = commands.getstatusoutput(arg1)
    return status,output


def cache(filename):
	if not os.path.exists(filename):
		res = command(""" /usr/sbin/ss -tpnl """)
		if res[0] == 0:
			with open(filename,'w') as fw:
				fw.write(res[1].strip())
	
	statinfo = os.stat(filename)
	ltime = int(statinfo.st_mtime)
	ntime = int(time.time())-40
	if ltime <= ntime:
		res = command(""" /usr/sbin/ss -tpnl """)
		if res[0] == 0:
			with open(filename,'w') as fw:
				fw.write(res[1].strip())

def discovery_port():
	data = []
	cache(port_file)
	for name in process_name:
		res = command(""" cat %s |grep "%s" """ %(port_file, name))
		if res[0] == 0:
			res = command(""" cat %s| grep "%s"|awk '{ if ($6 != "") print $4}'|awk -F ":" '{if ($NF~/^[0-9]*$/) print $NF}'|sort|uniq 2>/dev/null """ %(port_file, name))
			if res[0] == 0:
				ports = res[1].split('\n')
			for port in ports:
				if port:
					if name == "java":
						pid = command(""" cat %s |awk '$4~/:%s$/{print $0}'|awk '{print $NF}'|awk -F "," '{print $2}' 2>/dev/null """ %(port_file, port))
						if pid[0] == 0:
							if "pid" in pid[1].strip():
								p_num = pid[1].split('=')[1].strip()
							else:
								p_num = pid[1].strip()
							res = command(""" sudo /usr/bin/jps |grep -w "%s" |awk '{print $2}' """ %p_num)
							if res[0] == 0:
								p_name = res[1].strip()
					else:
						p_name = name

					data.append({"{#PROCESS_NAME}":p_name.strip(),"{#PORT_NUM}":port.strip()})
	return json.dumps({'data':data},sort_keys=True,indent=4,separators=(',',':'))

def port_status(port_num):
	try:
		cache(status_file)
		res = command(""" cat %s|awk '{ if ($6 != "") print $4}'|awk -F ":" '{if ($NF~/^[0-9]*$/) print $NF}'|sort|uniq 2>/dev/null """ %status_file)
		if res[0] == 0:
			ports = res[1].strip().split('\n')
			if ports:
				if port_num.strip() in ports:
					return 1
				else:
					return 0
			else:
				return 2
		else:
			return 3

	except Exception,e:
		return 4

if __name__ == "__main__":
	if sys.argv[1] == "discovery":
		print discovery_port()
	else:
		print port_status(sys.argv[1].strip())
			
