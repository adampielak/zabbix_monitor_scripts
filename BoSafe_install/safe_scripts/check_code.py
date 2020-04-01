#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************************************
# Function: 检查cms/core db配置文件中数据库用户名是否为root *
#           检查代码中是否存在不安全目录或文件              *
# Author: ruihua.wang@starcor.cn                            *
# DATE: 2017/11/08                                          *
#************************************************************

import os
import json
import commands
import sys

#业务类型cms/core,文件类型file
types = sys.argv[1]
#文件绝对路径
file_dir = sys.argv[2]

def command(arg1):
    (status, output) = commands.getstatusoutput(arg1)
    return status,output

def check_config(arg1,arg2):
	if not os.path.exists(arg2):
		return 1
		exit(0)

	if arg1 == "cms":
		data = []
		res = command(""" cat %s|grep "username"|grep -vE "^/|^$|^#"|awk -F "," '{print $2}'|awk -F ")" '{print $1}'|tr -d "'"|tr -d '"'|tr -d " "  """ %arg2)
		if res[0] == 0:
			data = res[1].split('\n')
			if "root" in data:
				return 0
			else:
				return 1
	elif arg1 == "core":
		data = []
		res = command(""" cat %s|grep "USER"|grep -vE "^/|^$|^#"|awk -F "," '{print $2}'|awk -F ")" '{print $1}'|tr -d "'"|tr -d '"'|tr -d " "  """ %arg2)
		if res[0] == 0:
			data = res[1].split('\n')
			if "root" in data:
				return 0
			else:
				return 1
	elif arg1 == "file":
		if not os.path.exists(arg2):
			return 1
		else:
			return 0
	elif arg1 == "content":
		#string = "adminer"
		string = sys.argv[3]
		list_a = []
		flag = 0
		res = command(""" ls -l %s|grep -vE "^d|^l|total|^$"|awk '{print $NF}'|grep -E "*.php" """ %arg2)
		if res[0] == 0:
			file_list = res[1].split('\n')
			for i in file_list:
				file_name = "%s/%s" %(arg2,i)
				with open(file_name) as fr:
					data = fr.read()
				if string in data:
					flag = 1
					list_a.append(file_name)
		if flag == 0:
			return "ok"
		else:
			return list_a
					

if __name__ == '__main__':
	print check_config(types,file_dir)
