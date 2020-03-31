#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************
# Function:Tomcat监控脚本           *
# Author:ruihua.wang@starcor.cn     *
# DATE:2017/07/13                   *
#************************************

import commands
import os
import sys,re
import time
import json
try: 
	import xml.etree.cElementTree as ET 
except ImportError: 
	import xml.etree.ElementTree as ET


#tomcat状态页接口地址
tomcat_url = "http://127.0.0.1:8080/manager/status/all?XML=true"

#tomcat状态页登录用户
tomcat_user = "tomcat"

#tomcat状态页登录密码
tomcat_pwd = "12345"

#tomcat状态页数据
tomcat_file = "/tmp/tomcat_status.xml"

#获取curl命令路径
curl_cmd = commands.getoutput("which curl")


def command(args):
    (status, output) = commands.getstatusoutput(args)
    return status,output

def get_data():
	try:
		#url = "http://%s:%s/manager/status/all?XML=true" %(tomcat_ip, tomcat_port)
		tries = 3
		while tries:
			cmd = """ %s -s -u %s:%s %s """ %(curl_cmd, tomcat_user, tomcat_pwd, tomcat_url)
			res = command(cmd)
			if res[0] != 0:
				tries -= 1
				time.sleep(2)
			else:
				with open(tomcat_file,'w') as fw:
					fw.write(res[1].strip())
				break
			if tries == 0:
				with open(tomcat_file,'w') as fw:
					fw.write("None")
	except Exception,e:
		with open(tomcat_file,'w') as fw:
			fw.write("None")

def cache(filename,len_time):
	if not os.path.exists(filename):
		get_data()
	statinfo = os.stat(filename)
	ltime = int(statinfo.st_mtime)
	ntime = int(time.time())-len_time
	if ltime <= ntime:
		get_data()

def tomcat_port_discovery():
	try:
		cache(tomcat_file, 30)
		with open(tomcat_file, 'r') as fr:
			data = fr.read()
		if data == "None":
			print 0
			exit(1)

		tree = ET.parse(tomcat_file)
		root=tree.getroot()
		ports = []
		for content in root.findall('connector'):
			jvm_name = content.get('name').strip('"')
			if "http" in jvm_name:
				tomcat_port = jvm_name.split('-')[-1]
				ports += [{'{#TOMCAT_PORT}':tomcat_port}]
		print json.dumps({'data':ports},sort_keys=True,indent=4,separators=(',',':'))
	except Exception,e:
		print e
	
def tomcat_info(tomcat_port):
	try:
		cache(tomcat_file, 30)
		with open(tomcat_file, 'r') as fr:
			data = fr.read()
		if data == "None":
			print 0
			exit(1)
		tree = ET.parse(tomcat_file)
		root=tree.getroot()
		if sys.argv[2].strip() == "memory":
			for content in root.findall('jvm'):
				for child in content.findall('memory'):
					if sys.argv[3].strip() == "total":
						print  child.get('total')
					elif sys.argv[3].strip() == "free":
						print  child.get('free')
					elif sys.argv[3].strip() == "max":
						print  child.get('max')
					else:
						print 0
		else:
			for content in root.findall('connector'):
				if content.get('name') == '\"http-nio-%s\"' %tomcat_port:
					if sys.argv[2].strip() == "threadInfo":
						for child in content.findall('threadInfo'):
							if sys.argv[3].strip() == "maxThreads":
								print child.get('maxThreads')
							elif sys.argv[3].strip() == "currentThreadCount":
								print child.get('currentThreadCount')
							elif sys.argv[3].strip() == "currentThreadsBusy":
								print child.get('currentThreadsBusy')
							else:
								print 0
					elif sys.argv[2].strip() == "requestInfo":
						for child in content.findall('requestInfo'):
							if sys.argv[3].strip() == "maxTime":
								print  child.get('maxTime')
							elif sys.argv[3].strip() == "processingTime":
								print  child.get('processingTime')
							elif sys.argv[3].strip() == "requestCount":
								print  child.get('requestCount')
							elif sys.argv[3].strip() == "errorCount":
								print  child.get('errorCount')
							elif sys.argv[3].strip() == "bytesReceived":
								print  child.get('bytesReceived')
							elif sys.argv[3].strip() == "bytesSent":
								print  child.get('bytesSent')
							else:
								print 0
	except Exception,e:
		print 0
	

if __name__ == '__main__':
	arg1 = sys.argv[1].strip()
	if arg1 == "tomcat_port":
		tomcat_port_discovery()
	else:
		tomcat_info(arg1)
