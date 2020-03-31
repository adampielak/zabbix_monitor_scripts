#!/bin/bash

#************************************
# Function:获取网卡名称和对应IP     *
# Author:ruihua.wang@starcor.cn     *
# DATE:2017/10/26                   *
#************************************

portarray=(`cat /proc/net/dev|grep -vE "Inter|face|lo"|awk -F ":" '{print $1}'|tr -d " "  2>/dev/null`)
length=${#portarray[@]}
printf "{\n"
printf  '\t'"\"data\":["
for ((i=0;i<$length;i++))
do
        printf '\n\t\t{'
    	processname=$(ip addr show|grep "brd"|grep 'global' |grep -w "${portarray[$i]}"|grep -v "${portarray[$i]}:"|awk '{print $2}')
        printf "\"{#IFNAME}\":\"${portarray[$i]}\",\"{#ADDR}\":\"${processname}\"}"
        if [ $i -lt $[$length-1] ];then
                printf ','
        fi
done
printf  "\n\t]\n"
printf "}\n"
