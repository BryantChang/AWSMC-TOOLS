#!/usr/bin/python
import sys
import os
import numpy

print("begin to analyse gc")

gc_log_base = sys.argv[1]
res_file_base = sys.argv[2]
log_name = sys.argv[3]

isExists=os.path.exists(res_file_base)
if not isExists:
    os.mkdir(res_file_base)

summary_log_name = "summary_" + log_name
detail_log_name = "detail_" + log_name
summary_log_full_path = res_file_base + "/" + summary_log_name
detail_log_full_path = res_file_base + "/" + detail_log_name

#Some functions
def getStd(counts):
    n_array = numpy.array(counts) 
    return numpy.std(n_array, ddof = 1)

def getVC(counts):
    n_array = numpy.array(counts) 
    return getStd(counts) / numpy.mean(n_array)   

log_info_arr = log_name.split(".")
log_info = log_info_arr[0]
app_info_arr = log_info.split("_")

app_name = app_info_arr[0]
input_data_size = app_info_arr[1]
executor_mem = app_info_arr[2]

analse_file_handler = open(gc_log_base + "/" + log_name)

a=[i.split() for i in analse_file_handler.readlines()]
max_gc_count = 0
max_stage = 0
cur_gc_count = int(a[0][2])
cur_stage = int(a[0][0])
tmp_max_gc = cur_gc_count
recompute_time = 0
index = 1
gc_counts = []
detail_log_handler = open(detail_log_full_path, 'w')
detail_log_handler.write('App Name: %s\n'%app_name)
detail_log_handler.write('Input Data Size: %s\n'%input_data_size)
detail_log_handler.write('Executor Memory: %s\n'%executor_mem)
detail_log_handler.write('Detail GC On each Stage: \n')
while index < len(a):
    tmp_stage = int(a[index][0])
    tmp_gc_count = int(a[index][2])
    if tmp_stage == cur_stage:
        if tmp_gc_count > tmp_max_gc:
            tmp_max_gc = tmp_gc_count
    elif tmp_stage > cur_stage:
        count = tmp_max_gc - cur_gc_count
        gc_counts.append(count)
        detail_log_handler.write("Stage %s: %d\n"%(cur_stage, count))
        if count > max_gc_count:
            max_gc_count = count
            max_stage = cur_stage
        cur_stage = tmp_stage
        cur_gc_count = tmp_gc_count
    else:
        recompute_time += 1
        cur_stage = tmp_stage
        cur_gc_count = tmp_gc_count
    index += 1
detail_log_handler.close()
summary_log_handler = open(summary_log_full_path, 'w')
std = getStd(gc_counts)
vc = getVC(gc_counts)
summary_log_handler.write("name \t input_size \t exec_mem \t stages \t max_gc_stage \t max_gc_count \t rec_times \t std \t vc\n")
summary_log_handler.write("%s \t %s \t %s \t %d \t %d \t %d \t %d \t %0.2f \t %0.2f\n"%(app_name, input_data_size, executor_mem, cur_stage, max_stage, max_gc_count, recompute_time, std, vc))
summary_log_handler.close()
analse_file_handler.close()

print("analyse gc succ")

