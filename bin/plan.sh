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



if [[ -f ${log_path} ]]; then
    rm -rf ${log_path}
fi


echo "initializing" >> ${log_path}
echo "initializing"

mkdir -p ${TMP_DIR}
mkdir -p ${ERR_DIR}
mkdir -p ${EVENTLOG_DIR}

echo "begin to generate"

for input_mem in `cat ${CONF}/input_mem_${app}`; do
    if [[ "${input_mem:0:1}" = "#" ]]; then
        continue;
    fi
    input=`echo ${input_mem} | cut -d '-' -f 1`
    mem=`echo ${input_mem} | cut -d '-' -f 2`
    echo "current input data size is ${input} M"
    echo "current input data size is ${input} M" >> ${log_path}
    echo "init mem is ${mem} m"
    echo "init mem is ${mem} m" >> ${log_path}
    for params in `cat ${CONF}/params`; do
        ${bin}/change_params.sh ${app} ${params} ${log_path}
        best_mem_path=${TMP_DIR}/${app}_${input}_${params}.log

    done

done




