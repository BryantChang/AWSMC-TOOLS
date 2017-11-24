#!/usr/bin/python2

#   Copyright 2011 Huafeng Xi, Zhen Jia, Jianfeng Zhan, and Lei Wang 
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
Usage: ./hmon.py %events-set-selector log-path record-interval
%events-set-selector may be:
  kperf kperf-basic kperf-cache kperf-instruction
  proc cpu mem net disk

Example: ./hmon.py cpu a.log 1
"""

import sys
import subprocess
import os, os.path
import exceptions
import re, string
import time

######################################## Common Stuff ########################################
class HmonErr(exceptions.Exception):
    def __init__(self, msg, obj=None):
        exceptions.Exception(self)
        self.obj, self.msg = obj, msg

    def __str__(self):
        return "HMon Exception: %s\n%s"%(self.msg, self.obj)
    
def list_slices(seq, *slices):
    return [seq[i] for i in slices]

def list_merge(*l):
    return reduce(lambda a,b: list(a)+list(b), l, [])

def sub(template, env={}, **vars):
    return string.Template(template).safe_substitute(env, **vars)

def popen(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if p.returncode != 0:
        raise HmonErr('%s\n%s'%(err, out), cmd)
    return out + err

def read(path):
    if path.startswith('P#'):
        return popen(path[2:])
    f = open(path)
    result = f.read()
    f.close()
    return result

def readlines(file):
    content = read(file)
    return filter(None, content.split('\n'))

def table_load(path):
    lines = [line.split() for line in readlines(path)]
    return lines[0], lines[1:]

def transpose(matrix):
    cols = [[] for i in matrix[0]] # Note: You can not write cols = [[]] * len(matrix[0]); if so, all col in cols will ref to same list object 
    for row in matrix:
        map(lambda col,i: col.append(i), cols, row)
    return cols

def interval_times(interval):
    while True:
        yield time.time()
        time.sleep(interval)

def log_read(path, *h):
    header, data = table_load(path)
    cols = [header.index(h) for c in cols]
    if any([c == -1 for c in cols]): raise HmonErr('no such cols', cols)
    return [seq_slice(row, *cols) for row in data]

def log_write(path, times, *collectors):
    if os.path.exists(path): raise HmonErr('log file already exists', path)
    f = open(path, 'a')
    f.write('\t'.join(['timestamp'] + list_merge(*[c.values for c in collectors])) + '\n')
    for t in times:
        f.write('\t'.join([str(t)]+ list_merge(*[c() for c in collectors])) + '\n')
        f.flush()
    f.close()

def make_extractor(path, pat):
    compiled_pat = re.compile(re.sub('\$\w+', ' *(\d+)', pat), re.M | re.S)
    values = re.findall('\$(\w+)', pat)
    def extract():
        mat = re.search(compiled_pat, read(path))
        if not mat: raise HmonErr('Extract Error', pat)
        return mat.groups()
    extract.path, extract.values, extract.pat = path, values, pat
    return extract

def make_extractor_acc(path, pat):
    compiled_pat = re.compile(re.sub('\$\w+', ' *(\d+)', pat), re.M | re.S)
    values = re.findall('\$(\w+)', pat)
    def extract():
        mat = re.findall(compiled_pat, read(path))
        if not mat: raise HmonErr('Extract Error', pat)
        mat = transpose(mat)
        return [str(sum([int(col) for col in row])) for row in mat]
    extract.path, extract.values, extract.pat = path, values, pat
    return extract

######################################## proc info extractor ########################################
stat_path = '/proc/stat'
stat_pattern = """cpu $usr $nice $sys $idle $iowait $irq $softirq.*
intr $intr .*
ctxt $ctx .*
processes $procs
procs_running $running
procs_blocked $blocked"""

meminfo_path = '/proc/meminfo'
meminfo_pattern = """MemTotal: $mem_total kB
MemFree: $free kB
Buffers: $buffers kB
Cached: $cached kB
SwapCached: $swap_cached kB
Active: $active kB
Inactive: $inactive kB
.*
SwapTotal: $swap_total kB
SwapFree: $swap_free kB"""

vmstat_path = '/proc/vmstat'
vmstat_pattern = """pgpgin $pgin
pgpgout $pgout
.*
pgfault $pgfault
pgmajfault $pgmajfault"""

snmp_path = '/proc/net/snmp'
snmp_pattern = 'Tcp: \S+ \S+ \S+ \S+ $active_conn $passive_conn' 
netdev_path = '/proc/net/dev'
netdev_pattern = 'eth.: $rbytes $rpackets $rerrs $rdrop +\S+ +\S+ +\S+ +\S+ $sbytes $spackets $serrs $sdrop'

diskstat_path = '/proc/diskstats'
diskstat_pattern = '^ +8 +(?:112|48|64|3|1) +\S+ $read $read_merged $read_sectors $read_time $write $write_merged $write_sectors $write_time $progress_io $io_time $io_time_weighted'
proc_events = [(src, re.findall('\$(\w+)', globals().get(src+'_pattern'))) for src in ('stat', 'meminfo', 'vmstat', 'snmp', 'netdev', 'diskstat')]

get_stat = make_extractor(stat_path, stat_pattern)
get_meminfo = make_extractor(meminfo_path, meminfo_pattern)
get_vmstat = make_extractor(vmstat_path, vmstat_pattern) 
get_snmp = make_extractor(snmp_path, snmp_pattern)
get_netdev = make_extractor_acc(netdev_path, netdev_pattern)
get_diskstat = make_extractor_acc(diskstat_path, diskstat_pattern)

######################################## kperf info extractor ########################################
kperf_events_map = '''
CPU_CLK_UNHALTED.CORE 3c           # cpu_cycles
CPU_CLK_UNHALTED.BUS 13c           # bus_cycles
INST_RETIRED.ANY c0                # insts
ITLB_MISS_RETIRED c9               # itlb_misses
DTLB_MISSES.ANY 108                # dtlb_misses
L1I_MISSES 81                      # icache_misses
L1D_REPL f45                       # dcache_misses
L2_LINES_IN.ANY f024               # l2cache_misses

PAGE_WALKS.CYCLES  20c             # page_walks
CYCLES_L1I_MEM_STALLED 86          # icache_stalls

BR_INST_RETIRED.ANY c4             # br_insts
BR_INST_RETIRED.MISPRED c5         # br_misses

INST_RETIRED.LOADS 1c0             # load_insts
INST_RETIRED.STORES 2c0            # store_insts
INST_RETIRED.OTHER 4c0             # other_insts
SIMD_INST_RETIRED.ANY 1fc7         # simd_insts
FP_COMP_OPS_EXE 10                 # fp_insts

RESOURCE_STALLS.ANY 1fdc           # res_stalls
RESOURCE_STALLS.ROB_FULL 1dc       # rob_stalls
RESOURCE_STALLS.RS_FULL 2dc        # rs_stalls
RESOURCE_STALLS.LD_ST 4dc          # ldst_stalls
RESOURCE_STALLS.FPCW 8dc           # fpcw_stalls
RESOURCE_STALLS.BR_MISS_CLEAR 10dc # br_miss_stalls

BUS_TRANS_ANY  e070                # bus_trans
BUS_DRDY_CLOCKS 2062               # bus_drdy
BUS_BNR_DRV 2061                   # bus_bnr
BUS_TRANS_BRD e065                 # bus_trans_brd
BUS_TRANS_RFO e066                 # bus_trans_rfo
'''
kperf_events_abbrs = '''
basic: cpu_cycles bus_cycles insts
cache: itlb_misses dtlb_misses icache_misses dcache_misses l2cache_misses page_walks icache_stalls
branches: br_insts br_misses
bus: bus_trans bus_drdy bus_bnr bus_trans_brd bus_trans_rfo
res: res_stalls rob_stalls rs_stalls ldst_stalls fpcw_stalls br_miss_stalls
inst_mix: load_insts store_insts other_insts simd_insts fp_insts
'''
kperf_events = [(_type, events.split()) for _type, events in re.findall('(\w+): (.+)', kperf_events_abbrs)]
                           
def get_kperf_events(events):
    abbrs = dict(re.findall('^(\w+): +(.+)$', kperf_events_abbrs, re.M))
    emap = dict([(k,'r'+v) for (v,k) in re.findall('^\S+ +(\w+) +# (\w+)', kperf_events_map, re.M)])
    events = sub(events, abbrs).split()
    return events, [emap[ev] for ev in events]

def make_kperfstat_extractor(events, interval):
    names, codes = get_kperf_events(events)
    def get_kperf_info():
        out = popen("sudo perf stat -a %s sleep %d"%(' '.join(["-e %s"%e for e in codes]), interval))
        counters = re.findall('^\s+(\d+)\s+[-a-zA-Z]+', out.replace('<not counted>', '0'), re.M)
        assert(len(counters))
        return counters
    get_kperf_info.path, get_kperf_info.values, get_kperf_info.pat = None, names, None
    return get_kperf_info

######################################## interface ########################################
def hmon_record(events_set, path, interval):####cpu 1.log 1
    get_kperf_all = make_kperfstat_extractor('$basic $cache $branches $bus $res $inst_mix', interval)
    get_kperf_basic = make_kperfstat_extractor('$basic', interval)
    get_kperf_cache = make_kperfstat_extractor('$basic $cache', interval)
    get_kperf_instruction = make_kperfstat_extractor('$basic $branches $inst_mix', interval)
    collector_sets = {'kperf': [get_kperf_all],
                  'kperf-basic': [get_kperf_basic], 'kperf-cache':[get_kperf_cache], 'kperf-instruction':[get_kperf_instruction],
                  'proc': [get_stat, get_meminfo, get_vmstat, get_snmp, get_netdev, get_diskstat],
                  'cpu': [get_stat], 'mem':[get_meminfo,  get_vmstat], 'net': [get_snmp,get_netdev], 'disk': [get_diskstat]}
    collectors = collector_sets.get(events_set)
    if not collectors: raise HmonErr('no such events_set', events_set)
    print 'log_write(%s, interval_times(%f), %s)' % (path, interval, ','.join([str(c.values) for c in collectors]))
    sys.stdout.flush()
    if events_set.startswith('kperf'): interval = 0.0
    log_write(path, interval_times(interval), *collectors)

def list_events():
    print 'Proc Events:'
    print '\n'.join(['%s: %s'%(type, ' '.join(events)) for type,events in proc_events])
    print ''
    print 'Kperf Events:'
    print '\n'.join(['%s: %s'%(type, ' '.join(events)) for type,events in kperf_events])

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print __doc__
        list_events()
        sys.exit(1)
    hmon_record(sys.argv[1], sys.argv[2], float(sys.argv[3]))
