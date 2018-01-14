#!/bin/bash

function usage() {
    echo "Usage $0 <res_log_path>"
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
. "${CONF}/sysenv.sh"

res_log_path=$1
internal=$2


conf_log_path="${CONF}/${EVENTMAP_CONF}"
echo ${conf_log_path}

#

python ${LIBS}/perf_tool.py ${conf_log_path} ${res_log_path} ${MONITOR_INTERNAL}

