#!/usr/bin/python
#coding=utf-8

#*****************************************
# Function: 大数据平台相关组件状态监控   *
# Author:ruihua.wang@starcor.com         *
# DATE:2018/06/27                        *
#*****************************************

import json
import time,datetime
from cm_api.api_client import ApiResource
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#配置信息
cm_host = "127.0.0.1"
cm_port = "7180"
username = "monitor"
password = "Starcor@1234"

#状态映射
CM_COMMISSION_MAPPING = { 'UNKNOWN': -1,
                          'COMMISSIONED': 0,
                          'DECOMMISSIONING': 1,
                          'DECOMMISSIONED': 2 
						}
CM_HEALTH_MAPPING = { 'HISTORY_NOT_AVAILABLE': -1,
                      'NOT_AVAILABLE': -1,
                      'DISABLED': -1,
                      'GOOD': 0,
                      'CONCERNING': 1,
                      'BAD': 2 
					}
CM_SERVICE_MAPPING = { 'HISTORY_NOT_AVAILABLE': -1,
                       'UNKNOWN': -1,
                       'STARTING': 0,
                       'STARTED': 0,
                       'STOPPING': 1,
                       'STOPPED': 1,
                       'NA': 0 
					}
CM_BOOLEAN_MAPPING = { 'False': 0,
                       'True': 1,
                       'FRESH': 0,
                       'STALE_REFRESHABLE': 0,
                       'STALE': 1
                     }

#主机状态名称映射
HOST_NAME_MAPPING = {'HOST_SCM_HEALTH' : '代理状态',
					 'HOST_NETWORK_INTERFACES_SLOW_MODE' : '网络接口速度',
					 'HOST_NETWORK_FRAME_ERRORS' : '帧错误',
					 'HOST_MEMORY_SWAPPING' : '内存交换',
					 'HOST_DNS_RESOLUTION' : 'DNS解析',
					 'HOST_CLOCK_OFFSET' : '时钟偏差',
					 'HOST_AGENT_PROCESS_DIRECTORY_FREE_SPACE' : '代理进程目录',
					 'HOST_AGENT_PARCEL_DIRECTORY_FREE_SPACE' : '代理parcel目录',
					 'HOST_AGENT_LOG_DIRECTORY_FREE_SPACE':'代理日志目录'
					}

#自动发现服务
def get_discovery(args):
	api = ApiResource(cm_host, cm_port,  username, password, version=3)
	data = []
	for cluster in api.get_all_clusters():
		#print cluster.name
		if args == "hosts":
			for instance in cluster.list_hosts():
				host =  api.get_host(instance.hostId)
				hostname =  host.hostname.strip()
				data.append({"{#HDPCLUSTER_NAME}": cluster.name.strip(),"{#HDPHOST_NAME}": hostname})
		elif args == "h_childs":
			for instance in cluster.list_hosts():
				host =  api.get_host(instance.hostId)
				hostname =  host.hostname.strip()
				for i in host.healthChecks:
					e_name = i['name'].strip()
					c_name = HOST_NAME_MAPPING[e_name]
					if e_name == "HOST_NETWORK_INTERFACES_SLOW_MODE":
						continue
					data.append({"{#HDPCLUSTER_NAME}": cluster.name.strip(),"{#HDPHOST_NAME}": hostname,"{#H_CHILD_E_NAME}":e_name,"{#H_CHILD_C_NAME}":c_name})
		else:
			for service in cluster.get_all_services():
				#print service.name,service.serviceState,service.healthSummary
				if args == "services":
					data.append({"{#HDPCLUSTER_NAME}": cluster.name.strip(),"{#HDPSERVICE_NAME}":service.name.strip()})
				elif args == "s_childs":
					for child in service.healthChecks:
						#print child['name']
						data.append({"{#HDPCLUSTER_NAME}": cluster.name.strip(),"{#HDPSERVICE_NAME}":service.name.strip(),"{#S_CHILD_NAME}":child['name'].strip()})
				elif args == "s_roles":
					for role in service.get_all_roles(view="full"):
						#print role.type, role.name, role.roleState,role.healthSummary,role.maintenanceMode
						data.append({"{#HDPCLUSTER_NAME}": cluster.name.strip(),"{#HDPSERVICE_NAME}":service.name.strip(),"{#HDPROLE_NAME}":role.name.strip(),"{#HDPROLE_TYPE}":role.type.strip()})

	return  json.dumps({'data':data},ensure_ascii=False,sort_keys=True,indent=4,separators=(',',':'))

