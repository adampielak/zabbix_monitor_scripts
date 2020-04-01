#!/bin/bash

#***********************************
#Function: 监控系统错误日志        *
#Author:ruihua.wang@starcor.com    *
#Date:2017/11/08                   *
#***********************************

args=$1
DMESG_BIN=$(which dmesg)

if [ $# -ne 1 ];then 
	echo "Please input one arguement:" 
	echo "./$0 'args'" 
	exit
fi 

res=$(${DMESG_BIN} |grep -i "${args}" 2>/dev/null|head -1)
if [ "${res}" = "" ];then
	echo "ok"
else
	echo ${res}
fi
${DMESG_BIN} -c >/dev/null 2>&1
