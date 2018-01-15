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
rdd_compress_boolean=`echo ${features} | cut -d '_' -f 5`
shuffle_compress_boolean=`echo ${features} | cut -d '_' -f 6`
best_mem=`echo ${features} | cut -d '_' -f 7`

if [[ ${rdd_compress_boolean} = "true" ]]; then
    rdd_compress_value=1
elif [[ ${rdd_compress_boolean} = "false" ]]; then
    rdd_compress_value=0
fi

if [[ ${shuffle_compress_boolean} = "true" ]]; then
    shuffle_compress_value=1
elif [[ ${shuffle_compress_boolean} = "false" ]]; then
    shuffle_compress_value=0
fi

echo "${input_size},${exe_cores},${block_size},${parallelism},${rdd_compress_value},${shuffle_compress_value},${best_mem}" >> ${sample_log_path}
