#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
import time

MYSQL_USER = "root"
MYSQL_PWD = "HLJ-root@2017"
MYSQL_HOST = "127.0.0.1"
MYSQLADMIN_BIN="/usr/local/mysql/bin/mysqladmin"
MYSQL_BIN="/usr/local/mysql/bin/mysql"
waring_str="Warning: Using a password on the command line interface can be insecure."

def sys_command_outstatuserr(cmd, timeout=120):
	p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
	t_beginning = time.time()
	seconds_passed = 0
	while True:
		if p.poll() is not None:
			res = p.communicate()
			exitcode = p.poll() if p.poll() else 0
			string = res[1].replace(waring_str,'')

			if string.strip() or exitcode != 0:
			   return 0
			else:
			   return 1
		seconds_passed = time.time() - t_beginning
		if timeout and seconds_passed > timeout:
			p.terminate()
			out, exitcode, err = '', 128, '执行系统命令超时'
			return 0
		time.sleep(0.1)

cmd = "%s -u%s -p%s -h%s ping" %(MYSQLADMIN_BIN, MYSQL_USER, MYSQL_PWD, MYSQL_HOST)
print sys_command_outstatuserr(cmd, timeout=15)
