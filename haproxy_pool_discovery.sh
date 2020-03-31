#!/bin/bash

#******************************************
#Funcition: 监控haproxy相关指标           *
#Author: ruihua.wang@starcor.cn           *
#Date: 2017/06/22                         *
#******************************************

export PATH=$PATH:/usr/bin:/bin:/usr/local/bin:/sbin:/usr/sbin:/usr/local/sbin:/usr/local/mysql/bin/
SOCAT=$(which socat)
portarray=(`echo "show stat"|$SOCAT /usr/local/haproxy/haproxy.sock stdio|grep -vE '^$|^#'|egrep -v "admin|FRONTEND|BACKEND"|awk -F ',' '{print $1":"$2}'`)
length=${#portarray[@]}
	
printf "{\n"
printf  '\t'"\"data\":["
for ((i=0;i<$length;i++))
do
        printf '\n\t\t{'
        	printf "\"{#POOL_NAME}\":\"${portarray[$i]}\"}"
        if [ $i -lt $[$length-1] ];then
                printf ','
        fi
done
printf  "\n\t]\n"
printf "}\n"
