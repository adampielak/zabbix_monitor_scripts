#!/usr/bin/python
#coding=utf-8

import json

def hex2dec(string_num): 
  	return str(int(string_num.upper(), 16)) 

def analyze():
	with open("/proc/net/ip_vs") as fp:
		contents = fp.readlines()
	
	line = len(contents)
	data=[]
	
	i = 0
	while i < line:
	    vip = {}
	    if contents[i].startswith("TCP"):
	        vip_name = contents[i].split()[1].strip()
		
		vip_ip = vip_name.split(':')[0].strip()
		vip_ip = "%s.%s.%s.%s" %(hex2dec(vip_ip[0:2]),hex2dec(vip_ip[2:4]),hex2dec(vip_ip[4:6]),hex2dec(vip_ip[6:8]))
		vip_port = vip_name.split(':')[1].strip()
		vip_port = hex2dec(vip_port)
		
		vip="%s:%s" %(vip_ip,vip_port)
		
	        while True:
	            i += 1
	            if i >= line:
	                break
	            if contents[i].startswith("TCP"):
	                i -= 1
	                break
	            else:
	                real_name = contents[i].split()[1].strip()

			real_ip = real_name.split(':')[0].strip()
			real_ip = "%s.%s.%s.%s" %(hex2dec(real_ip[0:2]),hex2dec(real_ip[2:4]),hex2dec(real_ip[4:6]),hex2dec(real_ip[6:8]))
			real_port = real_name.split(':')[1].strip()
			real_port = hex2dec(real_port)
			
			real = "%s:%s" %(real_ip,real_port)
			data.append({"{#TYPE_VIP}":vip,"{#TYPE_REAL}":real})
	    i += 1
	
	
	print json.dumps({"data":data},indent=4)

if __name__=="__main__":
	analyze()
