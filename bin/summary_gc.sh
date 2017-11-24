#!/bin/sh

##some usable functions
function usage() {
	echo "Usage: $0 <log_type>"
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
python $LIBS/summary_gc.py $GC_ORI_LOG_DIR $GC_RES_LOG_DIR $file_name
