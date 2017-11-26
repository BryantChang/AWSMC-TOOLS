import numpy as np
import pylab as pl
import sys
import os
# x = [1, 2, 3, 4, 5]# Make an array of x values
# y = [1, 4, 9, 16, 25]# Make an array of y values for each x value
# pl.plot(x, y)# use pylab to plot x and y
 
# pl.title('Plot of y vs. x')# give plot a title
# pl.xlabel('x axis')# make axis labels
# pl.ylabel('y axis')
 
# pl.xlim(0.0, 7.0)# set axis limits
# pl.ylim(0.0, 30.)
 
# pl.show()# show the plot on the screen

monitor_log_base = sys.argv[1]
gc_res_log_base = sys.argv[2]
log_name = sys.argv[3]
gc_res_full_log = gc_res_log_base + "/" + "detail_" + log_name
gc_graph_path = sys.argv[4]

isExists=os.path.exists(gc_graph_path)
if not isExists:
    os.mkdir(gc_graph_path)
log_handler = open(gc_res_full_log)
log_info_arr = log_name.split(".")
log_info = log_info_arr[0]
gc_graph_full_path = gc_graph_path + "/" + log_info + ".png"

pl.title(log_info)
pl.xlabel('Stage No')
pl.ylabel('Gc Times')

stages=[]
gc_times=[]
a=[i.split() for i in log_handler.readlines()]
index = 4
while index < len(a):
	stageNo = a[index][1][:-1]
	gcTime = a[index][2]
	stages.append(stageNo)
	gc_times.append(gcTime)
	index += 1

pl.plot(stages, gc_times)
pl.savefig(gc_graph_full_path)
print("draw succ")
# 













