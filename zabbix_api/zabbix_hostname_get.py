#!/usr/bin/python

import urllib2
import json
import sys
import time
import os

def login(url, user, passwd, header):
	values = {
		"jsonrpc": "2.0",
		"method": "user.login",
		"params": {
			"user": user,
			"password": passwd
		},
		"id": 1
	}
	data = json.dumps(values)
	req = urllib2.Request(url, data, header)
	response = urllib2.urlopen(req, data)
	output = json.loads(response.read())
	try:
		message = output['result']
		return message
	except:
		message = output['error']['data']
		print message
		sys.exit(1)

def get_hostname(header, url, auth, hostid):
	values = {
	"jsonrpc": "2.0",
	"method": "host.get",
		"params": {
			"output": 'extend',
			#"monitored_hosts":"1",
			"hostids": '%s' %hostid
		},
	"auth": "%s" %auth,
	"id": 1
	}

	data = json.dumps(values)
	req = urllib2.Request(url, data, header)
	response = urllib2.urlopen(req, data)
	output = json.loads(response.read())
	try:
		message = output['result']
		for r in message:
			return r['name']
	except Exception,e:
		print e
		sys.exit(1)

def get_applicationids(header, url, auth, application_name):
	values = {
		"jsonrpc": "2.0",
		"method": "application.get",
		"params": {
			"output": ['hostid'],
			#"selectHosts": ['hostid','host','name'],
			#"hostids": "%s" %hostid,
			"search": {
			    "name": "%s" %application_name
			},
			"sortfield": "name"
		},
		"auth": "%s" %auth,
		"id": 1
}
	data = json.dumps(values)
	req = urllib2.Request(url, data, header)
	response = urllib2.urlopen(req, data)
	output = json.loads(response.read())
	return output
	#try:
	#	message = output['result']
	#	#for r in message:
	#		return r['hostid']
	#except Exception,e:
	#	print e
	#	sys.exit(1)

def get_items(header, url, auth, key):
	values = {
		"jsonrpc": "2.0",
		"method": "item.get",
		"params": {
			"output": ['hostid'],
			#"groupids": '%s' %groupid,
			"monitored": "true",
			"search": {
			    "key_": "%s" %key
        	},
		},
		"auth": "%s" %auth,
		"id": 1
}

	data = json.dumps(values)
	req = urllib2.Request(url, data, header)
	response = urllib2.urlopen(req, data)
	host_get = response.read()
	output = json.loads(host_get)
	return output
	

def get_groupname(header, url, auth, hostid):
	values = {
		"jsonrpc": "2.0",
		"method": "hostgroup.get",
		"params": {
			"output": ['name'],
			"hostids": "%s" %hostid,
			#"filter": {
			#	"name": "%s" %groupname
			#},
		},
		"auth": "%s" %auth,
		"id": 1
}
	data = json.dumps(values)
	req = urllib2.Request(url, data, header)
	response = urllib2.urlopen(req, data)
	output = json.loads(response.read())
	try:
		message = output['result']
		for r in message:
			return r['name']
	except Exception,e:
		print e
		sys.exit(1)

	
if __name__ == "__main__":
	#if len(sys.argv) < 2:
	#	print "Usage: %s item-key" %sys.argv[0]
	#	sys.exit(1)
	url = "http://123.56.28.16:8080/zabbix/api_jsonrpc.php"
	user = "wangruihua"
	passwd = "5592535wang"
	#url = "http://192.168.94.152/zabbix/api_jsonrpc.php"
	#user = "admin"
	#passwd = "zabbix"
	header = {'Content-Type': 'application/json-rpc'}
	auth = login(url, user, passwd, header)
	key = sys.argv[1].strip()
	data = []

	itemids = get_items(header, url, auth, key)
	#for i in itemids['result']:
	#	groupname = get_groupname(header, url, auth, i['hostid'])
	#	hostname = get_hostname(header, url, auth, i['hostid'])
	#	data.append({"{#GROUP_NAME}": groupname,"{#HOST_NAME}": hostname})
	#print json.dumps({"data":data}, encoding='UTF-8', ensure_ascii=False, indent=4)
	hostids = get_applicationids(header, url, auth, 'nginx_status')
	#print hostids
	for i in hostids['result']:
		hostname = get_hostname(header, url, auth, i['hostid'])
		groupname = get_groupname(header, url, auth, i['hostid'])
	#	print hostname,groupname
		if hostname is not None:
			data.append({"{#GROUP_NAME}": groupname,"{#HOST_NAME}": hostname})
			#print i['hostid']
		#print i['hostid']
	#print	get_hostname(header, url, auth, '10141')
	print json.dumps({"data":data}, encoding='UTF-8', ensure_ascii=False, indent=4)
