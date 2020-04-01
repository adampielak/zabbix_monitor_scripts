#!/usr/bin/python
#coding=utf-8

import commands
import sys
import os

MYSQL_USER="root"
MYSQL_PWD="starcor"
MYSQL_HOST="127.0.0.1"
MYSQL_NAME="zabbix"
MYSQL_BIN="/usr/local/mysql/bin/mysql"
backup_dir="/data/mysql"

#需要备份的表
#table_list = ['history','history_str','history_log','history_uint','history_text','trends','trends_uint']
table_list = ['history','history_str','history_log','history_uint','history_text']

def command(arg1):
	(status, output) = commands.getstatusoutput(arg1)
	return status,output

def create_tmp_table(tmp_table_name, group_name):
	if not os.path.exists(backup_dir):
        	os.makedirs(backup_dir)

	#创建临时表存储itemid等数据
	res = command(""" %s -u"%s" -p"%s" -h"%s" "%s" -e 'drop table if exists tmp_%s;create table tmp_%s (select d.hostid,c.host,e.ip,d.itemid,d.key_,d.value_type  from hosts_groups a, groups b ,hosts c, items d, interface e where a.groupid=b.groupid and  b.name="%s" and a.hostid=c.hostid and c.status <> 3 and c.hostid=d.hostid and c.hostid=e.hostid);' 2>/dev/null """ %(MYSQL_BIN, MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_NAME, tmp_table_name, tmp_table_name, group_name))
	if res[0] == 0:
		print 'create tmp table:%s succeed!!'%tmp_table_name
	else:
		print 'create tmp table:%s Failed!!'%tmp_table_name

	#备份数据
	for i in table_list:
		res = command(""" %s -u"%s" -p"%s" -h"%s" "%s" -e 'select * from %s where itemid in (select itemid from tmp_%s) into outfile  "%s/%s.txt";' """ %(MYSQL_BIN, MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_NAME, i, tmp_table_name, backup_dir, i))
		if res[0] == 0:
			print 'backup table:%s succeed!!'%i
		else:
			print 'backup table:%s Failed!! reason: %s'%(i,res[1].strip())
	

	