#获取状态
def get_status(**kwargs):
	api = ApiResource(cm_host, cm_port,  username, password, version=3)
	for cluster in api.get_all_clusters():
		if kwargs.has_key('cluster_name') and cluster.name == kwargs['cluster_name']: 
			#获取主机状态
			if kwargs.has_key('host_name'):
				for instance in cluster.list_hosts():
					host =  api.get_host(instance.hostId)
					hostname =  host.hostname.strip()
					if hostname ==  kwargs['host_name']:
						if kwargs.has_key('h_child_name'):
							for i in  host.healthChecks:
								if i['name'] == kwargs['h_child_name']:
									return CM_HEALTH_MAPPING[str(i['summary'])]
						else:
							if kwargs['args'] == "healthSummary":
								return CM_HEALTH_MAPPING[str(host.healthSummary)]
							elif kwargs['args'] == "maintenanceMode":
								return CM_BOOLEAN_MAPPING[str(host.maintenanceMode)]
			#获取服务状态
			elif kwargs.has_key('service_name'):
				for service in cluster.get_all_services():
					if service.name.strip() == kwargs['service_name']:
						#获取对应服务下运行状态
						if kwargs.has_key('s_child_name'):
							for i in service.healthChecks:
								if i['name'] == kwargs['s_child_name']:
									return CM_HEALTH_MAPPING[str(i['summary'])]
						#获取对应服务下实例状态
						elif kwargs.has_key('s_role_name'):
							for role in service.get_all_roles(view="full"):
								if role.name.strip() == kwargs['s_role_name']:
									#print role.type, role.name, role.roleState,role.healthSummary
									if kwargs['args'] == "healthSummary":
										return CM_HEALTH_MAPPING[str(role.healthSummary)]
									elif kwargs['args'] == "maintenanceMode":
										return CM_BOOLEAN_MAPPING[str(role.maintenanceMode)]
									elif kwargs['args'] == "roleState":
										return CM_SERVICE_MAPPING[str(role.roleState)]
						#获取服务状态
						else:
							if kwargs['args'] == "healthSummary":
								return CM_HEALTH_MAPPING[str(service.healthSummary)]
							elif kwargs['args'] == "maintenanceMode":
								return CM_BOOLEAN_MAPPING[str(service.maintenanceMode)]
							elif kwargs['args'] == "serviceState":
								return CM_SERVICE_MAPPING[str(service.serviceState)]
								
def kafka_topic_discovery():
	api = ApiResource(cm_host, cm_port,  username, password, version=6)
	from_time = datetime.datetime.fromtimestamp(time.time() - 60)
	to_time = datetime.datetime.fromtimestamp(time.time())
	query="select total_kafka_bytes_received_1min_rate_across_kafka_broker_topics"
	result = api.query_timeseries(query, from_time, to_time)
	ts_list = result[0]
	topic_names = []
	for ts in ts_list.timeSeries:
		name = ts.metadata.entityName.strip()
		#print ts.metadata.metricName
		if "KAFKA_BROKER" not in name and "kafka:" in name.lower() and "__consumer_offsets" not in name:
			topic_names.append({'{#TOPIC_NAME}':name.split(':')[1].strip()})
	return json.dumps({'data':topic_names},sort_keys=True,indent=4,separators=(',',':'))

def kafka_topic_status(topic_name, args):
	api = ApiResource(cm_host, cm_port,  username, password, version=6)
	from_time = datetime.datetime.fromtimestamp(time.time() - 60)
	to_time = datetime.datetime.fromtimestamp(time.time())
	if args == "received":
		#TOPIC每分钟的接收流量
		query_received = """select total_kafka_bytes_received_1min_rate_across_kafka_broker_topics where kafkaTopicName = %s """ %topic_name
		result = api.query_timeseries(query_received, from_time, to_time)
	elif args == "fetched":
		#TOPIC每分钟的消费流量
		query_fetched = """select total_kafka_bytes_fetched_1min_rate_across_kafka_broker_topics where kafkaTopicName = "%s" """ %topic_name
		result = api.query_timeseries(query_fetched, from_time, to_time)

	ts_list = result[0]
	for ts in ts_list.timeSeries:
		if ts.data:
			for point in ts.data:
			#return "%s:\t%s" % (point.timestamp.isoformat(), point.value)
				if point.value:
					return int(point.value)
				else:
					return 0
		else:
			return 0
	
def kafka_total_broker_discovery():
	api = ApiResource(cm_host, cm_port,  username, password, version=3)
	data = []
	for cluster in api.get_all_clusters():
		for service in cluster.get_all_services():
			if service.name.lower() == "kafka": 
				data.append({"{#HDPCLUSTER_NAME}": cluster.name.strip(),"{#HDPSERVICE_NAME}":service.name.strip()})
				break
	return  json.dumps({'data':data},ensure_ascii=False,sort_keys=True,indent=4,separators=(',',':'))
		

