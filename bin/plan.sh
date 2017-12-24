#!/bin/bash

function usage() {
    echo "Usage: $0 app_name"
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

app=$1
log_path=${TMP_DIR}/${app}.log

echo "initializing" >> ${log_path}
echo "initializing"

mkdir -p ${TMP_DIR}
mkdir -p ${ERR_DIR}
mkdir -p ${EVENT_LOG_DIR}

echo "begin to generate"

for input in `cat ${CONF}/input_data_confs`; do
    echo "current input data size is ${input} M"
    
done




