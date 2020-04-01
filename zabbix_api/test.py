#!/usr/bin/python

import urllib2
import json
import sys

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

#def getGraph(header, hostname, url, auth, graphtype, dynamic, columns):
def getGraph(header, hostname, url, auth, graphtype):
	if graphtype == 0:
		selecttype = ['graphid','name']
		select = 'selectGraphs'
	if (graphtype == 1):
		selecttype = ['itemid', 'value_type']
		select = 'selectItems'

	values = {
		'jsonrpc': '2.0',
		'method': 'host.get',
		'params': {
			select: selecttype,
			#'output': ['hostid', 'host'],
			'output': selecttype,
		#	"search": {
        #        "name": "test"
        #    },
		#	'searchByAny': "true",
			'filter': {
            	'host': hostname,
                "name": "test",
			},
			#"search": {
            #    "name": "test"
            #},
		},
		'auth': auth,
		'id': '2'
	}
	data = json.dumps(values)
	req = urllib2.Request(url, data, header)
	response = urllib2.urlopen(req, data)
	host_get = response.read()
	output = json.loads(host_get)
	print output
	#print json.dumps(output)


def getGraphid(header, hostid, url, auth):
	values = {
        "jsonrpc": "2.0",
        "method": "graph.get",
        "params": {
            "output": "extend",
            "hostids": "%s" %hostid,
            "search": {
                #"name": "%s" %application_name
                "name": "test"
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
        #for r in message:
        #    return r['applicationid']
		print message
	except Exception,e:
		print e
                    

def get_items(header, hostname, url, auth):
	values = {
		"jsonrpc": "2.0",
		"method": "item.get",
		"params": {
			#"selectApplications":['applicationids','name'],
			"output": "extend",
			"hostids": "10132",
			"applicationids":"620",
		#	"applications":{
		#		"applicationids":"620",
		#		"name": "port_status"
		#	},
			#"search": {
			#    "key_": "msp_status"
        	#},
        	"sortfield": "name"
		},
		"auth": auth,
		"id": 1
}

	data = json.dumps(values)
	req = urllib2.Request(url, data, header)
	response = urllib2.urlopen(req, data)
	host_get = response.read()
	output = json.loads(host_get)
	for r in output['result']:
		print r['name'],r['key_']
		#print r['applications']
	#print json.dumps(output)
	

if __name__ == "__main__":
	url = "http://192.168.94.152/zabbix/api_jsonrpc.php"
	user = "admin"
	passwd = "zabbix"
	header = {'Content-Type': 'application/json-rpc'}
	hostname = "192.168.94.151"

	#print login(url, user, passwd, header)
	auth = login(url, user, passwd, header)
	getGraphid(header, '10132', url, auth)

	#getGraph(header, hostname, url, auth, 0)
	#get_items(header, hostname, url, auth)
