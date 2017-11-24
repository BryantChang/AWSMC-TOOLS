#!/bin/sh
function usage(){
	echo "Usage: $0 <res_dir> <summary_log_name>"
}

function dir_not_found(){
	echo "The log dir is not found, please check!"
	exit
}

##get current dir
bin=`dirname "$0"`
bin=`cd "$bin"; pwd`
CURDIR=`cd $bin/./; pwd`

if [[ $# -lt 2 ]]; then
	usage
	exit
fi

res_dir=$1
summary_log_name=$2

if [[ -f "$res_dir/$summary_log_name" ]]; then
	rm -rf "$res_dir/$summary_log_name"
fi

echo  "APP_name    Input_size    Exe_mem    IPC    L1D_Miss    L2_Miss    LLC_Miss    Monitor_time" >> "$res_dir/$summary_log_name"

cd ${res_dir}

for file in `ls *.log`; do
	app_name=`sed -n '1p' $file | awk '{print $3}'`
	input_data_size=`sed -n '2p' $file | awk '{print $4}'`
	executor_mem=`sed -n '3p' $file | awk '{print $3}'`
	monitor_time=`sed -n '4p' $file | awk '{print $3}'`
	ipc=`sed -n '5p' $file | awk '{print $2}'`
	l1d_miss=`sed -n '8p' $file | awk '{print $4}'`
	l2_miss=`sed -n '9p' $file | awk '{print $4}'`
	llc_miss=`sed -n '10p' $file | awk '{print $4}'`
	echo  "$app_name    $input_data_size    $executor_mem    $ipc    $l1d_miss    $l2_miss    $llc_miss    $monitor_time" >> "$res_dir/$summary_log_name" 
done

echo "all done"







