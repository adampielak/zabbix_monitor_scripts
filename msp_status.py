#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************
# Function:MSP指标监控脚本          *
# Author:ruihua.wang@starcor.cn     *
# DATE:2017/07/31                   *
#************************************

import types
import urllib2
import json
import os
import sys
import time
import re
try:
  import xml.etree.cElementTree as ET
except ImportError:
  import xml.etree.ElementTree as ET

import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')


#core 平台服务器ip地址
ip_core = "127.0.0.1"


#MSP在线人数数据临时存放地址
user_filename = "/tmp/msp_users.txt"
#MSP播放成功率数据临时存放地址
play_filename = "/tmp/msp_play.txt"
#MSP播放成功率状态码数据临时存放地址
play_code_filename = "/tmp/msp_play_code.txt"
#MSP调度成功率数据临时存放地址
npss_filename = "/tmp/msp_npss.txt"
#MSP调度成功率数据临时存放地址
npss_code_filename = "/tmp/msp_npss_code.txt"
#MSP时间偏移量,并发量统计数据存放地址
offset_filename = "/tmp/msp_time_offset.txt"

#在线人数统计接口地址
user_url="http://%s/nn_core/nn_stat_log/stat_log_dispatch.php?datatype=xml&action=server_load_all_by_realtime&_=1465265108340" %ip_core.strip()
#播放成功率统计接口地址
play_url="http://%s/nn_core/nn_stat_log/stat_log_dispatch.php?datatype=json&action=play_succ_percent_by_code_today&_=1501224709904" %ip_core.strip()
#播放成功率状态码统计接口地址
play_code_url="http://%s/nn_core/nn_stat_log/stat_log_dispatch.php?datatype=json&action=get_server_play_code_total_today&type=nmds&_=1501486042048" %ip_core.strip()
#调度成功率统计接口地址
npss_url="http://%s/nn_core/nn_stat_log/stat_log_dispatch.php?datatype=json&action=npss_succ_percent_by_code_today&_=1501225404825" %ip_core.strip()
#调度成功率状态码统计接口地址
npss_code_url="http://%s/nn_core/nn_stat_log/stat_log_dispatch.php?datatype=json&action=get_server_play_code_total_today&type=npss&_=1501485804631" %ip_core.strip()
#MSP时间偏移量,并发量统计数据接口地址
offset_url="http://%s/nn_core/nn_server/server_server_func.php?first=0&perpage=999&action=list&id=&name=&group_id=&hardware_id=&type=&version=&_=1501135726331" %ip_core.strip()

def get_data(url,filename):
	try:
		tries = 3
		while tries:
			data=urllib2.urlopen(url)
			stat_code=str(data.getcode())
			if stat_code != '200':
				tries -= 1
				time.sleep(2)
			else:
				with open(filename, 'w') as fw:
					fw.write(data.read())
				break
		if tries == 0:
			with open(filename, 'w') as fw:
				fw.write("None")
	except Exception,e:
		#print e
		with open(filename, 'w') as fw:
			fw.write("None")

def cache(filename, len_time, url):
	if not os.path.exists(filename):
		get_data(url,filename)
	statinfo = os.stat(filename)
	ltime = int(statinfo.st_mtime)
	ntime = int(time.time())-len_time
	if ltime <= ntime:
		get_data(url,filename)

def timestamp_datetime(value,formats):
	#format = '%Y-%m-%d %H:00:00'
	# value为传入的值为时间戳(整形)，如：1332888820
	value = time.localtime(value)
	## 经过localtime转换后变成
	# time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
	# 最后再经过strftime函数转换为正常日期格式。
	dt = time.strftime(formats, value)
	return dt

def datetime_timestamp(value):
	#转换成时间数组
	timeArray = time.strptime(value, "%Y-%m-%d %H:%M:%S")
	#转换成时间戳
	timestamp = time.mktime(timeArray)
	return timestamp

