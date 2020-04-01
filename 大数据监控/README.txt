#¼à¿Øhadoop
UserParameter=hadoop.discovery[*],/usr/local/zabbix/etc/scripts/hadoop_status.py "$1" "$2"
UserParameter=hadoop.status[*],/usr/local/zabbix/etc/scripts/hadoop_status.py "$1" "$2" "$3" "$4" "$5" "$6"



pip install cm-api 

cd setuptools-1.4.2  
python setup.py build  && python setup.py install
cd cm_api/python  && python setup.py install
