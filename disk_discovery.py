#!/usr/bin/python
#coding=utf-8

#****************************************
# Function:自动获取磁盘分区             *
# Author:ruihua.wang@starcor.com        *
# Date:2017/12/19                       *
#****************************************

import os
import json

args="cat /proc/diskstats |grep -E '\ssd[a-z]\s|\sxvd[a-z]\s|\svd[a-z]\s'|awk '{print $3}'|sort|uniq 2>/dev/null"
t=os.popen(args)
 
disks=[]
 
for disk in t.readlines():
    if len(disk) != 0:
       disks.append({'{#DEVNAME}':disk.strip('\n')})
print json.dumps({'data':disks},indent=4,separators=(',',':'))
