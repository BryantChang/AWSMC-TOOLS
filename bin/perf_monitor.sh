#!/bin/bash


#function usage() {
#	echo "Usage:$0: monitor_log_path"
#	exit
#}
#
#if [[ $# -lt 1 ]]; then
#	usage
#fi

##get the current path and initialize some constant values
bin=`dirname "$0"`
bin=`cd "$bin"; pwd`
DIR=`cd $bin/../; pwd`

LIBS="${DIR}/libs"
BIN="${DIR}/bin"
CONF="${DIR}/conf"


##source the env
. "${CONF}/env.sh"

echo "python ${LIBS}/hw115get_perf_new.py $1"


python ${LIBS}/hw115get_perf_new.py $1 1
# python $MONITOR_DIR $1 $2