def update_items(tmp_table_name,group_name):
	#导入数据
	for i in table_list:
		if os.path.getsize("%s/%s.txt" %(backup_dir,i)):
			res = command(""" %s -u"%s" -p"%s" -h"%s" "%s" -e 'load data infile "%s/%s.txt" into table %s;'  """ %(MYSQL_BIN, MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_NAME, backup_dir, i, i))
			if res[0] == 0:
				print 'load data table:%s succeed!!'%i
			else:
				print 'load data table:%s Failed!!, reason: %s '%(i,res[1].strip())

	#update history
	res = command(""" %s -u"%s" -p"%s" -h"%s" "%s" -e 'update  hosts_groups a, groups b ,hosts c, items d, interface e ,tmp_%s f,history g set g.itemid=d.itemid where a.groupid=b.groupid and  b.name="%s" and a.hostid=c.hostid and c.status <> 3 and c.hostid=d.hostid and c.hostid=e.hostid and e.ip=f.ip and d.value_type=0 and f.key_=d.key_ and f.itemid=g.itemid' 2>/dev/null """ %(MYSQL_BIN, MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_NAME, tmp_table_name, group_name))
	if res[0] == 0:
		print 'update history succeed!!'
	else:
		print 'update history failed!!'

	#update history_str
	res = command(""" %s -u"%s" -p"%s" -h"%s" "%s" -e 'update  hosts_groups a, groups b ,hosts c, items d, interface e ,tmp_%s f,history_str g set g.itemid=d.itemid where a.groupid=b.groupid and  b.name="%s" and a.hostid=c.hostid and c.status <> 3 and c.hostid=d.hostid and c.hostid=e.hostid and e.ip=f.ip and d.value_type=1 and f.key_=d.key_ and f.itemid=g.itemid' 2>/dev/null """ %(MYSQL_BIN, MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_NAME, tmp_table_name, group_name))
	if res[0] == 0:
		print 'update history_str succeed!!'
	else:
		print 'update history_str failed!!'

	#update history_log
	res = command(""" %s -u"%s" -p"%s" -h"%s" "%s" -e 'update  hosts_groups a, groups b ,hosts c, items d, interface e ,tmp_%s f,history_log g set g.itemid=d.itemid where a.groupid=b.groupid and  b.name="%s" and a.hostid=c.hostid and c.status <> 3 and c.hostid=d.hostid and c.hostid=e.hostid and e.ip=f.ip and d.value_type=2 and f.key_=d.key_ and f.itemid=g.itemid' 2>/dev/null """ %(MYSQL_BIN, MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_NAME, tmp_table_name, group_name))
	if res[0] == 0:
		print 'update history_log succeed!!'
	else:
		print 'update history_log failed!!'

	#update history_uint
	res = command(""" %s -u"%s" -p"%s" -h"%s" "%s" -e 'update  hosts_groups a, groups b ,hosts c, items d, interface e ,tmp_%s f,history_uint g set g.itemid=d.itemid where a.groupid=b.groupid and  b.name="%s" and a.hostid=c.hostid and c.status <> 3 and c.hostid=d.hostid and c.hostid=e.hostid and e.ip=f.ip and d.value_type=3 and f.key_=d.key_ and f.itemid=g.itemid' 2>/dev/null """ %(MYSQL_BIN, MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_NAME, tmp_table_name, group_name))
	if res[0] == 0:
		print 'update history_uint succeed!!'
	else:
		print 'update history_uint failed!!'

	#update history_text
	res = command(""" %s -u"%s" -p"%s" -h"%s" "%s" -e 'update  hosts_groups a, groups b ,hosts c, items d, interface e ,tmp_%s f,history_text g set g.itemid=d.itemid where a.groupid=b.groupid and  b.name="%s" and a.hostid=c.hostid and c.status <> 3 and c.hostid=d.hostid and c.hostid=e.hostid and e.ip=f.ip and d.value_type=4 and f.key_=d.key_ and f.itemid=g.itemid' 2>/dev/null """ %(MYSQL_BIN, MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_NAME, tmp_table_name, group_name))
	if res[0] == 0:
		print 'update history_text succeed!!'
	else:
		print 'update history_text failed!!'

	#update trends
	res = command(""" %s -u"%s" -p"%s" -h"%s" "%s" -e 'update  hosts_groups a, groups b ,hosts c, items d, interface e ,tmp_%s f,trends g set g.itemid=d.itemid where a.groupid=b.groupid and  b.name="%s" and a.hostid=c.hostid and c.status <> 3 and c.hostid=d.hostid and c.hostid=e.hostid and e.ip=f.ip and f.key_=d.key_ and f.itemid=g.itemid' 2>/dev/null """ %(MYSQL_BIN, MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_NAME, tmp_table_name, group_name))
	if res[0] == 0:
		print 'update trends succeed!!'
	else:
		print 'update trends failed!!'
	
	#update trends_uint
	res = command(""" %s -u"%s" -p"%s" -h"%s" "%s" -e 'update  hosts_groups a, groups b ,hosts c, items d, interface e ,tmp_%s f,trends_uint g set g.itemid=d.itemid where a.groupid=b.groupid and  b.name="%s" and a.hostid=c.hostid and c.status <> 3 and c.hostid=d.hostid and c.hostid=e.hostid and e.ip=f.ip and f.key_=d.key_ and f.itemid=g.itemid' 2>/dev/null """ %(MYSQL_BIN, MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_NAME, tmp_table_name, group_name))
	if res[0] == 0:
		print 'update trends_uint succeed!!'
	else:
		print 'update trends_uint failed!!'

if __name__ == '__main__':
	tmp_table_name = sys.argv[2].strip()
	group_name = sys.argv[3].strip()

	if sys.argv[1] == "backup":
		create_tmp_table(tmp_table_name,group_name)
	elif sys.argv[1] == "update":
		update_items(tmp_table_name,group_name)
	else:
		print 'input error'
