#!/usr/bin/env python
#coding=utf-8

#************************************
# Function:Redis监控脚本            *
# Author:ruihua.wang@starcor.cn     *
# DATE:2018/01/09                   *
#************************************

from subprocess import Popen, PIPE
import time
import os
import signal
import commands
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#Redis绑定的IP
REDIS_HOST = "127.0.0.1"
#Redis连接密码，若配置密码则填写对应密码，若无则不填写
REDIS_PWD = ""
#Redis-cli 命令路径
REDIS_BIN = "/usr/local/redis/bin/redis-cli"

#Redis连接端口,自动获取，无需填写
REDIS_PORT = sys.argv[1]

#Redis info结果存储文件
REDIS_FILE = "/tmp/redisinfo_%s.txt" %REDIS_PORT

#Redis slow log文件
REDIS_SLOW_LOG = "/tmp/redis_slow.txt"
#REDIS_SLOW_LOG = "1.txt"


def command(arg1):
    (status, output) = commands.getstatusoutput(arg1)
    return status,output

def sys_command_outstatuserr(cmd, timeout=120):
	p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
	t_beginning = time.time()
	seconds_passed = 0
	while True:
		if p.poll() is not None:
			res = p.communicate()
			exitcode = p.poll() if p.poll() else 0
			if res[1].strip() or exitcode != 0:
			   return 0
			else:
			   return 1
		seconds_passed = time.time() - t_beginning
		if timeout and seconds_passed > timeout:
			p.terminate()
			out, exitcode, err = '', 128, '执行系统命令超时'
			return 0
		time.sleep(0.1)

def get_data():
	if REDIS_PWD.strip():
		command( """ %s -h %s -p %s -a %s info 2>/dev/null > %s """ %(REDIS_BIN.strip(),REDIS_HOST.strip(), REDIS_PORT.strip(), REDIS_PWD.strip(), REDIS_FILE.strip() ) )
	else:
		command( """ %s -h %s -p %s info 2>/dev/null > %s """ %(REDIS_BIN.strip(),REDIS_HOST.strip(), REDIS_PORT.strip(), REDIS_FILE.strip() ) )
	
def cache(filename):
    if not os.path.exists(filename):
		get_data()
    statinfo = os.stat(filename)
    ltime = int(statinfo.st_mtime)
    ntime = int(time.time()) - 40
    if ltime <= ntime:
		get_data()

def redis_discovery():
	list_a = []
	res = command(""" ps -ef |grep -w "cluster"|grep -v "grep"|awk '{print $2}' """)
	if res[0] == 0:
		if res[1]:
			list_a = res[1].strip().split('\n')
	if list_a:
		string = "|".join(list_a)
		t=os.popen("""ss -tpnl|grep redis-server|awk '{if ($NF !~/%s/) print $4}'|awk -F ":" '{print $NF}'|uniq """ %string)
	else:
		t=os.popen("""ss -tpnl|grep redis-server|awk '{print $4}'|awk -F ":" '{print $NF}'|uniq """ )
	ports = []
	for port in  t.readlines():
		r = os.path.basename(port.strip())
		ports += [{'{#REDISPORT}':r}]
	return json.dumps({'data':ports},sort_keys=True,indent=4,separators=(',',':'))

#监控redis是否挂起
def redis_run_status():
	#ping
	cmd_a = "%s -h %s -p %s -a %s ping" %(REDIS_BIN.strip(),REDIS_HOST.strip(), REDIS_PORT.strip(), REDIS_PWD.strip())
	cmd_b = "%s -h %s -p %s ping" %(REDIS_BIN.strip(),REDIS_HOST.strip(), REDIS_PORT.strip())
	if REDIS_PWD.strip():
		res = sys_command_outstatuserr(cmd_a, int(sys.argv[3]))
		if res == 0:
			return 0
		if res == 1:
			return 1
		else:
			return 0
	else:
		res = sys_command_outstatuserr(cmd_b, int(sys.argv[3]))
		if res == 0:
			return 0
		if res == 1:
			return 1
		else:
			return 0

