#!/usr/bin/python
# -*- coding: utf-8 -*-

#******************************************
#Funcition: 获取EPG服务器配置文件IP信息   *
#Author: ruihua.wang@starcor.cn           *
#Date: 2017/05/23                         *
#******************************************

import os
import json
import time
import sys
#import simplejson as json  #特别要注意的地方
#reload(sys)
#sys.setdefaultencoding('utf-8')

#fping命令路径
FPING_BIN = "/usr/local/sbin/fping"
#EPG配置的IP信息
epg_config_ip="/tmp/epg_config_ip.txt"
#fping 结果文件地址
fping_res="/tmp/fping_res.txt"

#IP地址
ip_addr = sys.argv[1]
#监控项类型
m_type = sys.argv[2]
#发送数据包个数
packets_num = sys.argv[3]

#得到fping结果
def getdata():
	try:
		ip_list = []
		if os.path.exists(epg_config_ip):
			with open(epg_config_ip) as fr:
				content = json.loads(fr.read())
			if  content.has_key("data"):
				for key in content["data"]:
					if key.has_key("{#IP_ADDR}"):
						ip_list.append(key["{#IP_ADDR}"])

		ip_str = ' '.join(ip_list)
		t = os.popen(""" %s -A -u -c %s %s >%s 2>&1 """ %(FPING_BIN, packets_num, ip_str, fping_res))

	except Exception,e:		
		with open(fping_res, 'w') as fw:
			fw.write("None")



def cache(filename,len_time):
	if not os.path.exists(filename):
		getdata()

	statinfo = os.stat(filename)	
	ltime = int(statinfo.st_mtime)
	ntime = int(time.time())-len_time
	if ltime <= ntime:
		 getdata()
	#else:
	#	with open(filename,'r') as fr:
	#		data=fr.read()
	#	return data


def analyze():
	try:
		tries = 3
		while tries:
			cache(fping_res, 30)
			with open(fping_res, 'r') as fr:
				data = fr.read()
			if data == "None":
				tries -= 1
				time.sleep(2)
			else:
				break
		if tries == 0:
			return 0
			exit(1)
		t_loss = os.popen(""" cat %s |grep -w "%s"|awk -F "=" '{print $2}'|awk -F '/' '{print $3}'""" %(fping_res, ip_addr)) 
		t_req = os.popen(""" cat %s |grep -w "%s"|awk -F "max" '{print $2}'|awk -F "/" '{print $2}' """ %(fping_res, ip_addr)) 
		icmp_loss = t_loss.read().split('%')[0].strip()
		icmp_req = t_req.read().strip()
		if icmp_req == "":
			icmp_req = 0

		if m_type == "fping_loss":
			return icmp_loss
		if m_type == "fping_sec":
			return icmp_req

	except Exception,e:		
		#return e
		return 0
		
	

if __name__ == "__main__":
	print analyze()
	#print cache(epg_config_ip,30)
	#print analyze()
