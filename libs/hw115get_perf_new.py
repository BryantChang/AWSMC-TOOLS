#!/usr/bin/python

import sys
import subprocess
import os, os.path
import exceptions
import re, string
import time

path=sys.argv[1]
interval=float(sys.argv[2])
def popen(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out + err 


f=open(path,'a')
#codes=['r3c:k','r3c:u','rc0:k','rc0:u','rc4','r1c0','r2c0','rfec1','rc9','r108','r412e','r4f2e','r0143','r0243','r80','r81','rfc2','r8aa','r86','r283','r1aa','r2062','r1dc','r2dc','r4dc','r8dc','r10dc']
#events=['cycles_k','cycles_u','ins_k','ins_u','bran','load','store','fp','itlb_miss','dtlb_miss','l2cache_miss','l2cache_reference','L1Dcache_hit','L1Dcache_miss','L1I_READS','L1I_miss','uops','cisc','fron_stall','inst_queue_full','ins_de','BUS_DRDY','rob_stall','rs_stall','ld_stall','fpcw_stall','br_stall']
# codes=[' page-faults','rc0','rc4','r10b','r20b','r110','uncore/event=0x2c,umask=0x07/','rf024','rc026','r307','rc1','uncore/event=0x2f,umask=0x07/','r1ca','r2ca','r4ca','r8ca','r1fc7']
# codes=['page-faults','L1-dcache-loads','L1-dcache-load-misses','L1-dcache-stores','L1-dcache-store-misses','LLC-loads','LLC-load-misses','LLC-stores','LLC-store-misses','dTLB-loads','dTLB-load-misses','dTLB-stores','dTLB-store-misses']
codes=['page-faults','rc0','r3c','r2cb','rf024','r108','r412e','r1c0','r2c0']
# events=['page-faulte','ins','br','load','store','fp','UNC_READ','L2_in','L2_out','SSE_store','X87','UNC_WRITE','pack_single','scalar_single','pack_double','scalar_double','simd']
events=['page-faults','inst','cycles','l1d-miss','l2-miss','dtlb-miss','llc-miss','load','store']
# print len(codes)
# print len(events)
f.write(' '.join(events)+'\n')
while True:
	a=','.join(codes)
  # print a
	out = popen("sudo perf stat -a -e %s sleep %f"%(a,interval))
        out =out.replace(',','')
        counters = re.findall('\s+(\d+)\s+', out, re.M)
	f.write(' '.join(counters)+ '\n')
	f.flush()
f.close()
