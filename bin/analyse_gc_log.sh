#!/bin/bash
function usage() {
	echo "Usage:$0 <logName>"
}

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



log_name=$1

full_gc_log=$EXECUTOR_ORI_LOG_DIR/$log_name
full_gc_res_log=$GC_ORI_LOG_DIR/$log_name


if [[ ! -d $GC_ORI_LOG_DIR ]]; then
	mkdir -p $GC_ORI_LOG_DIR
fi




cat $full_gc_log | grep "==" | awk -F '==' '{print $2}' >> $full_gc_res_log