def kafka_total_broker_status(service_name,args):
	api = ApiResource(cm_host, cm_port,  username, password, version=6)
	from_time = datetime.datetime.fromtimestamp(time.time() - 60)
	to_time = datetime.datetime.fromtimestamp(time.time())
	#整个KAFKA集群的消息接收数
	if args == "total_kafka_messages":
		query = "select total_kafka_messages_received_rate_across_kafka_brokers where entityName=%s" %service_name
	#整个KAFKA集群的消息接收速率
	elif args == "total_kafka_bytes_received":
		query = "select total_kafka_bytes_received_rate_across_kafka_brokers where entityName=%s" %service_name
	#整个KAFKA集群的消息消费速率
	elif args == "total_kafka_bytes_fetched":
		query = "select total_kafka_bytes_fetched_rate_across_kafka_brokers where entityName=%s" %service_name
	#整个KAFKA集群的分区数
	elif args == "total_kafka_partitions":
		query = "select total_kafka_partitions_across_kafka_brokers where entityName=%s" %service_name
	#整个KAFKA集群的Leader分区数
	elif args == "total_kafka_leader":
		query = "select total_kafka_leader_replicas_across_kafka_brokers where entityName=%s" %service_name
	#整个KAFKA集群的不在线分区数
	elif args == "total_kafka_offline_partitions":
		query = "select total_kafka_offline_partitions_across_kafka_brokers where entityName=%s" %service_name
	#整个KAFKA集群的副本不足的分区数
	elif args == "total_kafka_under_replicated_partitions":
		query = "select total_kafka_under_replicated_partitions_across_kafka_brokers where entityName=%s" %service_name
	else:
		return "no this args"

	result = api.query_timeseries(query, from_time, to_time)
	ts_list = result[0]
	for ts in ts_list.timeSeries:
		if ts.data:
			for point in ts.data:
			#return "%s:\t%s" % (point.timestamp.isoformat(), point.value)
				if point.value:
					return int(point.value)
				else:
					return 0
		else:
			return 0

def kafka_broker_discovery():
	api = ApiResource(cm_host, cm_port,  username, password, version=3)
	data = []
	for cluster in api.get_all_clusters():
		for service in cluster.get_all_services():
			if service.name.lower() == "kafka": 
				for role in service.get_all_roles(view="full"):
					#print role.type, role.name,role.hostRef.hostId, role.roleState,role.healthSummary
					rolename = role.name.strip()
					hostname =  api.get_host(role.hostRef.hostId).hostname.strip()
					
					data.append({"{#HDPCLUSTER_NAME}": cluster.name.strip(), "{#HDPSERVICE_NAME}": service.name.strip(),"{#ROLE_NAME}": rolename, "{#HOST_NAME}": hostname})
				break
	return  json.dumps({'data':data},ensure_ascii=False,sort_keys=True,indent=4,separators=(',',':'))
	

def kafka_broker_status(role_name, args):
	#该broker接收消息量
	if args == "kafka_messages_received":
		query = "select kafka_messages_received_rate where entityName=%s" %role_name
	#该broker不在线的分区数
	elif args == "kafka_offline_partitions":
		query = "select kafka_offline_partitions where entityName=%s" %role_name
	#该broker副本不足的分区数
	elif args == "kafka_under_replicated_partitions":
		query = "select kafka_under_replicated_partitions where entityName=%s" %role_name
	#该broker的Leader副本数
	elif args == "kafka_leader_replicas":
		query = "select kafka_leader_replicas where entityName=%s" %role_name
	#该broker消息消费速率
	elif args == "kafka_bytes_fetched":
		query = "select kafka_bytes_fetched_rate where entityName=%s" %role_name
	#该broker消息接收速率
	elif args == "kafka_bytes_received":
		query = "select kafka_bytes_received_rate where entityName=%s" %role_name
	#该broker CPU 使用率
	elif args == "cpu_user_rate":
		#query = "select cpu_user_rate / getHostFact(numCores, 1) * 100, cpu_system_rate / getHostFact(numCores, 1) * 100 where entityName=%s" %role_name
		query = "select cpu_user_rate / getHostFact(numCores, 1.0) * 100  where entityName=%s" %role_name
	elif args == "cpu_system_rate":
		query = "select cpu_system_rate / getHostFact(numCores, 1.0) * 100  where entityName=%s" %role_name

	retry_time = 3
	while retry_time:
		api = ApiResource(cm_host, cm_port,  username, password, version=6)
		from_time = datetime.datetime.fromtimestamp(time.time() - 60)
		to_time = datetime.datetime.fromtimestamp(time.time())
		result = api.query_timeseries(query, from_time, to_time)
		ts_list = result[0]
		for ts in ts_list.timeSeries:
			if ts.data:
				for point in ts.data:
				#return "%s:\t%s" % (point.timestamp.isoformat(), point.value)
					if point.value:
						return int(point.value)
					else:
						return 0
			else:
				retry_time -= 1
				time.sleep(2)
	if retry_time == 0:
		return 0

