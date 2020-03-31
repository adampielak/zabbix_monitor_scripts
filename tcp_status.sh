#!/bin/bash
#tcp status

type=$1
tmp_file=/proc/net/tcp
case $type in
    ALL)
        output=$(cat $tmp_file|wc -l)
        if [ "$output" == "" ];then
            echo 0
        else
            echo $output
        fi
        ;;
    ERROR_STATUS)
        output=$(cat $tmp_file|awk '{print $4}'|grep -w "00"|wc -l)
        if [ "$output" == "" ];then
            echo 0
        else
            echo $output
        fi
        ;;
    TCP_ESTABLISHED)
        output=$(cat $tmp_file|awk '{print $4}'|grep -w "01"|wc -l)
        if [ "$output" == "" ];then
            echo 0
        else
            echo $output
        fi
        ;;
    TCP_SYN_SENT)
	output=$(cat $tmp_file|awk '{print $4}'|grep -w "02"|wc -l)
          if [ "$output" == "" ];then
             echo 0
          else
             echo $output
          fi
        ;;
    TCP_SYN_RECV)
	output=$(cat $tmp_file|awk '{print $4}'|grep -w "03"|wc -l)
          if [ "$output" == "" ];then
             echo 0
          else
             echo $output
          fi
        ;;
    TCP_FIN_WAIT1)
	output=$(cat $tmp_file|awk '{print $4}'|grep -w "04"|wc -l)
          if [ "$output" == "" ];then
             echo 0
          else
             echo $output
          fi
        ;;
    TCP_FIN_WAIT2)
	output=$(cat $tmp_file|awk '{print $4}'|grep -w "05"|wc -l)
          if [ "$output" == "" ];then
             echo 0
          else
             echo $output
          fi
        ;;
    TCP_TIME_WAIT)
	output=$(cat $tmp_file|awk '{print $4}'|grep -w "06"|wc -l)
          if [ "$output" == "" ];then
             echo 0
          else
             echo $output
          fi
        ;;
    TCP_CLOSE)
	output=$(cat $tmp_file|awk '{print $4}'|grep -w "07"|wc -l)
          if [ "$output" == "" ];then
             echo 0
          else
             echo $output
          fi
        ;;
    TCP_CLOSE_WAIT)
	output=$(cat $tmp_file|awk '{print $4}'|grep -w "08"|wc -l)
          if [ "$output" == "" ];then
             echo 0
          else
             echo $output
          fi
         ;;
    TCP_LAST_ACK)
	output=$(cat $tmp_file|awk '{print $4}'|grep -w "09"|wc -l)
          if [ "$output" == "" ];then
             echo 0
          else
             echo $output
          fi
         ;;
    TCP_LISTEN)
	output=$(cat $tmp_file|awk '{print $4}'|grep -w "0A"|wc -l)
          if [ "$output" == "" ];then
             echo 0
          else
             echo $output
          fi
         ;;
    TCP_CLOSING)
	output=$(cat $tmp_file|awk '{print $4}'|grep -w "0B"|wc -l)
          if [ "$output" == "" ];then
             echo 0
          else
             echo $output
          fi
         ;;

         *)
          echo -e "\e[033mUsage: sh  $0 [ALL|ERROR_STATUS|TCP_ESTABLISHED|TCP_SYN_SENT|TCP_SYN_RECV|TCP_FIN_WAIT1|TCP_FIN_WAIT2|TCP_TIME_WAIT|TCP_CLOSE|TCP_CLOSE_WAIT|TCP_LAST_ACK|TCP_LISTEN|TCP_CLOSING]\e[0m"
	;;
esac
