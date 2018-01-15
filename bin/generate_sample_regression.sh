#!/bin/bash


function usage(){
    echo "Usage: $0 <log_path> <features>"
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


sample_log_path=$1
features=$2


input_size=`echo ${features} | cut -d '_' -f 1`
exe_cores=`echo ${features} | cut -d '_' -f 2`
block_size=`echo ${features} | cut -d '_' -f 3`
parallelism=`echo ${features} | cut -d '_' -f 4`
rdd_compress=`echo ${features} | cut -d '_' -f 5`
shuffle_compress=`echo ${features} | cut -d '_' -f 6`
best_mem=`echo ${features} | cut -d '_' -f 7`

echo "${input_size},${exe_cores},${block_size},${parallelism},${rdd_compress},${shuffle_compress},${best_mem}" >> ${sample_log_path}
