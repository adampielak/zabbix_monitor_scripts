#!/usr/bin/python
# -*- coding: utf-8 -*-

#******************************************
#Funcition: 上报服务器对应端口连接的IP    *
#Author: ruihua.wang@starcor.cn           *
#Date: 2017/05/23                         *
#******************************************

import os
import json
#import simplejson as json  #特别要注意的地方

con_file="/tmp/connect_link.txt"

def getdata():
	try:
		t=os.popen(""" ss -an|egrep "ESTAB|LISTEN" """)
		with open(con_file, 'w') as fw:
			fw.write(t.read())
	except Exception,e:		
		print None
		exit()
	
def analyze():
	data = {}
	t=os.popen(""" cat %s|grep "LISTEN"|awk '{if ($4 ~/[0-9]*$/) print $4}'|awk -F ":" '{print $NF}'|sort|uniq """ %con_file) 
	for i in t.readlines():
		lists = []
		t=os.popen("""cat %s|grep "ESTAB"|grep -w "%s"|awk '{if ($5 ~/^[0-9].*$/) print $5}'|awk -F ":" '{print $1}'|sort|uniq """ %(con_file,i.strip()))
		for x in t.readlines():
			lists.append(x.strip())
		if lists:
			data[i.strip()] = lists
	return data
	

if __name__ == "__main__":
	getdata()
	print analyze()