def get_time():
	try:
		now_time = int(time.time())
		start_time = timestamp_datetime(now_time,"%Y-%m-%d %H:00:00")
		start_time = int(datetime_timestamp(start_time))
		before_30_time = int(start_time - 30 * 60)
		before_60_time = int(start_time - 60 * 60)
		middle_time = int(start_time + 30 * 60)
		end_time = int(start_time + 60 * 60)
		
		#print "now_time:", now_time,timestamp_datetime(now_time,"%H:%M")
		#print "start_time:",start_time,timestamp_datetime(start_time,"%H:%M")
		#print "middle_time:",middle_time,timestamp_datetime(middle_time,"%H:%M")
		#print "end_time:",end_time,timestamp_datetime(end_time,"%H:%M")

		if now_time == start_time:
			return timestamp_datetime(before_30_time,"%H:%M")
		elif now_time == middle_time:
			return timestamp_datetime(before_60_time,"%H:%M")
		elif now_time in range(start_time,middle_time):
			return timestamp_datetime(before_30_time,"%H:%M")
		elif now_time in range(middle_time,end_time):
			return timestamp_datetime(start_time,"%H:%M")	
		else:
			return "None"
	except Exception,e:
		#print e
		return "None"

def user_online_info(user_item):
	try:
		#取当前时间前2minutes 数据
		date=os.popen(""" date +%H:%M -d '-2 minutes' """).read().strip()
		cache(user_filename, 30, user_url)
		with open(user_filename, 'r') as fr:
			data = fr.read()
		content=json.loads(data)
		for value in content["data"]["data_list"]:
			if str(value["report_time"]) == date:
				if user_item == "total_user_count":
					return value["total_user_count"]
				elif user_item == "max_vod_user_count":
					return  value["max_vod_user_count"]
				elif user_item == "max_live_user_count":
					return value["max_live_user_count"]
				elif user_item == "max_back_user_count":
					return value["max_back_user_count"]
				elif user_item == "max_shift_user_count":
					return value["max_shift_user_count"]
				break
		else:
			return 0

	except Exception,e:
		return 0

def play_succ_percent(play_item):
	try:
		#取当前时间前2minutes 数据
		cache(play_filename, 30, play_url)
		with open(play_filename, 'r') as fr:
			data = fr.read()
		time = get_time()
		content=json.loads(data)
		for value in content["data"]["data_list"]:
			if time != "None":
				if str(value["time_point"]) == time:
					if play_item == "play_succ_percent":
						return value["succ_percent"]
					elif play_item == "succ_percent_live":
						return  value["succ_percent_live"]
					elif play_item == "succ_percent_vod":
						return value["succ_percent_vod"]
					elif play_item == "succ_percent_voda":
						return value["succ_percent_voda"]
					elif play_item == "succ_percent_tstv":
						return value["succ_percent_tstv"]
					elif play_item == "play_succ_count":
						return value["succ_count"]
					elif play_item == "play_fail_count":
						return value["fail_count"]
					break
			else:
				return 0
		else:
			return 0

	except Exception,e:
		return 0

def npss_succ_percent(npss_item):
	try:
		cache(npss_filename, 30, npss_url)
		with open(npss_filename, 'r') as fr:
			data = fr.read()
		time = get_time()
		content=json.loads(data)
		for value in content["data"]["data_list"]:
			if time != "None":
				if str(value["time_point"]) == time:
					if npss_item == "npss_succ_percent":
						return value["succ_percent"]
					elif npss_item == "all_count":
						return  value["all_count"]
					elif npss_item == "succ_count":
						return value["succ_count"]
					elif npss_item == "fail_count":
						return value["fail_count"]
					break
			else:
				return 0
		else:
			return 0

	except Exception,e:
		return 0

def code_succ_percent(filename,url,code_item):
	try:
		cache(filename, 30, url)
		with open(filename, 'r') as fr:
			data = fr.read()
		time = get_time()
		content=json.loads(data)
		for value in content["data"]:
			if time != "None":
				if str(value["report_time"]) == time:
					#print str(value["report_time"])
					sum = 0
					if code_item == "1xx":
						for key in value.keys():
							item = key.split('_')[1].strip()
							if re.findall(r'^1',item):
								x = value[key.strip()]
							else:
								x = 0
							sum += x
						return sum

					elif code_item == "2xx":
						for key in value.keys():
							item = key.split('_')[1].strip()
							if re.findall(r'^2',item):
								x = value[key.strip()]
							else:
								x = 0
							sum += x
						return sum

					elif code_item == "3xx":
						for key in value.keys():
							item = key.split('_')[1].strip()
							if re.findall(r'^3',item):
								x = value[key.strip()]
							else:
								x = 0
							sum += x
						return sum

					elif code_item == "4xx":
						for key in value.keys():
							item = key.split('_')[1].strip()
							if re.findall(r'^4',item):
								x = value[key.strip()]
							else:
								x = 0
							sum += x
						return sum

					elif code_item == "5xx":
						for key in value.keys():
							item = key.split('_')[1].strip()
							if re.findall('^5',item):
								x = value[key.strip()]
							else:
								x = 0
							sum += x
						return sum

			else:
				return 0

	except Exception,e:
		return 0

