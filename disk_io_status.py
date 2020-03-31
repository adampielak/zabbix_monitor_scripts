#!/usr/bin/env python
# -*- coding: utf-8 -*-

#************************************
# Function:服务器端口存活监控       *
# Author:ruihua.wang@starcor.cn     *
# DATE:2017/12/31                   *
#************************************

import os
import json
import commands
import sys
import time

#ss结果存储文件
io_file = "/tmp/iostat_status.txt"
#需要监控的进程名称

def command(arg1):
    (status, output) = commands.getstatusoutput(arg1)
    return status,output


def cache(filename):
    if not os.path.exists(filename):
		command(""" /usr/bin/iostat -dxkt > %s """ %io_file)
    statinfo = os.stat(filename)
    ltime = int(statinfo.st_mtime)
    ntime = int(time.time())-40
    if ltime <= ntime:
		command(""" /usr/bin/iostat -dxkt > %s """ %io_file)

def discovery_device():
	data = []
	res = command(""" cat /proc/diskstats |grep -E '\ssd[a-z]\s|\sxvd[a-z]\s|\svd[a-z]\s'|awk '{print $3}'|sort|uniq 2>/dev/null""")
	if res[0] == 0:
		names = res[1].split('\n')
		for name in names:
			data.append({'{#DEVNAME}':name.strip('\n')})
	return json.dumps({'data':data},sort_keys=True,indent=4,separators=(',',':'))

def io_status(device_name,args_type):
	try:
		cache(io_file)
		res = command(""" cat %s|grep -iw "%s" """ %(io_file,args_type))
		if res[0] == 0:
			res = command(""" cat %s|egrep -v "^$|Linux|AM|PM"|egrep -w "Device|%s"|awk '{for(i=0;++i<=NF;)a[i]=a[i]?a[i] FS $i:$i}END{for(i=0;i++<NF;)print a[i]}'|grep -iw "%s"|awk '{print $2}' 2>/dev/null""" %(io_file,device_name,args_type))
			if res[0] == 0:
				return res[1].strip()
			else:
				return 0
		else:
			return 0

	except Exception,e:
		return 0

if __name__ == "__main__":
	if sys.argv[1] == "discovery":
		print discovery_device()
	else:
		print io_status(sys.argv[1].strip(),sys.argv[2].strip())
