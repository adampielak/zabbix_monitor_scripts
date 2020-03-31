#Redis-Cluster¼à¿Ø
UserParameter=redis.cluster.discovery,/usr/local/zabbix/etc/scripts/redis_cluster_status.py "discovery"
UserParameter=redis_cluster_status[*],/usr/local/zabbix/etc/scripts/redis_cluster_status.py "$1" "$2"

##Redis-Node¼à¿Ø
UserParameter=redis.node.discovery,/usr/local/zabbix/etc/scripts/redis_cluster_node_status.py "discovery"
UserParameter=redis_node_status[*],/usr/local/zabbix/etc/scripts/redis_cluster_node_status.py "$1" "$2" "$3"
