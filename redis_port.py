#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
#import simplejson as json  #特别要注意的地方

t=os.popen("""ss -tpnl|grep redis-server|awk '{print $4}'|awk -F ":" '{print $NF}'|uniq """)
ports = []
for port in  t.readlines():
        r = os.path.basename(port.strip())
        ports += [{'{#REDISPORT}':r}]
print json.dumps({'data':ports},sort_keys=True,indent=4,separators=(',',':'))
