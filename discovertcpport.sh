#!/bin/bash
#portarray=(`netstat -tnlp|egrep -i "$1"|awk {'print $4'}|awk -F':' '{if ($NF~/^[0-9]*$/) print $NF}'|sort |uniq   2>/dev/null`)
outfile="/tmp/tcp_port.txt"
SS=$(which ss)
$SS -tpnl >$outfile 2>/dev/null
portarray=(`cat $outfile|grep -vE "vsftpd|rpc"|awk '{ if ($6 != "") print $4}'|awk -F ":" '{if ($NF~/^[0-9]*$/) print $NF}'|sort|uniq 2>/dev/null`)
	if [ -n "$portarray" ];then
		length=${#portarray[@]}
	else
		portarray=(`cat $outfile|grep -vE "vsftpd|rpc"|awk '{if ($5 != "") print $3}'|awk -F ":" '{if ($NF~/^[0-9]*$/) print $NF}'|sort|uniq 2>/dev/null`)		
		length=${#portarray[@]}
	fi
	
printf "{\n"
printf  '\t'"\"data\":["
for ((i=0;i<$length;i++))
do
        printf '\n\t\t{'
	processname=$(cat $outfile |grep -w "${portarray[$i]}"|awk -F "\"" '{print $2}'|sort|uniq)
	if [ -n "$processname" ];then
        	printf "\"{#TCP_PORT}\":\"${portarray[$i]}\",\"{#PROCESS_NAME}\":\"${processname}\"}"
	fi
        if [ $i -lt $[$length-1] ];then
                printf ','
        fi
done
printf  "\n\t]\n"
printf "}\n"