def server_discovery():
	try:
		cache(offset_filename, 30, offset_url)
		with open(offset_filename, 'r') as fr:
			data = fr.read()

		content = []
		root = ET.fromstring(data)
		for a in root.findall('server_list'):
			for b in a.findall('server'):
				#if b.get('state') == '0' and b.get('type') == 'nmds':
				if b.get('sis'):
					content.append( {"{#SERVER_NAME}": "%s-%s" %(b.get('name'),b.get('id'))} )
		return json.dumps({"data":content}, encoding='UTF-8', ensure_ascii=False, indent=4)
	except UnicodeEncodeError:
		return json.dumps({"data":content},ensure_ascii=False, indent=4)

	except Exception,e:
		return e

def time_offset(item, server_name):
	try:
		cache(offset_filename, 30, offset_url)
		with open(offset_filename, 'r') as fr:
			data = fr.read()

		content = []
		root = ET.fromstring(data)
		for a in root.findall('server_list'):
			for b in a.findall('server'):
				#if b.get('state') == '0' and b.get('type') == 'nmds':
				if b.get('sis') and server_name.split('-')[-1].strip() == b.get('id'):
					if item == "offset":
						sis = int(b.get('sis'))
						return abs(sis)
					elif item == "online_user_percent":
						limit_online_user_count = float(b.get('limit_online_user_count'))
						online_user_count = float(b.get('online_user_count'))
						if limit_online_user_count != 0:
							percent = "%.2f" %( (online_user_count/limit_online_user_count) * 100 )
							return percent
						else:
							return 0
	except Exception,e:
		return 0


if __name__=="__main__":
	item = sys.argv[1].strip()
	if item == "total_user_count":
		print user_online_info(item)
	elif item == "max_vod_user_count":
		print user_online_info(item)
	elif item == "max_live_user_count":
		print user_online_info(item)
	elif item == "max_back_user_count":
		print user_online_info(item)
	elif item == "max_shift_user_count":
		print user_online_info(item)
	elif item == "play_succ_percent":
		print play_succ_percent(item)
	elif item == "succ_percent_live":
		print play_succ_percent(item)
	elif item == "succ_percent_vod":
		print play_succ_percent(item)
	elif item == "succ_percent_voda":
		print play_succ_percent(item)
	elif item == "succ_percent_tstv":
		print play_succ_percent(item)
	elif item == "play_succ_count":
		print play_succ_percent(item)
	elif item == "play_fail_count":
		print play_succ_percent(item)
	elif item == "npss_succ_percent":
		print npss_succ_percent(item)
	elif item == "all_count":
		print npss_succ_percent(item)
	elif item == "succ_count":
		print npss_succ_percent(item)
	elif item == "fail_count":
		print npss_succ_percent(item)
	elif item == "play_1xx":
		print code_succ_percent(play_code_filename,play_code_url,"1xx")
	elif item == "play_2xx":
		print code_succ_percent(play_code_filename,play_code_url,"2xx")
	elif item == "play_3xx":
		print code_succ_percent(play_code_filename,play_code_url,"3xx")
	elif item == "play_4xx":
		print code_succ_percent(play_code_filename,play_code_url,"4xx")
	elif item == "play_5xx":
		print code_succ_percent(play_code_filename,play_code_url,"5xx")
	elif item == "npss_1xx":
		print code_succ_percent(npss_code_filename,npss_code_url,"1xx")
	elif item == "npss_2xx":
		print code_succ_percent(npss_code_filename,npss_code_url,"2xx")
	elif item == "npss_3xx":
		print code_succ_percent(npss_code_filename,npss_code_url,"3xx")
	elif item == "npss_4xx":
		print code_succ_percent(npss_code_filename,npss_code_url,"4xx")
	elif item == "npss_5xx":
		print code_succ_percent(npss_code_filename,npss_code_url,"5xx")
	elif item == "server_discovery":
		print server_discovery()
	elif item == "server_offset":
		server_name = sys.argv[2].strip()
		print time_offset("offset",server_name)
	elif item == "online_user_percent":
		server_name = sys.argv[2].strip()
		print time_offset("online_user_percent",server_name)
	else:
		print 0

	
