#!/bin/bash

#************************************************************
# Function: 检查nginx配置文件是否配置了某参数               *
# Author: ruihua.wang@starcor.cn                            *
# DATE: 2017/11/08                                          *
#************************************************************


#nginx配置文件绝对路径
nginx_dir=$1
#检测关键字
string=$2

if [ ! -f "${nginx_dir}" ];then 
	echo 1
	exit
fi

res=$(cat ${nginx_dir}|grep -vE "^$|^#"|grep "${string}" >/dev/null 2>&1)
if [ $? -eq 0 ];then
	echo 1
else
	echo 0
fi


