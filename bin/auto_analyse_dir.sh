#!/bin/bash
function usage() {
	echo "Usage: $0 <log_type>"
}

##argument check
if [[ $# -lt 1 ]]; then
	usage
	exit
fi

##get the current path and initialize some constant values
bin=`dirname "$0"`
bin=`cd "$bin"; pwd`
DIR=`cd $bin/../; pwd`

LIBS="${DIR}/libs"
BIN="${DIR}/bin"
CONF="${DIR}/conf"


##source the env
. "${CONF}/env.sh"

log_type=$1

if [[ $log_type = "gc" ]]; then
    script="summary_gc.sh"
    log_dir=$GC_ORI_LOG_DIR
elif [[ $log_type = "monitor" ]]; then
    script="analyse_perf.sh"
    log_dir=$MONITOR_ORI_LOG_DIR
elif [[ $log_type = "gc_graph" ]]; then
    script="get_graph.sh"
    log_dir=$MONITOR_ORI_LOG_DIR
fi

#
cd ${log_dir}

for file in `ls *.log`; do
	echo "operating $file"
	sh $BIN/$script $file
done

echo "all done"









