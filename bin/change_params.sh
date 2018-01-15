#!/bin/bash


function usage() {
    echo "Usage: $0 app params log_path"
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

app=$1
params=$2
log_path=$3


spark_cores=`echo ${params} | cut -d '_' -f 1`
spark_parallelism=`echo ${params} | cut -d '_' -f 3`
rdd_compress=`echo ${params} | cut -d '_' -f 4`
shuffle_compress=`echo ${params} | cut -d '_' -f 5`

echo "set parameters"
echo "set parameters" >> ${log_path}

sed -i "/spark.executor.cores/ c spark.executor.cores ${spark_cores}" ${SPARK_HOME}/conf/spark-defaults.conf
sed -i "/spark.default.parallelism/ c spark.default.parallelism ${spark_parallelism}" ${SPARK_HOME}/conf/spark-defaults.conf
sed -i "/spark.rdd.compress/ c spark.rdd.compress ${rdd_compress}" ${SPARK_HOME}/conf/spark-defaults.conf
sed -i "/spark.shuffle.compress/ c spark.shuffle.compress ${shuffle_compress}" ${SPARK_HOME}/conf/spark-defaults.conf
sed -i "/spark.executor.cores/ c spark.executor.cores ${spark_cores}" ${SPARK_HOME}/conf/spark-defaults.conf

${TOOLS_SCRIPT_HOME}/mscp.sh ${TOOLS_SCRIPT_HOME}/passwd_config dir ${SPARK_HOME}/conf ${SPARK_HOME}

echo "Restart Spark platform"
echo "Restart Spark platform" >> ${log_path}

${SPARK_HOME}/sbin/stop-all.sh
${SPARK_HOME}/sbin/start-all.sh

echo "generating the sample"
echo "generating the sample" >> ${log_path}







