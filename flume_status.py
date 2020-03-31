#!/usr/bin/env python
# -*- coding: utf-8 -*-

#************************************
# Function:flume状态监控            *
# Author:ruihua.wang@starcor.com    *
# DATE:2018/05/16                   *
#************************************

import os
import json
import commands
import sys
import time
import ConfigParser

#加载环境变量
os.environ['PATH'] = "/usr/bin:/bin:/usr/local/bin:/sbin:/usr/sbin:/usr/local/sbin"

#flume端口,自动发现
FLUME_PORT = sys.argv[1].strip()
#flume_status结果存储文件
status_file = "/tmp/flume_status_%s.txt" %FLUME_PORT
#url地址
url = "http://127.0.0.1:%s/metrics" %FLUME_PORT

#curl命令路径
CURL_BIN = commands.getoutput('which curl')

def command(arg1):
    (status, output) = commands.getstatusoutput(arg1)
    return status,output

def cache(filename):
	try:
		if not os.path.exists(filename):
			res = command(""" %s -s "%s" """ %(CURL_BIN, url))
			if res[0] == 0:
				with open(filename,'w') as fw:
					fw.write(res[1].strip())
		statinfo = os.stat(filename)
		ltime = int(statinfo.st_mtime)
		ntime = int(time.time())-30
		if ltime <= ntime:
			res = command(""" %s -s "%s" """ %(CURL_BIN, url))
			if res[0] == 0:
				with open(filename,'w') as fw:
					fw.write(res[1].strip())
	except Exception,e:
		return str(e)

def flume_discovery():
	ports = []
	t=os.popen("""ps -ef |grep flume|grep -v "grep"|awk -F "monitoring.port=" '{print $2}'|awk '{print $1}'|grep -vE "^$"|uniq """ )
	for port in  t.readlines():
		r = os.path.basename(port.strip())
		ports += [{'{#FLUME_PORT}':r}]
	return json.dumps({'data':ports},sort_keys=True,indent=4,separators=(',',':'))

def flume_status(item):
	try:
		cache(status_file)
		with open(status_file) as fr:
			data = fr.read()
		content = json.loads(data)
		sum = 0
		for key,value in content.items():
			if content[key].has_key(item):
				if item == "ChannelFillPercentage":
					a = float(content[key][item])
				else:
					a = int(content[key][item])
			else:
				a = 0
			sum += a
		return sum
	
	except Exception,e:
		return str(e)

if __name__ == "__main__":
	if FLUME_PORT == "discovery":
		print flume_discovery()
	else:
		print flume_status(sys.argv[2].strip())
			
