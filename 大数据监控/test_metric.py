# !/usr/bin/env python
# -*- coding: utf-8 -*-

from cm_api.api_client import ApiResource
import load_config
import sys, os
import datetime, time
reload(sys)
sys.setdefaultencoding('utf-8')

bin_path = sys.path[0]
# conf_path = bin_path + '/../conf'
# conf_file = conf_path + '/add_platform.ini'
# starcor_conf = load_config.SetupConf('STARCOR')
# 配置CM基本信息
cm_host = '192.168.95.235'
# cm_host = '47.96.137.65'
port = '7180'
userName = 'check'
passWD = 'Cloudera!23'
duration = 360
# userName = 'admin'
# passWD = 'admin'

api = ApiResource(cm_host, port, username=userName, password=passWD, version=5)

cluster = api.get_all_clusters()[0]
# print api.get_all_clusters().init

host_names = {}
host_IPs = {}
for host in api.get_all_hosts():
    host_names[host.hostId] = host.hostname
    host_IPs[host.hostId] = host.ipAddress

for cluster in api.get_all_clusters():
    print cluster.name

    for service in cluster.get_all_services():
        if service.name == 'bluewhale':
            print service.name
        else:
            continue
        # for role in service.get_all_roles():
        #     print role
        # 已用CPU内核
        # query = 'select cpu_system_rate + cpu_user_rate where category=ROLE and serviceName=' + service.name
        # hdfs容量
        # query = 'select dfs_capacity, dfs_capacity_used, dfs_capacity_used_non_hdfs where entityName=' + service.name
        # 任务调度所有任务
        query = 'select bluewhale_bdpweb_job_new_num_across_bluewhale_bdpwebs where category=SERVICE and serviceName=' + service.name
        # 任务调度成功任务
        query = 'select bluewhale_bdpweb_job_success_num_across_bluewhale_bdpwebs where category=SERVICE and serviceName=' + service.name
        # 任务调度运行中的任务
        query = 'select bluewhale_bdpweb_job_running_num_across_bluewhale_bdpwebs where category=SERVICE and serviceName=' + service.name
        # 重跑等待
        query = 'select bluewhale_bdpweb_job_again_num_across_bluewhale_bdpwebs where category=SERVICE and serviceName=' + service.name
        # 子任务等待
        query = 'select bluewhale_bdpweb_job_child_num_across_bluewhale_bdpwebs where category=SERVICE and serviceName=' + service.name
        # 正常任务等待
        query = 'select bluewhale_bdpweb_job_normal_num_across_bluewhale_bdpwebs where category=SERVICE and serviceName=' + service.name
        # yarn中正在执行的任务
        query = 'select bluewhale_bdpweb_job_running_yarn_num where category=SERVICE and serviceName=' + service.name
        # yarn中正在待定的任务
        query = 'select bluewhale_bdpweb_job_accept_yarn_num where category=SERVICE and serviceName=' + service.name

        query = 'select bluewhale_bdpweb_job_submit_num_across_bluewhale_bdpwebs, ' + \
                'bluewhale_bdpweb_job_success_num_across_bluewhale_bdpwebs, ' + \
                'bluewhale_bdpweb_job_running_num_across_bluewhale_bdpwebs, ' + \
                'bluewhale_bdpweb_job_again_num_across_bluewhale_bdpwebs, ' + \
                'bluewhale_bdpweb_job_child_num_across_bluewhale_bdpwebs, ' + \
                'bluewhale_bdpweb_job_normal_num_across_bluewhale_bdpwebs ' + \
                'where category=SERVICE and serviceName=' + service.name
        query = 'select bluewhale_bdpweb_job_running_yarn_num, ' + \
                'bluewhale_bdpweb_job_accept_yarn_num '
        query = 'select total_kafka_bytes_fetched_1min_rate_across_kafka_broker_topics where kafkaTopicName = N603_A_1_gxgd'
                 # 'bluewhale_bdpweb_job_accept_yarn_num ' + \
                 # 'where category=SERVICE and serviceName=' + service.name
        from_time = datetime.datetime.fromtimestamp(time.time() - duration)
        to_time = datetime.datetime.fromtimestamp(time.time())
        result = api.query_timeseries(query, from_time, to_time)
        # result = api.query_timeseries(query, from_time, to_time)
        ts_list = result[0]
        metrices_list = []
        mdist = {}
        for ts in ts_list.timeSeries:
            for point in ts.data:
                # print dir(ts.metadata)
                # mdist[ts.metadata.metricName] = point.value
                metrices_list.append([ts.metadata.entityName, ts.metadata.metricName, \
                                      point.timestamp.isoformat(), point.value])
        # print metrices_list
        for line in metrices_list:
            print line
        # for key, value in mdist.items():
        #     print key, value
        # break
