#!/bin/bash

function usage() {
    echo "Usage: $0 <sample_path> <log_prefix> "
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
. "${CONF}/sysenv.sh"

sample_path=$1
log_prefix=$2

gcsd=`ssh ${SLAVE_HOST} cat ${GC_RES_LOG_DIR}/summary_${log_prefix}.log | grep ${app} | cut -f 8| sed s/[[:space:]]//g`
pf=`ssh ${SLAVE_HOST} cat ${MONITOR_RES_LOG_DIR}/${log_prefix}.log | grep "Page" | cut -f 2 | sed s/[[:space:]]//g `
l1d=`ssh ${SLAVE_HOST} cat ${MONITOR_RES_LOG_DIR}/${log_prefix}.log | grep "L1D" | cut -f 2 | sed s/[[:space:]]//g `
l2=`ssh ${SLAVE_HOST} cat ${MONITOR_RES_LOG_DIR}/${log_prefix}.log | grep "L2" | cut -f 2 | sed s/[[:space:]]//g `
llc=`ssh ${SLAVE_HOST} cat ${MONITOR_RES_LOG_DIR}/${log_prefix}.log | grep "LLC" | cut -f 2 | sed s/[[:space:]]//g `
lsr=`ssh ${SLAVE_HOST} cat ${MONITOR_RES_LOG_DIR}/${log_prefix}.log | grep "Load-Store" | cut -f 2 | sed s/[[:space:]]//g `

echo "${gcsd},${pf},${l1d},${l2},${llc},${lsr}" >> ${sample_path}
