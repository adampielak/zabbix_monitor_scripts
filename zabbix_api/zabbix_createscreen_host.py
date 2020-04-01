#!/usr/bin/env python
#zabbix_screen_host.py
import urllib2
import json
import argparse
import sys

def authenticate(url, username, password):
	values = {'jsonrpc': '2.0',
	      'method': 'user.login',
	      'params': {
	        'user': username,
	        'password': password
	      },
	      'id': '0'
	      }
	data = json.dumps(values)
	req = urllib2.Request(url, data, {'Content-Type': 'application/json-rpc'})
	response = urllib2.urlopen(req, data)
	output = json.loads(response.read())
	try:
		message = output['result']
	except:
		message = output['error']['data']
		print message
		quit()
	return output['result']

def get_hostid(url, auth, hostname):
	values = {
		"jsonrpc": "2.0",
		"method": "host.get",
		    "params": {
		        "output": 'extend',
		        #"hostids": '%s' %hostid
				"filter": {
					"host": [
						"%s" %hostname
					]
				},
			},
		"auth": "%s" %auth,
		"id": 1
	}
	data = json.dumps(values)
	req = urllib2.Request(url, data, {'Content-Type': 'application/json-rpc'})
	response = urllib2.urlopen(req, data)
	output = json.loads(response.read())
	try:
		message = output['result']
		for r in message:
			return r['hostid']
	except Exception,e:
		print e
		sys.exit(1)


def getGraph(hostid, url, auth, dynamic, columns, graph_name):
	if graph_name == "Null":
		values = {
			"jsonrpc": "2.0",
			"method": "graph.get",
			"params": {
			    "output": "extend",
			    "hostids": "%s" %hostid,
			#    "search": {
			#        "name": "%s" %graph_name
			#    },
			    "sortfield": "name",
			},
			"auth": "%s" %auth,
			"id": 1
		}
	else:
		values = {
			"jsonrpc": "2.0",
			"method": "graph.get",
			"params": {
			    "output": "extend",
			    "hostids": "%s" %hostid,
			    "search": {
			        "name": "%s" %graph_name,
			       # "name": "Nginx",
			    },
			    "sortfield": "name"
			},
			"auth": "%s" %auth,
			"id": 1
		}

	data = json.dumps(values)
	req = urllib2.Request(url, data, {'Content-Type': 'application/json-rpc'})
	response = urllib2.urlopen(req, data)
	host_get = response.read()
	output = json.loads(host_get)
	graphs = []
	message = output['result']
	for i in message:
		if "Mysql" in i['name']:
			graphs.append(i['graphid'])

	graph_list = []
	x = 0
	y = 0
	for graph in graphs:
		graph_list.append({
			"resourcetype": 0,
			"resourceid": graph,
			"width": "600",
			"height": "100",
			"x": str(x),
			"y": str(y),
			"colspan": "1",
			"rowspan": "1",
			"elements": "0",
			"valign": "0",
			"halign": "0",
			"style": "0",
			"url": "",
			"dynamic": str(dynamic)
		})
		x += 1
		if x == columns:
			x = 0
			y += 1
	return graph_list

def screenCreate(url, auth, screen_name, graphids, columns):
  # print graphids
	if len(graphids) % columns == 0:
		vsize = len(graphids) / columns
	else:
		vsize = (len(graphids) / columns) + 1
	values = {"jsonrpc": "2.0",
		"method": "screen.create",
		"params": [{
		  "name": screen_name,
		  "hsize": columns,
		  "vsize": vsize,
		  "screenitems": []
		}],
		"auth": auth,
		"id": 2
		}
	for i in graphids:
		values['params'][0]['screenitems'].append(i)
	data = json.dumps(values)
	req = urllib2.Request(url, data, {'Content-Type': 'application/json-rpc'})
	response = urllib2.urlopen(req, data)
	host_get = response.read()
	output = json.loads(host_get)
	try:
		message = output['result']
	except:
		message = output['error']['data']
	print json.dumps(message)

def main():
	#url = 'http://192.168.94.152/zabbix/api_jsonrpc.php'
	#username = "admin"
	#password = "zabbix"
	url = "http://123.56.28.16:8080/zabbix/api_jsonrpc.php"
	username = "wangruihua"
	password = "5592535wang"
	parser = argparse.ArgumentParser(description='Create Zabbix screen from all of a host Items or Graphs.')
	parser.add_argument('hostname', metavar='H', type=str,
	          help='Zabbix Host to create screen from')
	parser.add_argument('screenname', metavar='N', type=str,
	          help='Screen name in Zabbix.  Put quotes around it if you want spaces in the name.')
	parser.add_argument('-g', dest='graph_name', type=str, default='Null',
	          help='graph name (default: Null)')
	parser.add_argument('-c', dest='columns', type=int, default=3,
	          help='number of columns in the screen (default: 3)')
	parser.add_argument('-d', dest='dynamic', action='store_true',
	          help='enable for dynamic screen items (default: disabled)')
	parser.add_argument('-t', dest='screentype', action='store_true',
	          help='set to 1 if you want item simple graphs created (default: 0, regular graphs)')
	args = parser.parse_args()
	hostname = args.hostname
	screen_name = args.screenname
	columns = args.columns
	graph_name = args.graph_name
	dynamic = (1 if args.dynamic else 0)
	screentype = (1 if args.screentype else 0)
	auth = authenticate(url, username, password)
	hostid = get_hostid(url, auth, hostname)
	#graph_name = "starcor"
	#print hostid
	#graphids = getGraph(hostname, url, auth, screentype, dynamic, columns)
	graphids = getGraph(hostid, url, auth, dynamic, columns, graph_name)
	#sys.exit()
	print "Screen Name: " + screen_name
	print "Total Number of Graphs: " + str(len(graphids))
	screenCreate(url, auth, screen_name, graphids, columns)

if __name__ == '__main__':
	main()
