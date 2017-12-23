#!/usr/bin/python

import sys
import subprocess
import os, os.path
import exceptions
import re, string
import time

log_name = sys.argv[1]
category_no = int(sys.argv[2])

monitor_log_base = "/Users/bryantchang/Desktop/study/Research/experiment/original_log/sparklogs_1114/monitor_logs/analyse_result/"
gc_log_base = "/Users/bryantchang/Desktop/study/Research/experiment/original_log/sparklogs_1114/gc_logs/gc_result/"
feature_csv_base = "/Users/bryantchang/Desktop/study/Research/experiment/original_log/sparklogs_1114/samples/"


is_dir_exist = os.path.exists(feature_csv_base)


if not is_dir_exist:
    os.mkdir(feature_csv_base)

print("writting csv samples")

monitor_log_file = monitor_log_base + log_name
gc_log_file = gc_log_base + "summary_" + log_name
csv_file = feature_csv_base + "classification_sample.csv"

is_csvfile_exist = os.path.exists(csv_file)
csv_handle = open(csv_file, 'a')
gc_log_handle = open(gc_log_file, 'r')
monitor_log_handle = open(monitor_log_file, 'r')

if not is_csvfile_exist:
    csv_handle.write("GCSD,PF,IPC,L1D,L2,LLC,LSR,CN\n")

a = [i.split(':') for i in monitor_log_handle.readlines()]
b = [i.split('\t') for i in gc_log_handle.readlines()]
gc_std_dev = float(b[1][7])
ipc = float(a[4][1])
l1d_miss = float(a[7][1])
l2_miss = float(a[8][1])
llc_miss = float(a[9][1])
page_fault = float(a[11][1])
lsr = float(a[13][1])



csv_handle.write("%0.2f,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f,%d\n"
                 %(gc_std_dev,page_fault,ipc,l1d_miss,l2_miss,llc_miss,lsr,category_no))


monitor_log_handle.close()
gc_log_handle.close()
csv_handle.close()
print("writting csv samples completed")