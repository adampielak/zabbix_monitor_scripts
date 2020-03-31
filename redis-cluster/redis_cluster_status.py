#!/usr/bin/env python
# -*- coding: utf-8 -*-

#************************************
# Function:Redis-Cluster监控脚本    *
# Author:ruihua.wang@starcor.cn     *
# DATE:2017/05/22                   *
#************************************

from subprocess import Popen, PIPE
import time
import sys
import os
import signal
import json

#Redis-cli 命令路径
REDIS_BIN = "/usr/local/bin/redis-cli"

#命令执行超时时间(s)
cmd_timeout = 10
#nodes信息保存文件
nodes_file = "/tmp/redis_cluster_nodes.txt"


def sys_command_outstatuserr(cmd, timeout=120):
	try:
		p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True,close_fds=True,preexec_fn = os.setsid)
		t_beginning = time.time()
		seconds_passed = 0
		while True:
			if p.poll() is not None:
				res = p.communicate()
				exitcode = p.poll() if p.poll() else 0
				#return res[0], exitcode, res[1]
				return res[0].strip()
			seconds_passed = time.time() - t_beginning
			if timeout and seconds_passed > timeout:
				os.killpg(p.pid,signal.SIGUSR1)
				out, exitcode, err = '', 128, '执行系统命令超时'
				return 0
			time.sleep(0.1)
	except Exception,e:
		return e
	

def get_nodes():
	try:
		#Redis-cluster节点的ip端口,自动获取，无需填写
		redis_cluster = sys.argv[1].split(',')
		flag = 0
		for node in redis_cluster:
			#集群节点IP
			node_ip = node.split(':')[0].strip()
			#集群节点PORT
			node_port = node.split(':')[1].strip()
			cmd_a = """ %s -h %s -p %s -c cluster nodes """ %(REDIS_BIN.strip(),node_ip, node_port)
			res = sys_command_outstatuserr(cmd_a, timeout=cmd_timeout)
			if res:
				with open(nodes_file, 'w') as fw:
					fw.write(res.strip())
				flag = 1
				break
			else:
				continue
		if flag == 0:
			with open(nodes_file, 'w') as fw:
				fw.write("NULL")
	except Exception,e:
		with open(nodes_file, 'w') as fw:
			fw.write("NULL")

def cache(filename,len_time):
	if not os.path.exists(filename):
		get_nodes()

	statinfo = os.stat(filename)
	ltime = int(statinfo.st_mtime)
	ntime = int(time.time())-len_time
	if ltime <= ntime:
		get_nodes()

def get_node_list():
	try:
		tries = 3
		while tries:
			cache(nodes_file, 40)
			with open(nodes_file, 'r') as fr:
				data = fr.read()
			if data == "NULL":
				tries -= 1
				time.sleep(2)
			else:
				break
		if tries == 0:
			return "error"
			exit(1)	
		cmd = """ cat %s |awk '{print $2}' """ %nodes_file		
		res = sys_command_outstatuserr(cmd, timeout=cmd_timeout)
		if res:
			return res.split()
		else:
			return "error"
	except Exception,e:
		return "error"

def redis_cluster_discovery():
	t=os.popen(""" ps -ef|grep "redis"|grep -w "\[cluster\]"|awk '{print $9}' """)
	lists = []
	ports = []
	for port in  t.readlines():
		ports.append(port.strip())

	ports.sort()
	str_ports = ','.join(ports)
	lists = [{"{#REDIS_CLUSTER}":"[%s]" %str_ports, "{#REDIS_CLUSTER_NAME}":"Redis_Cluster" }]
	return json.dumps({'data':lists},sort_keys=True,indent=4,separators=(',',':'))
	
def redis_cluster_info():
	try:
		redis_cluster = get_node_list()
		if redis_cluster == "error":
			return 0
			exit(1)
		#监控指标
		item = sys.argv[2].strip()
		#获取集群健康状态
		if item == "cluster_status":
			flag = 0
			for node in redis_cluster:
				#集群节点IP
				node_ip = node.split(':')[0].strip()
				#集群节点PORT
				node_port = node.split(':')[1].strip()
				cmd_a = """ %s -h %s -p %s -c cluster info 2>/dev/null |grep "cluster_state"|awk -F ":" '{print $2}' """ %(REDIS_BIN.strip(),node_ip, node_port)
				res = sys_command_outstatuserr(cmd_a, timeout=cmd_timeout)
				if res:
					if res == "ok":
						return 1
					else:
						return 0
					flag = 1
					break
				else:
					continue
			if flag == 0:
				return 0
		#获取集群节点健康状态
		elif item == "cluster_node_status":
			with open(nodes_file) as fr:
				result = fr.read()
			num = result.count("disconnected")
			if num == 0:
				return 1
			else:
				return 0

		#监控redis读写是否正常
		elif item == "cluster_rw_status":
			flag = 0
			for node in redis_cluster:
				#集群节点IP
				node_ip = node.split(':')[0].strip()
				#集群节点PORT
				node_port = node.split(':')[1].strip()
				#写入key
				cmd_w = "%s -h %s -p %s -c  set monitor starcor" %(REDIS_BIN.strip(), node_ip, node_port)
				#读key
				cmd_r = "%s -h %s -p %s -c  get monitor" %(REDIS_BIN.strip(), node_ip, node_port)
				res = sys_command_outstatuserr(cmd_w, timeout=cmd_timeout)
				res = sys_command_outstatuserr(cmd_r, timeout=cmd_timeout)
				if res:
					if res == "starcor":
						return 1
					else:
						return 0
					flag = 1
					break
				else:
					continue
			if flag == 0:
				return 0

		#获取集群key值	
		elif item == "cluster_all_keys":
			keys = 0
			for node in redis_cluster:
				#集群节点IP
				node_ip = node.split(':')[0].strip()
				#集群节点PORT
				node_port = node.split(':')[1].strip()

				cmd_a = """ %s -h %s -p %s -c info 2>/dev/null |grep "keys="|awk -F "keys=" '{print $2}'|awk -F ',' '{sum+=$1} END {print sum}' """ %(REDIS_BIN.strip(),node_ip, node_port)
				res = sys_command_outstatuserr(cmd_a, timeout=cmd_timeout)

				if res:
					key = res
				else:
					key = 0
				keys += int(key)
			return  keys

		#获取其他监控项指标值
		else:
			a =  item.split('_')[1:]
			item = '_'.join(a).strip()
			sums = 0
			for node in redis_cluster:
				#集群节点IP
				node_ip = node.split(':')[0].strip()
				#集群节点PORT
				node_port = node.split(':')[1].strip()

				cmd_a = """ %s -h %s -p %s -c info 2>/dev/null |grep -w "%s"|cut -d : -f2 """ %(REDIS_BIN.strip(),node_ip, node_port, item)
				res = sys_command_outstatuserr(cmd_a, timeout=cmd_timeout)

				if res:
					x = res
				else:
					x = 0
				sums += int(x)
				#print node,x
			return  sums
	
	except Exception,e:
		return 0
		
	
if __name__ == "__main__":
	if sys.argv[1] == "discovery":
		print redis_cluster_discovery()
	else:
		print redis_cluster_info()

