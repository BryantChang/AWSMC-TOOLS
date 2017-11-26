#!/bin/bash

##get the current path and initialize some constant values
bin=`dirname "$0"`
bin=`cd "$bin"; pwd`
DIR=`cd $bin/../; pwd`

LIBS="${DIR}/libs"
BIN="${DIR}/bin"
CONF="${DIR}/conf"


##source the env
. "${CONF}/env.sh"

function usage() {
    echo "$0  <log_name> "
}

if [[ $# -lt 1 ]]; then
    usage
    exit
fi

log_name=$1

python get_graph.py $MONITOR_ORI_LOG_DIR $log_name $GC_GRAPH_DIR