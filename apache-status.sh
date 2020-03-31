#!/bin/bash
export PATH=$PATH:/usr/bin:/bin:/usr/local/bin:/sbin:/usr/sbin:/usr/local/sbin:/usr/local/mysql/bin/
CURL=`which curl`

if [[ "$1" = "Workers" ]]; then
	$CURL -s http://127.0.0.1/server-status?auto | grep Score | grep -o "\." | wc -l
else
	$CURL -s http://127.0.0.1/server-status?auto | grep $1 | awk -F ":" '{print $2}'
fi
