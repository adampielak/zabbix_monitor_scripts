#!/bin/bash
#Author: ruihua.wang@starcor.cn
#Function: monitor hardware health status
#Date: 2017/4/28

export PATH=$PATH:/usr/bin:/bin:/usr/local/bin:/sbin:/usr/sbin:/usr/local/sbin:/usr/local/mysql/bin/
OMREPORT=$(which omreport)
type=$1

case $type in
	#CMOS电池状态
	hardware_battery)
		${OMREPORT} chassis batteries|awk '/^Status/{if($NF=="Ok") {print 1} else {print 0}}'
	;;
	#风扇状态
	hardware_fan_health)
		awk -v hardware_fan_number=`${OMREPORT} chassis fans|grep -c "^Index"` -v hardware_fan=`${OMREPORT} chassis fans|awk '/^Status/{if($NF=="Ok") count+=1}END{print count}'` 'BEGIN{if(hardware_fan_number==hardware_fan) {print 1} else {print 0}}'
	;;
	#内存状态
	hardware_memory_health)
		awk -v hardware_memory=`${OMREPORT} chassis memory|awk '/^Health/{print $NF}'` 'BEGIN{if(hardware_memory=="Ok") {print 1} else {print 0}}'
	;;
	#网卡状态
	hardware_nic_health)
		awk -v hardware_nic_number=`${OMREPORT} chassis nics |grep -c "Interface Name"` -v hardware_nic=`${OMREPORT} chassis nics |awk '/^Connection Status/{print $NF}'|wc -l` 'BEGIN{if(hardware_nic_number==hardware_nic) {print 1} else {print 0}}'
	;;
	#CPU状态
	hardware_cpu)
		${OMREPORT} chassis processors|awk '/^Health/{if($NF=="Ok") {print 1} else {print 0}}'
	;;
	#电源状态
	hardware_power_health)
		awk -v hardware_power_number=`${OMREPORT} chassis pwrsupplies|grep -c "Index"` -v hardware_power=`${OMREPORT} chassis pwrsupplies|awk '/^Status/{if($NF=="Ok") count+=1}END{print count}'` 'BEGIN{if(hardware_power_number==hardware_power) {print 1} else {print 0}}'
	;;
	#温度状态
	hardware_temp)
		${OMREPORT} chassis temps|awk '/^Status/{if($NF=="Ok") {print 1} else {print 0}}'|head -n 1
	;;
	#物理磁盘状态
	hardware_physics_health)
		awk -v hardware_physics_disk_number=`${OMREPORT} storage pdisk controller=0|grep -c "^ID"` -v hardware_physics_disk=`${OMREPORT} storage pdisk controller=0|awk '/^Status/{if($NF=="Ok") count+=1}END{print count}'` 'BEGIN{if(hardware_physics_disk_number==hardware_physics_disk) {print 1} else {print 0}}'
	;;
	#虚拟磁盘状态
	hardware_virtual_health)
		awk -v hardware_virtual_disk_number=`${OMREPORT} storage vdisk controller=0|grep -c "^ID"` -v hardware_virtual_disk=`${OMREPORT} storage vdisk controller=0|awk '/^Status/{if($NF=="Ok") count+=1}END{print count}'` 'BEGIN{if(hardware_virtual_disk_number==hardware_virtual_disk) {print 1} else {print 0}}'
	;;
	*)
		echo -e "\e[033mUsage: sh  $0 [hardware_battery|hardware_fan_health|hardware_memory_health|hardware_nic_health|hardware_cpu|hardware_power_health|hardware_temp|hardware_physics_health|hardware_virtual_health]\e[0m"
    ;;
esac
