#!/bin/bash

#************************************
# Function:Redis集群监控脚本            *
# Author:ruihua.wang@starcor.cn     *
# DATE:2017/12/18                   *
#************************************

export PATH=$PATH:/usr/bin:/bin:/usr/local/bin:/sbin:/usr/sbin:/usr/local/sbin:/usr/local/mysql/bin/

REDIS_BIN=$(which redis-cli)
#redis bind的ip
REDIS_HOST="127.0.0.1"
#redis连接密码，若配置密码则填写对应密码，若无则不填写
REDIS_PASSWD=""

REDIS_PORT=$1
item=$2

if [ -z "$REDIS_PASSWD" ];then
	if [ "$item" == "all_keys" ];then
		${REDIS_BIN} -h ${REDIS_HOST} -p ${REDIS_PORT} -c info 2>/dev/null |grep "keys="|awk -F "keys=" '{print $2}'|awk -F ',' '{sum+=$1} END {print sum}'
	elif [ "$item" == "cpu_usage" ];then
		/bin/ps aux|grep -w "cluster"|grep -w "${REDIS_PORT}"|grep -v "grep"|awk '{print $3}'
	else
		${REDIS_BIN} -h ${REDIS_HOST}  -p ${REDIS_PORT} -c info 2>/dev/null |grep -w ${item}|cut -d : -f2
	fi
else
	if [ "$item" == "all_keys" ];then
		${REDIS_BIN} -h ${REDIS_HOST} -p ${REDIS_PORT} -a ${REDIS_PASSWD} -c info 2>/dev/null|grep "keys=" |awk -F "keys=" '{print $2}'| awk -F ',' '{sum+=$1} END {print sum}'
	elif [ "$item" == "cpu_usage" ];then
		/bin/ps aux|grep -w "cluster"|grep -w "${REDIS_PORT}"|grep -v "grep"|awk '{print $3}'
	else
		${REDIS_BIN} -h ${REDIS_HOST}  -p ${REDIS_PORT} -a ${REDIS_PASSWD} -c info 2>/dev/null |grep -w ${item}|cut -d : -f2
	fi
fi
