#!/usr/bin/python
import sys
import os
print("begin analyse perf")


log_base = sys.argv[1]
res_path = sys.argv[2]
log_name = sys.argv[3]
log_full_dir = log_base + "/" + log_name
print(log_full_dir)
conf = open(log_full_dir)
isExists=os.path.exists(res_path)
if not isExists:
    os.mkdir(res_path)


log_info_arr = log_name.split(".")
log_info = log_info_arr[0]
app_info_arr = log_info.split("_")

app_name = app_info_arr[0]
input_data_size = app_info_arr[1]
executor_mem = app_info_arr[2]


res_log_path = res_path + "/" + log_name
a=[i.split() for i in conf.readlines()]
##1E9
one_e_nine = 1000000000
##Initial some metrics
sum_pf = 0
sum_inst = 0
sum_cycles = 0
sum_l1d_miss = 0
sum_l2_miss = 0
sum_dtlb_miss = 0
sum_llc_miss = 0
sum_load = 0 
sum_store = 0
# print (len(a))

##skip the first line
index = 1
secs = 0
while index < len(a):
    if len(a[index]) < 7:
        i+=1
        continue
    if not a[index][0].isdigit():
        index+=1
        continue
    sum_pf += int(a[index][0])
    sum_inst += int(a[index][1])
    sum_cycles += int(a[index][2])
    sum_l1d_miss += int(a[index][3])
    sum_l2_miss += int(a[index][4])
    sum_dtlb_miss += int(a[index][5])
    sum_llc_miss += int(a[index][6])
    sum_load += int(a[index][7])
    sum_store += int(a[index][8])
    index += 1
    secs += 1

res_file_handle = open(res_log_path, 'w')
res_file_handle.write('App Name: %s\n'%app_name)
res_file_handle.write('Input Data Size: %s\n'%input_data_size)
res_file_handle.write('Executor Memory: %s\n'%executor_mem)
res_file_handle.write('Monitor Time: %s\n'%secs)
res_file_handle.write('IPC: %.2f\n'%(float(sum_inst)/sum_cycles))
res_file_handle.write('Cycles(E9): %.2f\n'%float((sum_cycles)/one_e_nine))
res_file_handle.write('Instructions(E9): %.2f\n'%float((sum_inst)/one_e_nine))
res_file_handle.write('L1D Cache Miss: %.2f\n'%float(sum_l1d_miss*1000/sum_inst))
res_file_handle.write('L2 Cache Miss: %.2f\n'%float(sum_l2_miss*1000/sum_inst))
res_file_handle.write('LLC Cache Miss: %.2f\n'%float(sum_llc_miss*1000/sum_inst))
res_file_handle.write('DTLB Cache Miss: %.2f\n'%float(sum_dtlb_miss*1000/sum_inst))
res_file_handle.write('Page Fault: %.2f\n'%(float(sum_pf)/secs))
res_file_handle.write('MAI: %.2f\n'%(float(sum_load+sum_store)/sum_inst))
res_file_handle.write('Load-Store ratio: %.2f\n'%(float(sum_load/sum_store)))
# res_file_handle.write("Input Data Size: ", input_data_size)
# res_file_handle.write("Executor Memory: ", executor_mem)

res_file_handle.close()
conf.close()
print("analyse perf succ")



