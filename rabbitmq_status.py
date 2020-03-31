#!/usr/bin/env python
# -*- coding: utf-8 -*-

#********************************************************
# Function:rabbitmq状态监控                             *
# Author:ruihua.wang@starcor.com                        *
# DATE:2018/02/01                                       *
# PS:需开启rabbitmq-plugins enable rabbitmq_management  *
#********************************************************

import os
import json
import commands
import sys
import time

#加载环境变量
os.environ['PATH'] = "/usr/bin:/bin:/usr/local/bin:/sbin:/usr/sbin:/usr/local/sbin"

#rabbitmq ip地址
RABBITMQ_HOST='127.0.0.1'
#rabbitmq 账号
RABBITMQ_USER='starcor'
#rabbitmq 密码
RABBITMQ_PWD='starcor'

#rabbit_mq /api/queues 结果存储文件
discovery_file = "/tmp/rabbitmq_discovery.txt"
#rabbit_mq /api/queues 结果存储文件
status_file = "/tmp/rabbitmq_status.txt"

#url地址
url = "http://%s:15672/api/queues/" %RABBITMQ_HOST.strip()

#curl命令路径
CURL_BIN = commands.getoutput('which curl')

def command(arg1):
    (status, output) = commands.getstatusoutput(arg1)
    return status,output

def cache(filename):
	try:
		if not os.path.exists(filename):
			command(""" %s -s -u "%s:%s" "%s"  > %s """ %(CURL_BIN, RABBITMQ_USER, RABBITMQ_PWD, url, filename))
		statinfo = os.stat(filename)
		ltime = int(statinfo.st_mtime)
		ntime = int(time.time())-30
		if ltime <= ntime:
			command(""" %s -s -u "%s:%s" "%s"  > %s """ %(CURL_BIN, RABBITMQ_USER, RABBITMQ_PWD, url, filename))
	except Exception,e:
		return str(e)

def rabbitmq_discovery():
	cache(discovery_file)
	data = []
	with open(discovery_file) as fr:
		content = json.loads(fr.read())
	for i in content:
		data.append({"{#QUEUE_NAME}": i.get("name").strip(),"{#VHOST_NAME}": i.get("vhost").strip()})
	return json.dumps({'data':data},sort_keys=True,indent=4,separators=(',',':'))
		

def rabbitmq_status(queue_name,vhost_name,item):
	try:
		cache(status_file)
		with open(status_file) as fr:
			content = json.loads(fr.read())
		for i in content:
			if i.get('name').strip() == queue_name and i.get('vhost').strip() == vhost_name:
				if item == "ack_rate":
					if i.has_key('message_stats'):
						if i['message_stats'].has_key('ack_details'):
							return i['message_stats']['ack_details']['rate']
						else:
							return 0
					else:
						return 0
				elif item == "deliver_rate":
					if i.has_key('message_stats'):
						if i['message_stats'].has_key('deliver_details'):
							return i['message_stats']['deliver_details']['rate']
						else:
							return 0
					else:
						return 0
				elif item == "publish_rate":
					if i.has_key('message_stats'):
						if i['message_stats'].has_key('publish_details'):
							return i['message_stats']['publish_details']['rate']
						else:
							return 0
					else:
						return 0
				elif item == "redeliver_rate":
					if i.has_key('message_stats'):
						if i['message_stats'].has_key('redeliver_details'):
							return i['message_stats']['redeliver_details']['rate']
						else:
							return 0
					else:
						return 0
				else:
					if i.has_key(item):
						return i.get(item)
					else:
						return 0
				
	except Exception,e:
		return str(e)

if __name__ == "__main__":
	if sys.argv[1] == "discovery":
		print rabbitmq_discovery()
	else:
		print rabbitmq_status(sys.argv[1].strip(),sys.argv[2].strip(),sys.argv[3].strip())
			
