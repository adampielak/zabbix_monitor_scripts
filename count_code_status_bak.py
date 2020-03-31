#!/usr/bin/python
# -*- coding: utf-8 -*-

import types
import urllib2
import json
import os
import sys
import time

filename="/tmp/code_status.json"

def jsonfile():
	try:
		url="http://127.0.0.1/service/sync_status?t=access"
		data=urllib2.urlopen(url,timeout=15)
		stat_code=str(data.getcode())
		if stat_code != '200':
			print 'GET url is Failed.exit!'
			exit()
		else:
			data=data.read()
			with open (filename,'w') as fw:
				fw.write(data)
			return data
	except Exception,e:
		print e
		exit()

def getdata():
	if not os.path.exists(filename):
		 return jsonfile()

	statinfo = os.stat(filename)	
	ltime = int(statinfo.st_mtime)
	ntime = int(time.time())-30
	if ltime <= ntime:
		return jsonfile()
	else:
		with open(filename,'r') as fr:
			data=fr.read()
		return data

def analyze_json(jsondata):
	try:
		content=json.loads(jsondata)
	except ValueError:
		print 'no json object %s' %jsondata
		exit()
	x=0
	sum = 0
	if sys.argv[1] == 'ng_total_api_hit':
		if content.has_key("ng_total_api_hit"):
			if content["ng_total_api_hit"].has_key("qps"):
				print content["ng_total_api_hit"]["qps"]	
			else:
				print 0
		else:
			print 0
	
	elif sys.argv[1] == 'service_total_api_hit':
		if content.has_key("service_total_api_hit"):
			if content["service_total_api_hit"].has_key("qps"):
				print content["service_total_api_hit"]["qps"]	
			else:
				print 0
		else:
			print 0

	elif sys.argv[1] == 'share_total_api_hit':
		if content.has_key("shared_data_hit"):
			for inter_name in content["shared_data_hit"]:
				if content["shared_data_hit"][inter_name].has_key("qps"):
					x=content["shared_data_hit"][inter_name]["qps"]
				else:
					x=0
				sum+=x
			print sum
		else:
			print 0

	elif sys.argv[1] == 'cache_total_api_hit':
		if content.has_key("cache_data_hit"):
			for inter_name in content["cache_data_hit"]:
				if content["cache_data_hit"][inter_name].has_key("qps"):
					x=content["cache_data_hit"][inter_name]["qps"]
				else:
					x=0
				sum+=x
			print sum
		else:
			print 0
	elif sys.argv[1] == 'lua_total_api_hit':
		if content.has_key("lua_api_hit"):
			for inter_name in content["lua_api_hit"]:
				if content["lua_api_hit"][inter_name].has_key("qps"):
					x=content["lua_api_hit"][inter_name]["qps"]
				else:
					x=0
				sum+=x
			print sum
		else:
			print 0

	elif sys.argv[1] == 'service_db_sql_exec_num':
		if content.has_key("service_db_sql_exec_num"):
			for inter_name in content["service_db_sql_exec_num"]:
				if content["service_db_sql_exec_num"][inter_name].has_key("qps"):
					x=content["service_db_sql_exec_num"][inter_name]["qps"]
				else:
					x=0
				sum+=x
			print sum
		else:
			print 0

	elif content.has_key("service_status_hit"):	
		for inter_name in content["service_status_hit"]:
			if sys.argv[1] == '2xx':
				if content["service_status_hit"][inter_name].has_key("2xx"):
					if content["service_status_hit"][inter_name]["2xx"].has_key("total"):
						x=content["service_status_hit"][inter_name]["2xx"]["total"]
					else:
						x=0
				else:
					x=0
				sum+=x
			elif sys.argv[1] == '3xx':
				if content["service_status_hit"][inter_name].has_key("3xx"):
					if content["service_status_hit"][inter_name]["3xx"].has_key("total"):
						x=content["service_status_hit"][inter_name]["3xx"]["total"]
					else:
						x=0
				else:
					x=0
				sum+=x
			elif sys.argv[1] == '4xx':
				if content["service_status_hit"][inter_name].has_key("4xx"):
					if content["service_status_hit"][inter_name]["4xx"].has_key("total"):
						x=content["service_status_hit"][inter_name]["4xx"]["total"]
					else:
						x=0
				else:
					x=0
				sum+=x
			elif sys.argv[1] == '5xx':
				if content["service_status_hit"][inter_name].has_key("5xx"):
					if content["service_status_hit"][inter_name]["5xx"].has_key("total"):
						x=content["service_status_hit"][inter_name]["5xx"]["total"]
					else:
						x=0
				else:
					x=0
				sum+=x
		print sum
	else:
		print 0
		


if __name__=="__main__":
	if len(sys.argv)<2:
		print """parameter error
please "python count_code_status.py [lua_total_api_hit|cache_total_api_hit|share_total_api_hit|ng_total_api_hit|service_db_sql_exec_num|service_total_api_hit|2xx|3xx|4xx|5xx]" """
		sys.exit()
	analyze_json(getdata())
