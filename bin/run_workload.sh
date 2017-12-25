#!/bin/bash


function usage() {
    echo "Usage: $0: app_name input mem log_path"
}

if [[ $# -lt 4 ]]; then
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
input=$2
mem=$3
log_path=$4

echo "setting the memory configuration"
echo "setting the memory configuration" >> ${log_path}


sed -i "/TYPE=/ c TYPE=\"${input}M\"" ${SPARKBENCH_HOME}/${app}/conf/env.sh
sed -i "/SPARK_EXECUTOR_MEMORY=/ c SPARK_EXECUTOR_MEMORY=\"${mem}m\"" ${SPARKBENCH_HOME}/${app}/conf/env.sh

${SPARKBENCH_HOME}/${app}/bin/run.sh

















