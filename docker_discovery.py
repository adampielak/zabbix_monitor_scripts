#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
#import simplejson as json  #特别要注意的地方

t=os.popen(""" docker ps -a|grep -v "CONTAINER ID"|awk '{print $NF}' """)
ports = []
for port in  t.readlines():
        r = os.path.basename(port.strip())
        ports += [{'{#CONTAINERNAME}':r}]
print json.dumps({'data':ports},sort_keys=True,indent=4,separators=(',',':'))
