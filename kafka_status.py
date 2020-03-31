#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************
# Function:Kafaka监控脚本           *
# Author:ruihua.wang@starcor.cn     *
# DATE:2017/07/24                   *
#************************************

import commands
import os
import sys,re
import time
import json

#zookeeper集群地址
zookeeper_cluster = "192.168.94.37:2181,192.168.94.38:2181,192.168.94.39:2181"

#kafka-consumer-groups.sh 命令路径
kafka_consumer_groups = "/usr/local/kafka/bin/kafka-consumer-groups.sh"

#kafaka 消费组信息
kafka_file = "/tmp/kafka_group.txt"


def command(args):
    (status, output) = commands.getstatusoutput(args)
    return status,output

def get_group():
	try:
		cmd_a = """ %s --zookeeper %s --list """ %(kafka_consumer_groups, zookeeper_cluster)
		res = command(cmd_a)
		if res[0] == 0:
			with open(kafka_file, 'w') as fw:
				fw.write(res[1].strip())
			#return res[1].split()
		else:
			with open(kafka_file,'w') as fw:
				fw.write("None")

	except Exception,e:
		with open(kafka_file,'w') as fw:
			fw.write("None")

def get_data(group_id):
	try:
		filename = "/tmp/kafka_%s.txt" %group_id
		str_warning = "No topic available for consumer group provided"
		cmd_a = """ %s --zookeeper %s --describe --group "%s" """ %(kafka_consumer_groups, zookeeper_cluster, group_id)
		res = command(cmd_a)
		if res[0] == 0:
			if str_warning not in res[1].strip():
				with open(filename, 'w') as fw:
					fw.write(res[1].strip())
			else:
				with open(filename,'w') as fw:
					fw.write("None")
		else:
			with open(filename,'w') as fw:
				fw.write("None")
					
	except Exception,e:
		#print e
		with open(filename,'w') as fw:
			fw.write("None")

def cache_data(filename, len_time, group_id):
	if not os.path.exists(filename):
		get_data(group_id)
	statinfo = os.stat(filename)
	ltime = int(statinfo.st_mtime)
	ntime = int(time.time())-len_time
	if ltime <= ntime:
		get_data(group_id)

def cache_group(filename, len_time):
	if not os.path.exists(filename):
		get_group()
	statinfo = os.stat(filename)
	ltime = int(statinfo.st_mtime)
	ntime = int(time.time())-len_time
	if ltime <= ntime:
		get_group()


def kafka_discovery():
	try:
		data = []
		cache_group(kafka_file, 30)
		with open(kafka_file, 'r') as fr:
			group = fr.read()
		if group != "None":
			for group_id in group.strip().split():
				filename = "/tmp/kafka_%s.txt" %group_id
				cache_data(filename, 30, group_id)
				with open(filename, 'r') as fr:
					result = fr.read()
				if result != "None":
					cmd = """ cat %s |sed -n '2,$p'|awk '{print $1,$2,$3";"}'|tr -d "\n" """ %filename
					res = command(cmd)
					if res[0] == 0:
						re_a = res[1].split(';')[:-1]
						for a in re_a:
							data.append({"{#GROUP_NAME}":a.split()[0], "{#TOPIC_NAME}":a.split()[1], "{#PARTITION_NUM}":a.split()[2]})
		return json.dumps({"data":data},sort_keys=True,indent=4)

	except Exception,e:
		return e
	
def kafka_info(group_id, topic_name, partition_num, item):
	try:
		filename = "/tmp/kafka_%s.txt" %group_id
		cache_data(filename, 30, group_id)
		with open(filename, 'r') as fr:
			result = fr.read()
		if result != "None":
			if item == "CURRENT-OFFSET":
				cmd = """ cat %s |grep -w "%s"|grep -w "%s"|awk '{if ($3=="%s") print $4}' """ %(filename, group_name, topic_name, partition_num)
			elif item == "LOG-END-OFFSET":
				cmd = """ cat %s |grep -w "%s"|grep -w "%s"|awk '{if ($3=="%s") print $5}' """ %(filename, group_name, topic_name, partition_num)
			elif item == "LAG":
				cmd = """ cat %s |grep -w "%s"|grep -w "%s"|awk '{if ($3=="%s") print $6}' """ %(filename, group_name, topic_name, partition_num)
			res = command(cmd)
			if res[0] == 0:
				return res[1].strip()
			else:
				return 0
		else:
			return 0
		
	except Exception,e:
		#print e
		return 0
	

if __name__ == '__main__':
	arg1 = sys.argv[1].strip()
	if arg1 == "kafka_discovery":
		print kafka_discovery()
	else:
		group_name = sys.argv[1].strip()
		topic_name = sys.argv[2].strip()
		partition_num = sys.argv[3].strip()
		item = sys.argv[4].strip()
		print kafka_info(group_name, topic_name, partition_num, item)
