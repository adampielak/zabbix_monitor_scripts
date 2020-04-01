#!/usr/bin/python

import urllib2
import json
import sys
import time

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

def get_hostids(header, url, auth, itemid):
	values = {
	"jsonrpc": "2.0",
	"method": "host.get",
		"params": {
		#"output": ['hostid'],
			#"selectItems": ['itemid', 'key_','value_type'],
			"output": 'extend',
			#"groupids": '%s' %groupid,
			"itemids": '%s' %itemid,
		#"filter": {
		#	"host": [
		#		"%s" %hostname
		#		]
		#}
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
		#for r in message:
		#	return r['hostid']
		return message
	except Exception,e:
		print e
		sys.exit(1)

def get_applicationids(header, url, auth, hostid, application_name):
	values = {
		"jsonrpc": "2.0",
		"method": "application.get",
		"params": {
			"output": "extend",
			"hostids": "%s" %hostid,
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
	try:
		message = output['result']
		for r in message:
			return r['applicationid']
	except Exception,e:
		print e
		sys.exit(1)

def get_items(header, url, auth, groupid, key):
	values = {
		"jsonrpc": "2.0",
		"method": "item.get",
		"params": {
			#"selectApplications":['applicationids','name'],
			#"output": "extend",
			"output": ['itemids'],
			"groupids": '%s' %groupid,
			#"hostids": "%s" %hostid,
			#"applicationids":"%s" %applicationid,
			"search": {
			    "key_": "%s" %key
        	},
        	#"sortfield": "name"
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
	#for r in output['result']:
		#print r['name'], r['itemid']
		#print r['applications']
	#print type(json.dumps(output))
	
def get_history(header, url, auth, itemid, time_len):
	time_till = int(time.time())
	time_from = int(time_till - int(time_len))
	#time_till = int(time.mktime(time.strptime(options.time_from,'%Y-%m-%d %H:%M:%S')))		
	values = {
		"jsonrpc": "2.0",
		"method": "history.get",
		"params": {
			"output": "extend",
			"history": 3,
			"itemids": "%s" %itemid,
			"sortfield": "clock",
			"time_from": "%s" %time_from,
			"time_till": "%s" %time_till,
			#"sortorder": "DESC",
			#"limit":10
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
		#for r in message:
		#	return r['applicationid']
		return message
	except Exception,e:
		print e
		sys.exit(1)

def get_groupname(header, url, auth, groupname):
	values = {
		"jsonrpc": "2.0",
		"method": "hostgroup.get",
		"params": {
			"output": ['groupids'],
			"filter": {
				"name": "%s" %groupname
			},
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
			return r['groupid']
		#return message
	except Exception,e:
		print e
		sys.exit(1)

	
if __name__ == "__main__":
	url = "http://192.168.94.152/zabbix/api_jsonrpc.php"
	user = "admin"
	passwd = "zabbix"
	header = {'Content-Type': 'application/json-rpc'}
	hostname = "192.168.94.151"
	auth = login(url, user, passwd, header)
	groupname = "test"
	key = "nginx.status[qps]"

	#getGraph(header, hostname, url, auth, 0)
	#get_items(header, hostname, url, auth)
	#print get_hostid(header, hostname, url, auth)
	#itemids = get_items(header, url, auth, hostid, applicationid)
	#hostid = get_hostids(header, hostname, url, auth, itemid)
	#print hostid
	#applicationid = get_applicationids(header, url, auth, hostid, 'msp_total')
	#itemids = get_items(header, url, auth, hostid, applicationid)
	#for i in itemids['result']:
		#print i['itemid']
	#	print get_history(header, url, auth, i['itemid'], 600)
	groupid = get_groupname(header, url, auth, groupname)
	itemids = get_items(header, url, auth, groupid, key)
	for i in itemids['result']:
		#print i['itemid']
		print get_hostids(header, url, auth, groupid, i['itemid'])
