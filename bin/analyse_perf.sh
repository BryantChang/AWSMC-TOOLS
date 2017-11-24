#!/bin/sh

##some usable functions
function usage(){
    echo "Usage: $0 <filename>"
}

##get the current path and initialize some constant values
bin=`dirname "$0"`
bin=`cd "$bin"; pwd`
DIR=`cd $bin/../; pwd`

LIBS="${DIR}/libs"
BIN="${DIR}/bin"
CONF="${DIR}/conf"


##source the env
. "${CONF}/env.sh"

##parameter check
if [[ $# -lt 1 ]]; then
    usage
    exit
fi

file_name=$1
python $LIBS/analyse_perf.py $MONITOR_ORI_LOG_DIR  $MONITOR_RES_LOG_DIR $file_name
