#!/bin/bash

#************************************
# Function:ZooKeeper监控脚本        *
# Author:ruihua.wang@starcor.cn     *
# DATE:2017/07/24                   *
#************************************ 

ZOOKEEPER_HOST="127.0.0.1"
ZOOKEEPER_PORT="2181"
item=$1

if [ "${item}" == "status" ];then
	result=$(echo ruok|nc ${ZOOKEEPER_HOST} ${ZOOKEEPER_PORT})
	if [ "${result}" == "imok" ];then
		echo 1
	else
		echo 0		
	fi
else
	echo mntr|nc ${ZOOKEEPER_HOST} ${ZOOKEEPER_PORT} | grep -w "${item}" |awk '{print $2}'
fi