def bluewhale_discovery():
	api = ApiResource(cm_host, cm_port,  username, password, version=3)
	data = []
	for cluster in api.get_all_clusters():
		for service in cluster.get_all_services():
			if service.name.lower() == "bluewhale": 
				data.append({"{#HDPCLUSTER_NAME}": cluster.name.strip(),"{#HDPSERVICE_NAME}":service.name.strip()})
				break
	return  json.dumps({'data':data},ensure_ascii=False,sort_keys=True,indent=4,separators=(',',':'))
		

def bluewhale_status(args):
	api = ApiResource(cm_host, cm_port,  username, password, version=6)
	from_time = datetime.datetime.fromtimestamp(time.time() - 60)
	to_time = datetime.datetime.fromtimestamp(time.time())
	#提交任务数
	if args == "job_submit":
		query = "select bluewhale_bdpweb_job_submit_num_across_bluewhale_bdpwebs"
	#执行失败任务数
	elif args == "job_fail":
		query = "select bluewhale_bdpweb_job_fail_num_across_bluewhale_bdpwebs"
	#任务调度成功任务
	elif args == "job_success":
		query = "select bluewhale_bdpweb_job_success_num"
	#任务调度运行中的任务
	elif args == "job_running":
		query = "select bluewhale_bdpweb_job_running_num"
	#重跑等待
	elif args == "job_again":
		query = "select bluewhale_bdpweb_job_again_num"
	#子任务等待
	elif args == "job_child":
		query = "select bluewhale_bdpweb_job_child_num"
	#正常任务等待
	elif args == "job_normal":
		query = "select bluewhale_bdpweb_job_normal_num"
	#yarn中正在执行的任务
	elif args == "job_running_yarn":
		query = "select bluewhale_bdpweb_job_running_yarn_num as yarn_running"

	result = api.query_timeseries(query, from_time, to_time)
	ts_list = result[0]
	for ts in ts_list.timeSeries:
		if ts.data:
			for point in ts.data:
			#return "%s:\t%s" % (point.timestamp.isoformat(), point.value)
				if point.value:
					return int(point.value)
				else:
					return 0
		else:
			return 0
				

if __name__ == "__main__":
	#自动发现
	if sys.argv[1].strip() == "discovery":
		if sys.argv[2].strip() == "hosts":
			print get_discovery("hosts")
		elif sys.argv[2].strip() == "h_childs":
			print get_discovery("h_childs")
		elif sys.argv[2].strip() == "services":
			print get_discovery("services")
		elif sys.argv[2].strip() == "s_childs":
			print get_discovery("s_childs")
		elif sys.argv[2].strip() == "s_roles":
			print get_discovery("s_roles")
		elif sys.argv[2].strip() == "k_topics":
			print kafka_topic_discovery()
		elif sys.argv[2].strip() == "k_total_broker":
			print kafka_total_broker_discovery()
		elif sys.argv[2].strip() == "k_broker":
			print kafka_broker_discovery()
		elif sys.argv[2].strip() == "bluewhale":
			print bluewhale_discovery()
	#获取状态
	elif sys.argv[1].strip() == "status":
		if sys.argv[2].strip() == "hosts":
			print get_status(cluster_name=sys.argv[3].strip(),host_name=sys.argv[4].strip(),args=sys.argv[5].strip()) 
		elif sys.argv[2].strip() == "h_childs":
			print get_status(cluster_name=sys.argv[3].strip(),host_name=sys.argv[4].strip(),h_child_name=sys.argv[5].strip()) 
		elif sys.argv[2].strip() == "services":
			print get_status(cluster_name=sys.argv[3].strip(),service_name=sys.argv[4].strip(),args=sys.argv[5].strip())
		elif sys.argv[2].strip() == "s_childs":
			print get_status(cluster_name=sys.argv[3].strip(),service_name=sys.argv[4].strip(),s_child_name=sys.argv[5].strip())
		elif sys.argv[2].strip() == "s_roles":
			print get_status(cluster_name=sys.argv[3].strip(),service_name=sys.argv[4].strip(),s_role_name=sys.argv[5].strip(),args=sys.argv[6].strip()) 
		elif sys.argv[2].strip() == "k_topics":
			print kafka_topic_status(sys.argv[3].strip(),sys.argv[4].strip())
		elif sys.argv[2].strip() == "bluewhale":
			print bluewhale_status(sys.argv[3].strip())
		elif sys.argv[2].strip() == "total_broker_status":
			print  kafka_total_broker_status(sys.argv[3].strip(),sys.argv[4].strip())
		elif sys.argv[2].strip() == "broker_status":
			print  kafka_broker_status(sys.argv[3].strip(),sys.argv[4].strip())

