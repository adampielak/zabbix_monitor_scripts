#!/bin/bash

zabbix_conf="/usr/local/zabbix/etc/zabbix_agentd.conf"
starcor_conf="/usr/local/zabbix/etc/zabbix_agentd.conf.d/starcor.conf"
script_dir="/usr/local/zabbix/etc/scripts/"

#修改zabbix_agentd.conf文件
function change_agentd_conf()
{
	if [ ! -f "${zabbix_conf}" ];then
		echo "部署失败，${zabbix_conf} 不存在!!"
		exit
	else
		#a=$(cat /usr/local/zabbix/etc/zabbix_agentd.conf|grep -vE "^#"|grep "AllowRoot=1")
		#if [ $? != 0 ];then
		#	b=$(cat /usr/local/zabbix/etc/zabbix_agentd.conf|grep -vE "^#"|grep "AllowRoot=0")
		#	if [ $? == 0 ];then
		#		sed -i 's/AllowRoot=0/AllowRoot=1/g' ${zabbix_conf}
		#	else
		#		echo "AllowRoot=1" >> ${zabbix_conf}
		#		
		#	fi
		#fi
		c=$(cat /usr/local/zabbix/etc/zabbix_agentd.conf|grep -vE "^#"|grep "UnsafeUserParameters=1")
		if [ $? != 0 ];then
			d=$(cat /usr/local/zabbix/etc/zabbix_agentd.conf|grep -vE "^#"|grep "UnsafeUserParameters=0")
			if [ $? == 0 ];then
				sed -i 's/UnsafeUserParameters=0/UnsafeUserParameters=1/g' ${zabbix_conf}
			else
				echo "UnsafeUserParameters=1" >> ${zabbix_conf}
				
			fi
		fi
	fi
}

function change_starcor_conf()
{
	if [ ! -f "${starcor_conf}" ];then
		echo "部署失败， ${starcor_conf} 不存在!!"
		exit
	else
		a=$(cat ${starcor_conf}|grep "abnormal.login")
		if [ $? != 0 ];then
			cat >> ${starcor_conf} <<EOF
#异常登录监控
UserParameter=abnormal.login,/usr/local/zabbix/etc/scripts/abnormal_login.sh
EOF
		else
			echo "${starcor_conf}中已存在abnormal.login "
		fi

		b=$(cat ${starcor_conf}|grep "dmesg.status")
		if [ $? != 0 ];then
			cat >> ${starcor_conf} <<EOF
#系统dmesg状态监控
UserParameter=dmesg.status[*],/usr/local/zabbix/etc/scripts/dmesg_status.sh "\$1"
EOF
		else
			echo "${starcor_conf}中已存在dmesg.status"
		fi

		c=$(cat ${starcor_conf}|grep -E "iptables.discovery|iptables.status")
		if [ $? != 0 ];then
			cat >> ${starcor_conf} <<EOF
#防火墙状态监控
UserParameter=iptables.discovery,/usr/local/zabbix/etc/scripts/iptables_status.py "discovery"
UserParameter=iptables.status[*],/usr/local/zabbix/etc/scripts/iptables_status.py "\$1" "\$2"
EOF
		else
			echo "${starcor_conf}中已存在iptable配置"
		fi

		d=$(cat ${starcor_conf}|grep -E "process.bindip.discovery|process.bindip.status")
		if [ $? != 0 ];then
			cat >> ${starcor_conf} <<EOF
#监控进程是否绑定了外网IP
UserParameter=process.bindip.discovery,/usr/local/zabbix/etc/scripts/process_bindip_status.py "discovery"
UserParameter=process.bindip.status[*],/usr/local/zabbix/etc/scripts/process_bindip_status.py "\$1" 
EOF
		else
			echo "${starcor_conf}中已存在process.bindip配置"
		fi

		e=$(cat ${starcor_conf}|grep  "crontab.status")
		if [ $? != 0 ];then
			cat >> ${starcor_conf} <<EOF
#监控服务器是否有异常定时器
UserParameter=crontab.status[*],/usr/local/zabbix/etc/scripts/crontab_status.py "\$1" 
EOF
		else
			echo "${starcor_conf}中已存在crontab.status配置"
		fi

		f=$(cat ${starcor_conf}|grep  "check.code")
		if [ $? != 0 ];then
			cat >> ${starcor_conf} <<EOF
#监控代码中是否存在异常目录
UserParameter=check.code[*],/usr/local/zabbix/etc/scripts/check_code.py "\$1" "\$2" "\$3"
EOF
		else
			echo "${starcor_conf}中已存在check.code配置"
		fi

		g=$(cat ${starcor_conf}|grep  "check.nginx")
		if [ $? != 0 ];then
			cat >> ${starcor_conf} <<EOF
#监控nginx配置文件中是否配置了指定内容
UserParameter=check.nginx[*],/usr/local/zabbix/etc/scripts/check_nginx.sh "\$1" "\$2"
EOF
		else
			echo "${starcor_conf}中已存在check.nginx配置"
		fi

	fi
}

function copy_script()
{
	if [ ! -d "${script_dir}" ];then
		echo "${script_dir} 不存在!!"
	else
		echo "正在拷贝脚本到/usr/local/zabbix/etc/scripts/下"
		cp safe_scripts/* ${script_dir} -rf 
		chown zabbix.zabbix -R /usr/local/zabbix/etc/scripts/
		chmod 755 -R /usr/local/zabbix/etc/scripts/
		chmod 644 /var/log/btmp
		chmod a+s /bin/dmesg
		chmod a+s /sbin/iptables
		chmod a+s /bin/netstat
		echo -e 'Defaults:zabbix !requiretty \nzabbix ALL=(root) NOPASSWD: /usr/bin/crontab' >/etc/sudoers.d/zabbix 
		chmod 0400 /etc/sudoers.d/zabbix
		/etc/init.d/zabbix_agentd restart
	fi

}

change_agentd_conf
change_starcor_conf
copy_script
res=$(ps -ef |grep "zabbix_agentd"|grep -v "grep")
if [ $? == 0 ];then
	echo "zabbix重启成功，部署完成!!!"
else
	echo "zabbix重启失败，部署失败!!!"
fi
