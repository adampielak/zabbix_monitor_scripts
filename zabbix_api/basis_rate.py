#!/usr/bin/python
#coding=utf-8
#Function:获取对应itemid数据

import MySQLdb
import sys
import time
import os

def zabbix_db(ip, username, password, dbname, hostname, key, time_type):
	try:
		#连接数据库
		db = MySQLdb.connect(host = ip, user = username, passwd = password, db = dbname, charset='utf8' )
		cur = db.cursor()
		#根据hostname查询对应hostid
		get_hostid_sql = """ select hostid from hosts where name='%s' """ %hostname 
		cur.execute(get_hostid_sql)
		data = cur.fetchone()

		#根据hostid和key_查询对应itemid
		get_itemid_sql = """ select itemid,value_type from items where hostid='%s' and key_='%s' """ %(data[0],key) 
		cur.execute(get_itemid_sql)
		data = cur.fetchone()	
		itemid, value_type = data[0],data[1]
		#判断数据值类型
		if value_type == 0:
			table_name = "history"
		elif value_type == 1:
			table_name = "history_str"
		elif value_type == 2:
			table_name = "history_log"
		elif value_type == 3:
			table_name = "history_uint"
		elif value_type == 4:
			table_name = "history_text"

		#根据itemid查看最新数据
		get_last_sql = """ select clock,value from %s where itemid='%s' order by clock desc limit 1 """ %(table_name,itemid) 
		cur.execute(get_last_sql)
		data = cur.fetchone()
		last_clock, last_value = data[0], float(data[1])

		#判断是同比7天还是1天
		if time_type == "week":
			time_len = 24 * 7 * 3600
			old_clock = int(last_clock - time_len)
		if time_type == "day":
			time_len = 24 * 3600
			old_clock = int(last_clock - time_len)

		#获取7天或1天前同一时期的数据
		tries = 5
		while tries:
			try:
				get_last_sql = """ select value from %s where itemid='%s' and clock="%s" limit 1 """ %(table_name, itemid, old_clock) 
				cur.execute(get_last_sql)
				data = cur.fetchone()
				old_value = float(data[0])
				break
			except TypeError:
				tries -= 1
				old_clock +=1
				
		#计算同比
		if old_value != 0.0:
			rate = "%.2f" %( (last_value-old_value)/old_value * 100 )
			print rate
		else:
			print 0.00
	
		print time_len
		print last_clock, last_value,old_clock,old_value
		
		cur.close()	
		db.close()
	except TypeError:
			print 0.00
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print "Usage: %s Hostname key time_type(week/day)"
		sys.exit(1)

	ip = "192.168.94.152"
	username = "nn_cms"
	password = "nn_cms1234"
	dbname = "zabbix"
	hostname = sys.argv[1]
	key = sys.argv[2]
	time_type = sys.argv[3]
	zabbix_db(ip, username, password, dbname, hostname, key, time_type)

