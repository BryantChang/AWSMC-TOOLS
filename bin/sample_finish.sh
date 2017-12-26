#!/bin/bash

function usage() {
    echo "Usage: $0 confName appName mem"
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

conf_file=$1
app=$2
sample_count=$3

python ${LIBS}/sample_finish.py ${conf_file} ${app} ${sample_count}