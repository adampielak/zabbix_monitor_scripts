#!/bin/bash

#******************************************
#Funcition: 监控haproxy相关指标           *
#Author: ruihua.wang@starcor.cn           *
#Date: 2017/06/22                         *
#******************************************

export PATH=$PATH:/usr/bin:/bin:/usr/local/bin:/sbin:/usr/sbin:/usr/local/sbin:/usr/local/mysql/bin/
SOCAT=`which socat`
haproxy_socket="/usr/local/haproxy/haproxy.sock"
 
metric=$1
info_file=/tmp/haproxy_info.csv
echo "show info"| $SOCAT   $haproxy_socket  stdio > $info_file
grep $metric $info_file|awk '{print $2}'
