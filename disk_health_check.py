#!/usr/bin/python
# -*- coding: utf-8 -*-
#磁盘只读检测脚本，正常1，异常0

import os
import sys
import time
import atexit

#health_file="/usr/local/zabbix/etc/scripts/disk_health_check.log"
health_file="%s/disk_health_check.log" %sys.argv[1]

def cleanup():
	try:
		os.remove(health_file)
	except:
		pass

def disk_check():
	try:
		with open(health_file,'w') as fw:
			old = str(time.time())
			fw.write(old)
		with open(health_file,'r') as fr:
			new = fr.read()
		if ( old == new ):
			print 1
		else:
			print 0
		
	#except:
	except Exception:
		print 0
	
if __name__=="__main__":
	if len(sys.argv) < 2:
		print "parameter error! please input ./disk_health_check.py [DISKNAME]"
		sys.exit()
	atexit.register(cleanup)
	disk_check()
