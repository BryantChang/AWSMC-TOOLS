#!/bin/bash

function usage() {
    echo "Usage $0 <res_log_path> <internal>"
}


if [[ $# -lt 2 ]]; then
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

res_log_path=$1
internal=$2


conf_log_path="${CONF}/eventmap.properties"

python ${LIBS}/perf_tools.sh $conf_log_path $res_log_path $internal

