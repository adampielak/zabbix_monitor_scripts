#!/usr/bin/python
#coding=utf-8

import os,sys

#def dec2hex(string_num):
#	num = int(string_num)
#	mid = []
#	while True:
#	    if num == 0: break
#	    num,rem = divmod(num, 16)
#	    mid.append(base[rem])
#	
#	return ''.join([str(x) for x in mid[::-1]])

def analyze():
	ip_port = sys.argv[1]
	ip = ip_port.split(':')[0].strip()
	ip = "%s%s%s%s" %(hex(int(ip.split('.')[0]))[2:],hex(int(ip.split('.')[1]))[2:],hex(int(ip.split('.')[2]))[2:],hex(int(ip.split('.')[3]))[2:] )
	ip=ip.upper()

	port = ip_port.split(':')[1].strip()
	port = hex(int(port))[2:]
	port = port.upper().zfill(4)
	
	flag=('%s:%s') %(ip,port)

	with open("/proc/net/ip_vs") as fp:
		lines = fp.readlines()
	for line in lines:
		if flag in line:
			if sys.argv[2] == 'ActiveConn':
				print line.split()[4].strip()
			elif sys.argv[2] == 'InActConn':
				print line.split()[5].strip()
	
	
if __name__=="__main__":
	analyze()
