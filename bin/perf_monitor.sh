#!/bin/bash

MONITOR_DIR=/home/hadoop/bryantchang/tools/monitor

function usage(){
	echo "Usage:$0: monitor_log_path monitor_interval"
	exit
}

if [[ $# -lt 1 ]]; then
	usage
fi

echo "python $MONITOR_DIR/hw115get_perf_new.py $1"


python $MONITOR_DIR/hw115get_perf_new.py $1 1
# python $MONITOR_DIR $1 $2