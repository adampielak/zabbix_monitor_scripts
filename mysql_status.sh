#!/bin/sh 
export PATH=$PATH:/usr/bin:/bin:/usr/local/bin:/sbin:/usr/sbin:/usr/local/sbin:/usr/local/mysql/bin/
MYSQL_USER="root"
MYSQL_PWD="starcor"
MYSQL_HOST="127.0.0.1"
MYSQLADMIN_BIN="/usr/local/mysql/bin/mysqladmin"
MYSQL_BIN="/usr/local/mysql/bin/mysql"
ARGS=1 
if [ $# -ne "$ARGS" ];then 
echo "Please input one arguement:" 
fi 
case $1 in
    Uptime) 
        result=`${MYSQLADMIN_BIN} -u${MYSQL_USER} -p${MYSQL_PWD} -h ${MYSQL_HOST} status 2>/dev/null|cut -f2 -d":"|cut -f1 -d"T"` 
         echo $result 
            ;; 
    Com_update) 
            result=`${MYSQLADMIN_BIN} -u${MYSQL_USER} -p${MYSQL_PWD} -h ${MYSQL_HOST} extended-status 2>/dev/null |grep -w "Com_update"|cut -d"|" -f3` 
           echo $result 
            ;;
    Slow_queries) 
        result=`${MYSQLADMIN_BIN} -u${MYSQL_USER} -p${MYSQL_PWD} -h ${MYSQL_HOST} status 2>/dev/null|cut -f5 -d":"|cut -f1 -d"O"` 
                echo $result 
                ;; 
    Com_select) 
        result=`${MYSQLADMIN_BIN} -u${MYSQL_USER} -p${MYSQL_PWD} -h ${MYSQL_HOST} extended-status 2>/dev/null |grep -w "Com_select"|cut -d"|" -f3`
                echo $result 
                ;; 
    Com_rollback) 
        result=`${MYSQLADMIN_BIN} -u${MYSQL_USER} -p${MYSQL_PWD} -h ${MYSQL_HOST} extended-status 2>/dev/null|grep -w "Com_rollback"|cut -d"|" -f3` 
                echo $result 
                ;;
    Threads_connected)
        result=`${MYSQLADMIN_BIN} -u${MYSQL_USER} -p${MYSQL_PWD} -h ${MYSQL_HOST} extended-status 2>/dev/null|grep -w "Threads_connected"|cut -d"|" -f3`
                echo $result 
                ;;
    Threads_running)
        result=`${MYSQLADMIN_BIN} -u${MYSQL_USER} -p${MYSQL_PWD} -h ${MYSQL_HOST} extended-status 2>/dev/null|grep -w "Threads_running"|cut -d"|" -f3`
                echo $result 
                ;;
    max_connections)
        result=`${MYSQL_BIN} -u${MYSQL_USER} -p${MYSQL_PWD} -h ${MYSQL_HOST} -e"show global variables"  2>/dev/null|grep -w "max_connections"|awk '{print $2}'`
                echo $result 
                ;; 
        Questions) 
        result=`${MYSQLADMIN_BIN} -u${MYSQL_USER} -p${MYSQL_PWD} -h ${MYSQL_HOST} status 2>/dev/null|cut -f4 -d":"|cut -f1 -d"S"` 
                echo $result 
                ;; 
    Com_insert) 
        result=`${MYSQLADMIN_BIN} -u${MYSQL_USER} -p${MYSQL_PWD} -h ${MYSQL_HOST} extended-status 2>/dev/null|grep -w "Com_insert"|cut -d"|" -f3` 
                echo $result
                ;; 
    Com_delete)
        result=`${MYSQLADMIN_BIN} -u${MYSQL_USER} -p${MYSQL_PWD} -h ${MYSQL_HOST} extended-status 2>/dev/null|grep -w "Com_delete"|cut -d"|" -f3`
                echo $result                 
		;; 
    Com_commit) 
        result=`${MYSQLADMIN_BIN} -u${MYSQL_USER} -p${MYSQL_PWD} -h ${MYSQL_HOST} extended-status 2>/dev/null|grep -w "Com_commit"|cut -d"|" -f3`
 echo $result
                ;; 
    Bytes_sent) 
        result=`${MYSQLADMIN_BIN} -u${MYSQL_USER} -p${MYSQL_PWD} -h ${MYSQL_HOST} extended-status 2>/dev/null|grep -w "Bytes_sent" |cut -d"|" -f3`
                echo $result
               ;;
    Bytes_received) 
        result=`${MYSQLADMIN_BIN} -u${MYSQL_USER} -p${MYSQL_PWD} -h ${MYSQL_HOST} extended-status 2>/dev/null|grep -w "Bytes_received" |cut -d"|" -f3`
                echo $result 
                ;; 
    Com_begin) 
        result=`${MYSQLADMIN_BIN} -u${MYSQL_USER} -p${MYSQL_PWD} -h ${MYSQL_HOST} extended-status 2>/dev/null|grep -w "Com_begin"|cut -d"|" -f3`
                echo $result
                ;;
    	  qps) 
        Queries=`${MYSQLADMIN_BIN} -u${MYSQL_USER} -p${MYSQL_PWD} -h ${MYSQL_HOST} extended-status 2>/dev/null|grep -w "Queries"|cut -d"|" -f3`
                echo $Queries
                ;;
          tps) 
        Handler_commit=`${MYSQLADMIN_BIN} -u${MYSQL_USER} -p${MYSQL_PWD} -h ${MYSQL_HOST} extended-status 2>/dev/null|grep -w "Handler_commit"|cut -d"|" -f3`
        Handler_rollback=`${MYSQLADMIN_BIN} -u${MYSQL_USER} -p${MYSQL_PWD} -h ${MYSQL_HOST} extended-status 2>/dev/null|grep -w "Handler_rollback"|cut -d"|" -f3`
		tps=`expr $(($Handler_commit + $Handler_rollback))`
		echo $tps
                ;;

   	Slave_SQL_Running) 
		status=`${MYSQL_BIN} -h${MYSQL_HOST} -u${MYSQL_USER} -p${MYSQL_PWD}  -e "show slave status\G" 2>/dev/null |grep -w $1|awk '{if($NF=="Yes") {print 1} else {print 0}}'`
		echo ${status}
		;;
	
   	Slave_IO_Running) 
		status=`${MYSQL_BIN} -h${MYSQL_HOST} -u${MYSQL_USER} -p${MYSQL_PWD}  -e "show slave status\G" 2>/dev/null |grep -w $1|awk '{if($NF=="Yes") {print 1} else {print 0}}'`
		echo ${status}
		;;
	Replicate_Delay)
		result=`${MYSQL_BIN} -u${MYSQL_USER} -p${MYSQL_PWD} -h ${MYSQL_HOST} -e"show slave status \G"  2>/dev/null|grep Seconds_Behind_Master|cut -d: -f2 `
            	echo $result
		;;
	
	Read_Master_Log_Pos)
		result=`${MYSQL_BIN} -u${MYSQL_USER} -p${MYSQL_PWD} -h ${MYSQL_HOST} -e"show slave status \G"  2>/dev/null|grep "Read_Master_Log_Pos"|cut -d: -f2 `
            	echo $result
		;;
    	 status) 
        	result=`${MYSQLADMIN_BIN} -u${MYSQL_USER} -p${MYSQL_PWD} -h ${MYSQL_HOST}  ping 2>/dev/null| grep -c alive`
                echo $result
                ;;
    	 version) 
        	result=`${MYSQL_BIN} -V`
                echo $result
                ;;
	Check_root)
			hostname=$(hostname|tr '[a-z]' '[A-Z]'|tr '_' '%')
			host=(`${MYSQL_BIN} -h${MYSQL_HOST} -u${MYSQL_USER} -p${MYSQL_PWD} -e "select Host from mysql.user where User='root' and upper(Host) not like '${hostname}'\G" 2>/dev/null|grep -w "Host"|awk '{print $2}'`)
			len=${#host[@]}
			local_host=$(/sbin/ifconfig -a eth0|grep -w "inet addr"|awk -F ":" '{print $2}'|awk '{print $1}')
			flag=0
			for((i=0;i<${len};i++))
			do
				if [[ "${host[$i]}" != "127.0.0.1" && "${host[$i]}" != "::1" && "${host[$i]}" != "localhost" && "${host[$i]}" != "localhost.localdomain" && "${host[$i]}" != "${local_host}" ]];then
					flag=1 	
				fi
			done
			if [ ${flag} -eq 0 ];then
				echo 1
			else
				echo 0
			fi
		;;
	Check_passwd)
			passwd=(`${MYSQL_BIN} -h${MYSQL_HOST} -u${MYSQL_USER} -p${MYSQL_PWD} -e 'select Password from mysql.user where User != "hacheck"\G;' 2>/dev/null|grep -w "Password"|awk '{if ($2==""){$2="null"}print $2}'`)
			len=${#passwd[@]}
			flag=0
			for((i=0;i<${len};i++))
			do
				if [ "${passwd[$i]}" == "null" ];then
					flag=1
				fi
			done
			if [ ${flag} -eq 0 ];then
				echo 1
			else
				echo 0
			fi
			;;
	Check_db_test)
			res=$(${MYSQL_BIN} -h${MYSQL_HOST} -u${MYSQL_USER} -p${MYSQL_PWD} -e 'use test;' 2>/dev/null)
			if [ $? -eq 0 ];then
				echo 0
			else
				echo 1
			fi
			;;
	Check_user_num)
			res=$(${MYSQL_BIN} -h${MYSQL_HOST} -u${MYSQL_USER} -p${MYSQL_PWD} -e 'select count(*) from mysql.user\G;' 2>/dev/null|grep -w "count"|awk '{print $2}')
			echo $res
			;;
        *)
        echo "Usage:$0 (Uptime|Com_update|Slow_queries|Com_select|Com_rollback|Threads_connected|Threads_running|max_connections|Questions|com_insert|Com_delete|Com_commit|Bytes_sent|Bytes_received|Com_begin|qps|tps|Slave_SQL_Running|Slave_IO_Running|Replicate_Delay|Read_Master_Log_Pos|status|version|Check_root|Check_passwd|Check_db_test|Check_user_num)" 
        ;; 
esac