def redis_slowlog():
	try:
		time_len = int(sys.argv[3])
		time_now = int(time.time())
		data = []
		num = 0	
		if REDIS_PWD.strip():
			res_a = command(""" %s -h %s -p %s -a %s CONFIG GET slowlog-max-len|grep -v "slowlog-max-len" """ %(REDIS_BIN.strip(),REDIS_HOST.strip(), REDIS_PORT.strip(), REDIS_PWD.strip()))
			res_b = command(""" %s -h %s -p %s -a %s slowlog get %s |grep -aE "^[1-9]" > %s """ %(REDIS_BIN.strip(),REDIS_HOST.strip(), REDIS_PORT.strip(), REDIS_PWD.strip(), res_a[1].strip(), REDIS_SLOW_LOG))
		else:
			res_a = command(""" %s -h %s -p %s CONFIG GET slowlog-max-len|grep -v "slowlog-max-len" """ %(REDIS_BIN.strip(),REDIS_HOST.strip(), REDIS_PORT.strip()))
			res_b = command(""" %s -h %s -p %s slowlog get %s |grep -aE "^[1-9]" > %s""" %(REDIS_BIN.strip(),REDIS_HOST.strip(), REDIS_PORT.strip(),res_a[1].strip(),REDIS_SLOW_LOG)) 
			#res_b = command(""" %s -h %s -p %s slowlog get %s  > %s""" %(REDIS_BIN.strip(),REDIS_HOST.strip(), REDIS_PORT.strip(),res_a[1].strip(),REDIS_SLOW_LOG)) 
		
		if res_b[0] == 0:

			with  open(REDIS_SLOW_LOG) as files:
				list_b = files.readlines()
				for i,line in enumerate(list_b):
					if i == 0:
						first_id = line.strip('\n')
						if first_id and first_id.isdigit():
							data.append(list_b[i+1].strip('\n'))
							id = int(first_id) - 1
					else:
						if line.strip('\n') == str(id):
							data.append(list_b[i+1].strip('\n'))
							id = int(id) - 1
		for key in data:
			if key and key.isdigit():
				if int(key) > int(time_now - time_len):
					num += 1
		return num
	except Exception,e:
		return e

def redis_info():
	try:
		cache(REDIS_FILE.strip())
		#监控项
		ITEM = sys.argv[2]
		#获取当前所有key数量
		if ITEM == "all_keys":
			res = command( """ cat %s |grep "keys="|awk -F "keys=" '{print $2}'|awk -F ',' '{sum+=$1} END {print sum}' """%REDIS_FILE.strip() )
			if res[0] == 0:
				if res[1]:
					return res[1].strip()
				else:
					return 0
			else:
				return 0
		
		#监控主从同步状态,1正常,0异常
		elif ITEM == "master_link_status":
			#获取redis角色
			cmd_a = """ cat %s |grep -w role|cut -d : -f2 """ %REDIS_FILE.strip()
			#获取主从同步状态值
			cmd_b = """ cat %s |grep -w "%s"|cut -d : -f2 """ %(REDIS_FILE.strip(),ITEM.strip())
			res = command(cmd_a)
			if res[0] == 0:
				role = res[1].strip()
				if role == "master":
					return 2
				elif role == "slave":
					res = command(cmd_b)
					if res[0] == 0:
						if res[1].strip() == "up":
							return 1
						else:
							return 0
					else:
						return 2
				else:
					return 2
			else:
				return 2
				
		#监控redis能否正常读取
		elif ITEM == "r_status":
			#获取随机key
			cmd_a = "%s -h %s -p %s -a %s RANDOMKEY" %(REDIS_BIN.strip(),REDIS_HOST.strip(), REDIS_PORT.strip(), REDIS_PWD.strip())
			cmd_b = "%s -h %s -p %s RANDOMKEY" %(REDIS_BIN.strip(),REDIS_HOST.strip(), REDIS_PORT.strip())
			if REDIS_PWD.strip():
				res = command(cmd_a)
				if res[0] == 0:
					return 1
				else:
					return 0
			else:
				res = command(cmd_b)
				if res[0] == 0:
					return 1
				else:
					return 0

		#监控redis使用的CPU
		elif ITEM == "cpu_usage":
			res = command(""" /bin/ps aux|grep -w "redis-server"|grep -w "%s"|grep -v "grep"|awk '{print $3}' """%REDIS_PORT.strip())
			if res[0] == 0:
				if res[1]:
					return res[1]
				else:
					return 0
			else:
				return 0

			
		#获取其他监控项指标值
		else:
			res = command(""" cat %s|grep -w "%s"|cut -d : -f2 """ %(REDIS_FILE.strip(),ITEM.strip()))
			if res[0] == 0:
				if res[1]:
					return res[1].strip()
				else:
					return 0
			else:
				return 0
				
	except Exception,e:
		return e
		
	
if __name__ == "__main__":
	if REDIS_PORT == "discovery":
		print redis_discovery()
	elif sys.argv[2] == "run_status":
		print redis_run_status()
	elif sys.argv[2] == "slow_log":
		print redis_slowlog()
	else:
		print redis_info()

