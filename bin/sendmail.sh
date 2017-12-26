#!/bin/bash


function usage() {
    echo "Usage: $0 <conf_path> <sample_log> <log_name>"
}

if [[ $# -lt 3 ]]; then
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

conf_file=$1
sample_log=$2
log_name=$3


${LIBS}/sendmail.py ${conf_file} ${sample_log} ${log_name}
