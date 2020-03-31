#!/bin/bash
 
export PATH=$PATH:/usr/bin:/bin:/usr/local/bin:/sbin:/usr/sbin:/usr/local/sbin:/usr/local/mysql/bin/

item=$1
MEMCACHE_HOST=127.0.0.1
MEMCACHE_PORT=11211

(echo "stats";sleep 0.5) | telnet ${MEMCACHE_HOST} ${MEMCACHE_PORT} 2>/dev/null | grep -w "STAT $item\b" | awk '{print $3}'
