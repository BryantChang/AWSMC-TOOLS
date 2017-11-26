#!/usr/bin/python
import sys
import subprocess
import os, os.path
import exceptions
import re, string
import time


def popen(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out + err

conf_path=sys.argv[1]
log_path=sys.argv[2]
interval=float(sys.argv[3])

conf_handle = open(conf_path, 'r')
event_arr = []
code_arr = []

a=[i.split('=') for i in conf_handle.readlines()]
index = 0
while index < len(a):
    event = a[index][0]
    code = a[index][1]
    if event[0] == '#':
        index += 1
        continue
    event_arr.append(event)
    code_arr.append(code)
    index += 1
conf_handle.close()
log_handle = open(log_path, 'a')
log_handle.write(' '.join(event_arr)+'\n')
while True:
	b=','.join(code_arr)
	out = popen("sudo perf stat -a -e %s sleep %f"%(b,interval))
        out =out.replace(',','')
        counters = re.findall('\s+(\d+)\s+', out, re.M)
	log_handle.write(' '.join(counters)+ '\n')
	log_handle.flush()
log_handle.close()

