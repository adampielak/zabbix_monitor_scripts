#!/bin/bash

#***********************************
#Author:ruihua.wang@starcor.com    *
#Function: 监控系统异常登录        *
#Date:2017/11/08                   *
#***********************************

LASTB_BIN=$(which lastb)
res=$(${LASTB_BIN} |wc -l 2>/dev/null)
echo ${res}

