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
#import simplejson as json  #特别要注意的地方

#CMS数据库配置文件地址
cms_config = "/data/starcor/www/nn_cms/nn_cms_config.php"
#lua配置文件地址
lua_config = "/data/starcor/www/nn_cms/nn_cms_config/ng_config.lua"
#haproxy配置文件地址
hap_config = "/usr/local/haproxy/conf/haproxy.cfg"

epg_config_ip="/tmp/epg_config_ip.txt"


#获取以上cms,lua,haproxy配置文件中的ip及类型，并写入文件epg_config_ip.txt
def create_config():
	try:
		content = ""
		#data = {}
		data = []
		ip_list = []
		#读取CMS数据库配置文件
		#获取DB信息
		if os.path.exists(cms_config):
			a=os.popen(""" cat %s|grep -vE "^$|^/"|grep "host"|grep "db"|awk -F "'" '{print "DB""\t"$4}'|awk -F ":" '{print $1}'|grep -v "127.0.0.1"|sort|uniq """ %cms_config)
			content += a.read()
		#获取redis信息
		if os.path.exists(cms_config):
			b=os.popen(""" cat %s|grep -vE "^$|^/"|grep "host"|grep "redis"|awk -F "'" '{print "Redis""\t"$4}'|awk -F ":" '{print $1}'|grep -v "127.0.0.1"|sort|uniq """ %cms_config)
			content += b.read()
		#获取memcache信息
		if os.path.exists(cms_config):
			c=os.popen(""" cat %s|grep -vE "^$|^/"|grep "memcache_server"|awk -F "'" '{print $4}'|awk '{split($0,a,";" ); for (i=1; i<=length(a); i++) print a[i]}'|grep -vE "^$"|awk -F ":" '{print "Memcache" "\t" $1}'|grep -v "127.0.0.1"|sort|uniq""" %cms_config)
			content += c.read()
		#获取redis-cluster信息
		if os.path.exists(cms_config):
			c=os.popen(""" cat %s|grep -vE "^$|^/"|grep "redis_cluster_server"|awk -F "'" '{print $4}'|awk '{split($0,a,";" ); for (i=1; i<=length(a); i++) print a[i]}'|grep -vE "^$"|awk -F ":" '{print "Redis-Cluster" "\t" $1}'|grep -v "127.0.0.1"|sort|uniq""" %cms_config)
			content += c.read()

		#读取lua配置文件
		if os.path.exists(lua_config):
			d=os.popen(""" cat %s |grep -vE "^$|^--"|grep "host="|awk -F "host=" '{print $2}'|awk -F '"' '{print "Redis" "\t" $2}'|grep -v "127.0.0.1"|sort|uniq """ %lua_config)
			content += d.read()

		#读取haproxy配置文件
		if os.path.exists(hap_config):
			e=os.popen(""" cat %s |grep -vE "^$|^#"|grep "server"|awk -F ":" '{print $1}'|awk '{print "DB" "\t" $3}'|grep -v "127.0.0.1"|sort|uniq """ %hap_config)
			content += e.read()

		with open(epg_config_ip, 'w') as fw:
			fw.write(content.strip())
		with open(epg_config_ip, 'r') as fr:
			lines = fr.readlines()

		for line in lines:
			ip = line.strip().split()[1]
			ip_list.append(ip)

		#ip去重
		ip_list = list(set(ip_list))
		#获取IP的类型
		for ip in ip_list:
			tag_list = []
			t = os.popen(""" cat %s|grep -w "%s" |awk '{print $1}'|sort|uniq """ %(epg_config_ip, ip))
			for i in t.readlines():
				#tag_list.append(i.split('_host')[0].strip())
				tag_list.append(i.strip())
			#data[ip] = tag_list
			tag_str = ','.join(tag_list)
			data.append({"{#IP_ADDR}":ip,"{#IP_TAG}":"[%s]" %tag_str})
		#return data
		config = json.dumps({"data":data},sort_keys=True,indent=4)

		#json格式写入配置文件
		with open(epg_config_ip, 'w') as fw:
			fw.write(config)
		return config

	except Exception,e:		
		print e
		exit()
	

#def cache(filename,len_time):
#	if not os.path.exists(filename):
#		 return create_config()
#
#	statinfo = os.stat(filename)	
#	ltime = int(statinfo.st_mtime)
#	ntime = int(time.time())-len_time
#	if ltime <= ntime:
#		return create_config()
#	else:
#		with open(filename,'r') as fr:
#			data=fr.read()
#		return data



if __name__ == "__main__":
	print create_config()
