#!/bin/bash

#************************************
# Function:iptables状态监控脚本     *
# Author:ruihua.wang@starcor.cn     *
# DATE:2017/10/26                   *
#************************************

IPTABLES_BIN=$(which iptables)
lines=$(${IPTABLES_BIN} -L -n |wc -l)
args=$1

if [ ${lines} -gt ${args} ];then
	echo 1
else
	echo 0
fi

