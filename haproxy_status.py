#!/usr/bin/python
# -*- coding: utf-8 -*-

#******************************************
#Funcition: 监控haproxy相关指标           *
#Author: ruihua.wang@starcor.cn           *
#Date: 2017/06/22                         *
#******************************************

import os
import time
import json
import sys
import commands

#socat命令路径
socat_bin="/usr/local/bin/socat"
#文件名称
stat_file="/tmp/haproxy_stat.csv"

pool_name = sys.argv[1].split(':')[0].strip()
server_name = sys.argv[1].split(':')[1].strip()
#指标
item = sys.argv[2].strip()

def command(arg1):
    (status, output) = commands.getstatusoutput(arg1)
    return status,output

#获取数据写入文件
def getdata():
	try:
		t=os.popen("""echo "show stat"|"%s" /usr/local/haproxy/haproxy.sock stdio """ %socat_bin)
		with open(stat_file, 'w') as fw:
			fw.write(t.read())
	except Exception,e:		
		with open(stat_file, 'w') as fw:
			fw.write("None")

def cache(filename,len_time):
    if not os.path.exists(filename):
        getdata()

    statinfo = os.stat(filename)
    ltime = int(statinfo.st_mtime)
    ntime = int(time.time())-len_time
    if ltime <= ntime:
         getdata()
	
