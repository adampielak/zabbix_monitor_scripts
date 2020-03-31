#!/bin/bash

#***********************************
#Author:ruihua.wang@starcor.com    *
#Function:统计异常请求日志         *
#Date:2017/10/28                   *
#***********************************

log_file="/data/logs/illegal_access.log"
arg=$1

if [ -f ${log_file} ];then
	log_line=$(cat ${log_file}|grep -vE "^$"|grep -vw "get_epg_status.php"|awk -F "\"" '{if ($14 == '${arg}')print $14}'|wc -l)
	echo ${log_line}
else
	echo 0
fi
