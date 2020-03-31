#!/bin/bash

#****************************************
# Function:监控磁盘IO相关信息           *
# Author:ruihua.wang@starcor.com        *
# Date:2017/12/19                       *
#****************************************

Device=$1
ITEM=$2

function disk_status_v6()
{
	case $ITEM in
	         rrqm/s)
	            iostat -dxkt |grep "\b$Device\b"|tail -1|awk '{print $2}'
	            ;;
	         wrqm/s)
	            iostat -dxkt |grep "\b$Device\b"|tail -1|awk '{print $3}'
	            ;;
	          r/s)
	            iostat -dxkt |grep "\b$Device\b"|tail -1|awk '{print $4}'
	            ;;
	          w/s)
	            iostat -dxkt |grep "\b$Device\b" |tail -1|awk '{print $5}'
	            ;;
	        rkB/s)
	            iostat -dxkt |grep "\b$Device\b" |tail -1|awk '{print $6}'
	            ;;
	        wkB/s)
	            iostat -dxkt |grep "\b$Device\b" |tail -1|awk '{print $7}'
	            ;;
	        avgrq-sz)
	            iostat -dxkt |grep "\b$Device\b" |tail -1|awk '{print $8}'
	            ;;
	        avgqu-sz)
	            iostat -dxkt |grep "\b$Device\b" |tail -1|awk '{print $9}'
	            ;;
	        await)
	            iostat -dxkt |grep "\b$Device\b" |tail -1|awk '{print $10}'
	            ;;
	        svctm)
	            iostat -dxkt |grep "\b$Device\b" |tail -1|awk '{print $11}'
	            ;;
	         util)
	            iostat -dxkt |grep "\b$Device\b" |tail -1|awk '{print $12}'
	            ;;
		   *)
		    echo 0 
		    ;;
	esac
}

function disk_status_v7()
{
	case $ITEM in
	         rrqm/s)
	            iostat -dxkt |grep "\b$Device\b"|tail -1|awk '{print $2}'
	            ;;
	         wrqm/s)
	            iostat -dxkt |grep "\b$Device\b"|tail -1|awk '{print $3}'
	            ;;
	          r/s)
	            iostat -dxkt |grep "\b$Device\b"|tail -1|awk '{print $4}'
	            ;;
	          w/s)
	            iostat -dxkt |grep "\b$Device\b" |tail -1|awk '{print $5}'
	            ;;
	        rkB/s)
	            iostat -dxkt |grep "\b$Device\b" |tail -1|awk '{print $6}'
	            ;;
	        wkB/s)
	            iostat -dxkt |grep "\b$Device\b" |tail -1|awk '{print $7}'
	            ;;
	        avgrq-sz)
	            iostat -dxkt |grep "\b$Device\b" |tail -1|awk '{print $8}'
	            ;;
	        avgqu-sz)
	            iostat -dxkt |grep "\b$Device\b" |tail -1|awk '{print $9}'
	            ;;
	        await)
	            iostat -dxkt |grep "\b$Device\b" |tail -1|awk '{print $10}'
	            ;;
	        r_await)
	            iostat -dxkt |grep "\b$Device\b" |tail -1|awk '{print $11}'
	            ;;
	        w_await)
	            iostat -dxkt |grep "\b$Device\b" |tail -1|awk '{print $12}'
	            ;;
	        svctm)
	            iostat -dxkt |grep "\b$Device\b" |tail -1|awk '{print $13}'
	            ;;
	         util)
	            iostat -dxkt |grep "\b$Device\b" |tail -1|awk '{print $14}'
	            ;;
		   *)
		    echo 0 
		    ;;
	esac
}
num=$(iostat -dxkt|grep "\b$Device\b"|tail -1|awk '{print NF}')
if [ "${num}" = "12" ];then
	disk_status_v6 
elif [ "${num}" = "14" ];then
	disk_status_v7 
fi