def haproxy_info():
	try:
		tries = 3
		while tries:
			cache(stat_file, 30)
			with open(stat_file, 'r') as fr:
				data = fr.read()
			if data == "None":
				tries -= 1
				time.sleep(2)
			else:
				break
		if tries == 0:
			return 2
			exit(1)
		#current queued requests
		if item == "qcur":
			if server_name == "FRONTEND":
				res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $3}' %s """ %(pool_name, server_name, stat_file) )
				if res[0] == 0:
					return res[1].strip()
				else:
					return 0
			else:
				return 0
		#max queued requests
		elif item == "qmax":
			if server_name == "FRONTEND":
				res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $4}' %s """ %(pool_name, server_name, stat_file) )
				if res[0] == 0:
					return res[1].strip()
				else:
					return 0
			else:
				return 0
		#current sessions
		elif item == "scur":
			res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $5}' %s """ %(pool_name, server_name, stat_file) )
			if res[0] == 0:
				return res[1].strip()
			else:
				return 0
		#max sessions
		elif item == "smax":
			res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $6}' %s """ %(pool_name, server_name, stat_file) )
			if res[0] == 0:
				return res[1].strip()
			else:
				return 0
		#sessions limit
		elif item == "slim":
			res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $7}' %s """ %(pool_name, server_name, stat_file) )
			if res[0] == 0:
				return res[1].strip()
			else:
				return 0
		#total sessions
		elif item == "stot":
			res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $8}' %s """ %(pool_name, server_name, stat_file) )
			if res[0] == 0:
				return res[1].strip()
			else:
				return 0
		#bytes in
		elif item == "bin":
			res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $9}' %s """ %(pool_name, server_name, stat_file) )
			if res[0] == 0:
				return res[1].strip()
			else:
				return 0
		#bytes out
		elif item == "bout":
			res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $10}' %s """ %(pool_name, server_name, stat_file) )
			if res[0] == 0:
				return res[1].strip()
			else:
				return 0
		#denied requests
		#only FRONTEND and BACKEND has this field
		elif item == "dreq":
			if server_name == "FRONTEND" or server_name == "BACKEND":
				res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $11}' %s """ %(pool_name, server_name, stat_file) )
				if res[0] == 0:
					return res[1].strip()
				else:
					return 0
			else:
				return 0
		#denied responses
		elif item == "dresp":
			res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $12}' %s """ %(pool_name, server_name, stat_file) )
			if res[0] == 0:
				return res[1].strip()
			else:
				return 0
		#request errors
		#only FRONTEND has this field
		elif item == "ereq":
			if server_name == "FRONTEND":
				res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $13}' %s """ %(pool_name, server_name, stat_file) )
				if res[0] == 0:
					return res[1].strip()
				else:
					return 0
			else:
				return 0
		#connection errors
		#FRONTEND has not this field
		elif item == "econ":
			if server_name == "FRONTEND":
				res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $14}' %s """ %(pool_name, server_name, stat_file))
				if res[0] == 0:
					return res[1].strip()
				else:
					return 0
			else:
				return 0
		#response errors
		#FRONTEND has not this field
		elif item == "eresp":
			if server_name == "FRONTEND":
				res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $15}' %s """ %(pool_name, server_name, stat_file) )
				if res[0] == 0:
					return res[1].strip()
				else:
					return 0
			else:
				return 0
		#status
		elif item == "status":
			res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $18}' %s """ %(pool_name,server_name,stat_file) )
			if res[0] == 0:
				if res[1].strip() == "UP" or res[1].strip() == "OPEN":
					return 1
				else:
					return 0
					
			else:
				return 2
		#chkfail
		#number of failed checks
		#FRONTEND and BACKEND has not this field
		elif item == "chkfail":
			if server_name == "FRONTEND" or server_name == "BACKEND":
				res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $22}' %s """ %(pool_name, server_name, stat_file) )
				if res[0] == 0:
					return res[1].strip()
				else:
					return 0
			else:
				return 0
		#number of UP->DOWN transitions
		#FRONTEND has not this field will return 0
		elif item == "chkdown":
			if server_name == "FRONTEND":
				res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $23}' %s """ %(pool_name, server_name, stat_file) )
				if res[0] == 0:
					return res[1].strip()
				else:
					return 0
			else:
				return 0
		#last status change in seconds
		#FRONTEND has not this field will return 0
		elif item == "lastchg":
			if server_name == "FRONTEND":
				res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $24}' %s """ %(pool_name, server_name, stat_file))
				if res[0] == 0:
					return res[1].strip()
				else:
					return 0
			else:
				return 0
		#total downtime in seconds
		#FRONTEND has not this field will return 0
		elif item == "downtime":
			if server_name == "FRONTEND":
				res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $25}' %s """ %(pool_name, server_name, stat_file) )
				if res[0] == 0:
					return res[1].strip()
				else:
					return 0
			else:
				return 0
		#total number of times a server
		#FRONTEND has not this field
		elif item == "lbtot":
			if server_name == "FRONTEND":
				res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $31}' %s """ %(pool_name, server_name, stat_file) )
				if res[0] == 0:
					return res[1].strip()
				else:
					return 0
			else:
				return 0
		#number of sessions per second over last elapsed second
		elif item == "rate":
			res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $34}' %s """ %(pool_name, server_name, stat_file) )
			if res[0] == 0:
				return res[1].strip()
			else:
				return 0
		#limit on new sessions per second
		#only FRONTEND has this field
		elif item == "rate_limit":
			if server_name == "FRONTEND":
				res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $35}' %s """ %(pool_name, server_name, stat_file) )
				if res[0] == 0:
					return res[1].strip()
				else:
					return 0
			else:
				return 0
		#max number of new sessions per second
		elif item == "rete_max":
			res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $36}' %s """ %(pool_name, server_name, stat_file) )
			if res[0] == 0:
				return res[1].strip()
			else:
				return 0
		#status of last health check
		elif item == "check_status":
			if server_name == "FRONTEND" or server_name == "BACKEND":
				return "NULL"
			else:
				res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $37}' %s """ %(pool_name, server_name, stat_file) )
				if res[0] == 0:
					return res[1].strip()
				else:
					return 0
		#http response with 1xx code
		elif item == "hrsp_1xx":
			res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $40}' %s """ %(pool_name, server_name, stat_file) )
			if res[0] == 0:
				return res[1].strip()
			else:
				return 0
		#http response with 2xx code
		elif item == "hrsp_2xx":
			res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $41}' %s """ %(pool_name, server_name, stat_file))
			if res[0] == 0:
				return res[1].strip()
			else:
				return 0
		#http response with 3xx code
		elif item == "hrsp_3xx":
			res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $42}' %s """ %(pool_name, server_name, stat_file))
			if res[0] == 0:
				return res[1].strip()
			else:
				return 0
		#http response with 4xx code
		elif item == "hrsp_4xx":
			res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $43}' %s """ %(pool_name, server_name, stat_file))
			if res[0] == 0:
				return res[1].strip()
			else:
				return 0
		#http response with 5xx code
		elif item == "hrsp_5xx":
			res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $44}' %s """ %(pool_name, server_name, stat_file))
			if res[0] == 0:
				return res[1].strip()
			else:
				return 0
		#HTTP requests per second over last elapsed second
		#only FRONTEND has this field,others will return 0
		elif item == "req_rate":
			if server_name == "FRONTEND":
				res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $47}' %s """ %(pool_name, server_name, stat_file) )
				if res[0] == 0:
					return res[1].strip()
				else:
					return 0
			else:
				return 0
		#max number of HTTP requests per second observed
		#only FRONTEND has this field,others will return 0
		elif item == "req_rate_max":
			if server_name == "FRONTEND":
				res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $48}' %s """ %(pool_name, server_name, stat_file) )
				if res[0] == 0:
					return res[1].strip()
				else:
					return 0
			else:
				return 0
		#total number of HTTP requests recevied
		#only FRONTEND has this field,others will return 0
		elif item == "req_tot":
			if server_name == "FRONTEND":
				res = command(""" awk -F"," '$1=="'%s'"&&$2=="'%s'"{print $49}' %s """ %(pool_name, server_name, stat_file) )
				if res[0] == 0:
					return res[1].strip()
				else:
					return 0
			else:
				return 0
		else:
			return "please input the correct argument!!"

	except Exception,e:		
		return 2

if __name__ == "__main__":
	print haproxy_info()
