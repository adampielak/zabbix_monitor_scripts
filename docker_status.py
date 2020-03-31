#!/usr/bin/python
# coding=utf8
#Function="monitor docer stats"

from docker import Client
import sys
import os
import commands
import re
import time

def container_status(container_name):
	detail = c.inspect_container(container_name)
	state = detail["State"]
	if bool(state["Running"]):
		print(1)#Running
	elif bool(state["Paused"]):
		print(2)#Paused
	elif int(state["ExitCode"]) >= 0:
		print(0)#stopped
	else:
		print(3)#Crashed

def display_memory(container_name,args_type):
	detail = c.inspect_container(container_name)
	if bool(detail["State"]["Running"]):
		container_id = detail["Id"]
		if args_type == "limit_max_mem":
			with open("/cgroup/memory/docker/%s/memory.limit_in_bytes" %container_id,'r') as f:
				limit_mem = f.read()
			if len(limit_mem) > 12:
				with open("/proc/meminfo",'r') as fe:
					for line in fe:
						m = re.search(r"MemTotal: ", line)
						if m:
							print int(line.split()[1]) * 1024
			else:
				print limit_mem,
		if args_type == "usage_mem":
			with open("/cgroup/memory/docker/%s/memory.usage_in_bytes" %container_id,'r') as f:
				print f.read(),

	else:
		print 0
	
def display_network(container_name,args):
	detail = c.inspect_container(container_name)
	if bool(detail["State"]["Running"]):
		container_pid = detail["State"]["Pid"]
		with open("/proc/%s/net/dev" %container_pid, 'r') as f:
			for line in f:
				m = re.search(r"\seth0", line)
				if m:
					if args == "rx_bytes":
						rx_bytes = line.split()[1]
						print int(rx_bytes)
					elif args == "tx_bytes":
						tx_bytes = line.split()[9]
						print int(tx_bytes)
					else:
						print "args is error"
	else:
		print 0

def display_cpu(container_name):
	detail = c.inspect_container(container_name)
	if bool(detail["State"]["Running"]):
		container_id = detail["Id"]
		with open("/cgroup/cpuacct/docker/%s/cpuacct.usage" %container_id,'r') as f:
			usage_1 = int(f.read())
		with open('/proc/stat','r') as fe:
			for line in fe:
				m=re.search(r"cpu ",line) 
				if m:
					list = line.split()[1:]
					i=0
					for j in list:
					     i += int(j)
					total_1 = i
		time.sleep(1)
		with open("/cgroup/cpuacct/docker/%s/cpuacct.usage" %container_id,'r') as f:
			usage_2 = int(f.read())
		with open('/proc/stat','r') as fe:
			for line in fe:
				m=re.search(r"cpu ",line) 
				if m:
					list=line.split()[1:]
					i=0
					for j in list:
					     i+=int(j)
					total_2 = i

		user_ticks = os.sysconf(os.sysconf_names['SC_CLK_TCK'])
		
		total = float(total_2/100 - total_1/100) * 1000000000
		usage = float(usage_2 - usage_1)
		try:
			cpu_usage = float(usage/total) * 100
			print round(cpu_usage,2)
		except ZeroDivisionError:
			print 0

	else:
		print 0

#def display_cpu(container_name,args_type):
#	detail = c.inspect_container(container_name)
#	if bool(detail["State"]["Running"]):
#		container_id = detail["Id"]
#		with open("/cgroup/cpuacct/docker/%s/cpuacct.stat" %container_id,'r') as f:
#			for line in f:
#				if args_type == "cpu_user_time":
#					m = re.search(r"^user ", line)
#					if m:
#						print line.split()[1]
#				if args_type == "cpu_system_time":
#					m = re.search(r"^system ", line)
#					if m:
#						print line.split()[1]
#	else:
#		print 0
#	
#
#def display_cpu(container_name):
#	detail = c.inspect_container(container_name)
#	if bool(detail["State"]["Running"]):
#		generator=c.stats(container_name)
#		try:
#			container_stats=eval(generator.next())
#		except NameError,error_msg:
#			pass
#		finally:
#			old_result = eval(generator.next())
#			new_result = eval(generator.next())
#			c.close()
#		cpu_total_usage=new_result['cpu_stats']['cpu_usage']['total_usage'] - old_result['cpu_stats']['cpu_usage']['total_usage'] 
#		cpu_system_uasge=new_result['cpu_stats']['system_cpu_usage'] - old_result['cpu_stats']['system_cpu_usage'] 
#		cpu_num=len(old_result['cpu_stats']['cpu_usage']['percpu_usage']) 
#		cpu_percent=round((float(cpu_total_usage)/float(cpu_system_uasge))*cpu_num*100.0,2)
#		print cpu_percent
#	else:
#		print 0
		

if __name__ == '__main__':
	c = Client(base_url='unix://var/run/docker.sock',version='1.22')
	if len(sys.argv) < 3:
		#print "error! please %s [container_name] [up|cpu_per_usage|memory_usage|rx_bytes|tx_bytes]" %sys.argv[0] 	
		print "error! please %s [container_name] [up|cpu_per_usage|usage_mem|limit_max_mem|rx_bytes|tx_bytes]" %sys.argv[0] 	

	elif sys.argv[2] == "up":
		container_status(sys.argv[1])

	elif sys.argv[2] == "cpu_per_usage":
		display_cpu(sys.argv[1])

	elif sys.argv[2] == "limit_max_mem":
		display_memory(sys.argv[1],"limit_max_mem")

	elif sys.argv[2] == "usage_mem":
		display_memory(sys.argv[1],"usage_mem")

	elif sys.argv[2] == "rx_bytes":
		display_network(sys.argv[1],"rx_bytes")

	elif sys.argv[2] == "tx_bytes":
		display_network(sys.argv[1],"tx_bytes")
	else:
		print "error! please %s [container_name] [status|cpu_per_usage|memory_usage|rx_bytes|tx_bytes]" %sys.argv[0] 	
		exit(1)

