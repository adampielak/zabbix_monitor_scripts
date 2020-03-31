#!/bin/bash
 
export PATH=$PATH:/usr/bin:/bin:/usr/local/bin:/sbin:/usr/sbin:/usr/local/sbin:/usr/local/mysql/bin/

MONGO_BIN=$(which mongo)
MONGO_HOST=127.0.0.1
MONGO_PORT=27017

TYPE=$1
ITEM=$2

case $TYPE in
	opcounters)
		if [ $ITEM == "insert" ];then
			output=$(/bin/echo "db.serverStatus().opcounters" |${MONGO_BIN} ${MONGO_HOST}:${MONGO_PORT}/foo --quiet|grep -w "$ITEM"|awk -F: '{print $2}'|awk -F, '{print $1}')
			if [ "$output" == "" ];then
             			echo 0
          		else
             			echo $output
          		fi
		
		elif [ $ITEM == "query" ];then
			output=$(/bin/echo "db.serverStatus().opcounters" |${MONGO_BIN} ${MONGO_HOST}:${MONGO_PORT}/foo --quiet|grep -w "$ITEM"|awk -F: '{print $2}'|awk -F, '{print $1}')
			if [ "$output" == "" ];then
             			echo 0
          		else
             			echo $output
			fi
	
		elif [ $ITEM == "update" ];then
			output=$(/bin/echo "db.serverStatus().opcounters" |${MONGO_BIN} ${MONGO_HOST}:${MONGO_PORT}/foo --quiet|grep -w "$ITEM"|awk -F: '{print $2}'|awk -F, '{print $1}')
			if [ "$output" == "" ];then
             			echo 0
          		else
             			echo $output
			fi
	
		elif [ $ITEM == "delete" ];then
			output=$(/bin/echo "db.serverStatus().opcounters" |${MONGO_BIN} ${MONGO_HOST}:${MONGO_PORT}/foo --quiet|grep -w "$ITEM"|awk -F: '{print $2}'|awk -F, '{print $1}')
			if [ "$output" == "" ];then
             			echo 0
          		else
             			echo $output
			fi

		elif [ $ITEM == "getmore" ];then
			output=$(/bin/echo "db.serverStatus().opcounters" |${MONGO_BIN} ${MONGO_HOST}:${MONGO_PORT}/foo --quiet|grep -w "$ITEM"|awk -F: '{print $2}'|awk -F, '{print $1}')
			if [ "$output" == "" ];then
             			echo 0
          		else
             			echo $output
			fi

		elif [ $ITEM == "command" ];then
			output=$(/bin/echo "db.serverStatus().opcounters" |${MONGO_BIN} ${MONGO_HOST}:${MONGO_PORT}/foo --quiet|grep -w "$ITEM"|awk -F: '{print $2}'|awk -F, '{print $1}')
			if [ "$output" == "" ];then
             			echo 0
          		else
             			echo $output
			fi

		fi
	;;
	connections)
		 if [ $ITEM == "current" ];then
                        output=$(/bin/echo "db.serverStatus().connections" |${MONGO_BIN} ${MONGO_HOST}:${MONGO_PORT}/foo --quiet|awk -F "$ITEM" '{print $2}'|awk -F: '{print $2}'|awk -F, '{print $1}')
                        if [ "$output" == "" ];then
                                echo 0
                        else
                                echo $output
                        fi
		
		 elif [ $ITEM == "available" ];then
                        output=$(/bin/echo "db.serverStatus().connections" |${MONGO_BIN} ${MONGO_HOST}:${MONGO_PORT}/foo --quiet|awk -F "$ITEM" '{print $2}'|awk -F: '{print $2}'|awk -F, '{print $1}')
                        if [ "$output" == "" ];then
                                echo 0
                        else
                                echo $output
                        fi

                fi
	;;
	mem)
		if [ $ITEM == "resident" ];then
                        output=$(/bin/echo "db.serverStatus().mem" |${MONGO_BIN} ${MONGO_HOST}:${MONGO_PORT}/foo --quiet|grep -w "$ITEM"|awk -F: '{print $2}'|awk -F, '{print $1}')
                        if [ "$output" == "" ];then
                                echo 0
                        else
                                echo $output
                        fi
		elif [ $ITEM == "virtual" ];then
                        output=$(/bin/echo "db.serverStatus().mem" |${MONGO_BIN} ${MONGO_HOST}:${MONGO_PORT}/foo --quiet|grep -w "$ITEM"|awk -F: '{print $2}'|awk -F, '{print $1}')
                        if [ "$output" == "" ];then
                                echo 0
                        else
                                echo $output
                        fi	
		fi
	;;
	network)
		if [ $ITEM == "bytesIn" ];then
                        output=$(/bin/echo "db.serverStatus().network" |${MONGO_BIN} ${MONGO_HOST}:${MONGO_PORT}/foo --quiet|grep -w "$ITEM"|awk -F: '{print $2}'|awk -F, '{print $1}'|tr -d "NumberLong|()")
                        if [ "$output" == "" ];then
                                echo 0
                        else
                                echo $output
                        fi
		elif [ $ITEM == "bytesOut" ];then
                        output=$(/bin/echo "db.serverStatus().network" |${MONGO_BIN} ${MONGO_HOST}:${MONGO_PORT}/foo --quiet|grep -w "$ITEM"|awk -F: '{print $2}'|awk -F, '{print $1}'|tr -d "NumberLong|()")
                        if [ "$output" == "" ];then
                                echo 0
                        else
                                echo $output
                        fi	
		fi
	;;
	*)
		echo -e "\e[033mUsage: sh  $0 [opcounters|connections|mem|network] [Item] \e[0m"
	
esac
