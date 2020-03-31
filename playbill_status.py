#!/usr/bin/python
# -*- coding: utf-8 -*-

import types
import urllib2
import json
import os
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#煤资包ID
media_assets_id = ['nn_live','channel']
#media_assets_id = ['channel']

#N39_a_1获取煤资包下所有频道列表,nns_media_assets_id 设置为变量
get_channel_list_url = "http://10.21.16.39/gzgd/EPGV2?nns_media_assets_id=%s&nns_category_id=1000&nns_include_category=1&nns_order_type=6&nns_buss_id=200000&nns_func=get_channel_list&nns_mac=88-CC-45-B2-D7-FC&nns_mac_id=88-CC-45-B2-D7-FC&nns_version=1.12.005.STB.GZGD.AUTO.OTT01.Release&nns_user_agent=nn_player&nns_area_code=156520027012029009&nns_user_id=01010217051710457794&nns_webtoken=9e1d8401545cd619e98c8205043098cc&nns_output_type=json&nns_tag=26"
#N39_A_12获取指定频道的所有节目单,nns_video_id，通过n39_a_1接口获取之后变量传入
get_playbill_url = "http://10.21.16.39/gzgd/EPGV2?nns_video_id=%s&nns_before_day=0&nns_after_day=3&nns_buss_id=200000&nns_func=get_playbill_by_days&nns_mac=88-CC-45-7D-4D-A6&nns_mac_id=88-CC-45-7D-4D-A6&nns_version=1.10.313.STB.GZGD.AUTO.OTT01.Release&nns_user_agent=nn_player&nns_area_code=15652000200301500c&nns_user_id=01010217032308385301&nns_webtoken=04986d13e887be7a19518c23681a18a6&nns_output_type=json&nns_tag=26"

filename="/tmp/playbill_status.json"

time_str = time.time()
time_today = time.strftime('%Y%m%d', time.localtime(time_str))
time_tomorrow = time.strftime('%Y%m%d', time.localtime(time_str + 60 * 60 * 24 ))

def get_video_id():
	try:
		video_id_list = []
		for id in media_assets_id:
			i = 0
			while i < 3:
				url = get_channel_list_url %id
				data = urllib2.urlopen(url,timeout=30)
				code = data.getcode()
				if code != 200:
					i += 1
				else:
					break
			content = json.loads(data.read())
			con_list = content['l']['il']
			for con in con_list:
				video_id_list.append(con['name'].strip()+':'+con['id'].strip())
		video_id_list = list(set(video_id_list))
		video_id_list_1 = []
		for i in video_id_list:
			video_id_list_1.append({'{#VIDEONAME}':i.split(':')[0],'{#VIDEOID}':i.split(':')[1]})

		return json.dumps({"data":video_id_list_1},sort_keys=True, encoding='UTF-8', ensure_ascii=False, indent=4)
				
	except Exception, e:
		return e

def cache(file_name, len_time, video_id):
    if not os.path.exists(file_name):
		get_playbill(video_id, file_name)
    statinfo = os.stat(file_name)
    ltime = int(statinfo.st_mtime)
    ntime = int(time.time())-len_time
    if ltime <= ntime:
		get_playbill(video_id, file_name)


def get_playbill(video_id, file_name):
	try:
		url = get_playbill_url %video_id
		i = 0
		while i < 3:
			data = urllib2.urlopen(url,timeout=30)
			code = data.getcode()
			if code != 200:
				i += 1
			else:
				break

		with open(file_name,'w') as fw:
			fw.write(data.read())
						
	except Exception, e:
		return e

def judge_status(video_id, file_name):
	try:
		cache(file_name, 30, video_id)
		with open(file_name) as fr:
			data = fr.read()
		content = json.loads(data)
		playbill_list = content['l']['il']
		flag = 0
		for i in playbill_list:
			if i['arg_list']['day'].strip() == time_tomorrow:
				if i.has_key('id'):
					pass
				else:
					flag = 1
		if flag == 0:
			return 1
		else:
			return 0
	except Exception, e:
		return e

	
	


if __name__=="__main__":
	if sys.argv[1].strip() == "discovery":
		print get_video_id()
	else:
		print judge_status(sys.argv[1],filename)

