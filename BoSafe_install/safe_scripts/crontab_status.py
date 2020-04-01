#!/usr/bin/python
#coding=utf-8

#****************************************
# Function:监控服务器是否有异常定时器   *
# Author:ruihua.wang@starcor.com        *
# Date:2017/11/08                       *
#****************************************

import sys
import commands
import os
import re

def command(arg1):
    (status, output) = commands.getstatusoutput(arg1)
    return status,output

def crontab_status(args):
	data = ""
	result = ""
	flag = 0
	res = command(""" cat /etc/crontab 2>/dev/null|grep -vE "^#|^$|SHELL=|PATH=|MAILTO=|HOME=" """)
	if res[0] == 0:
		data += res[1]+"\n"
	res = command(""" sudo /usr/bin/crontab -l 2>/dev/null|grep -vE "^#|^$|SHELL=|PATH=|MAILTO=|HOME=" """)
	if res[0] == 0:
		data += res[1]

	crontab_list = data.split('\n')

	for i in crontab_list:
		if i:
			if re.search(args,i):
				pass
			else:
				result += i+"\n"
				flag = 1

	if flag == 1:
		return result.strip('\n')
	else:
		return "ok"

if __name__ == "__main__":
	print crontab_status(sys.argv[1])
