#!/bin/sh

function usage() {
	echo "Usage: $0 <type> <AppName> (<input_data> <exe_mem>(if you want to delete logs of one specific configuration))"
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
#executor_log_path="/home/hadoop/bryantchang/logs/sparklogs/executor_logs"
#gc_original_path="/home/hadoop/bryantchang/logs/sparklogs/gc_logs"
#gc_result_path="/home/hadoop/bryantchang/logs/sparklogs/gc_logs/gc_result"
#monitor_path="/home/hadoop/bryantchang/logs/sparklogs/monitor_logs"
#monitor_result_path="/home/hadoop/bryantchang/logs/sparklogs/monitor_logs/analyse_result"

type_no=$1
app_name=$2

if [[ ${type_no} = "all" ]]; then
	common_log_name="${app_name}*"
	gc_detail_name="detail_${app_name}*"
	gc_summary_name="summary_${app_name}*"

elif [[ ${type_no} = "one" ]]; then
	input_size=$3
	exe_mem=$4
    cores=`cat ${SPARK_HOME}/conf/spark-defaults.conf | grep 'spark.executor.cores' | cut -d ' ' -f 2`
    parallelism=`cat ${SPARK_HOME}/conf/spark-defaults.conf | grep 'spark.default.parallelism' | cut -d ' ' -f 2`
    rdd_compress=`cat ${SPARK_HOME}/conf/spark-defaults.conf | grep 'spark.rdd.compress' | cut -d ' ' -f 2`
    shuffle_compress=`cat ${SPARK_HOME}/conf/spark-defaults.conf | grep 'spark.shuffle.compress' | cut -d ' ' -f 2`
	common_log_name="${app_name}_${input_size}_${exe_mem}_${cores}_${parallelism}_${rdd_compress}_${shuffle_compress}.log"
	gc_detail_name="detail_${app_name}_${input_size}_${exe_mem}_${cores}_${parallelism}_${rdd_compress}_${shuffle_compress}.log"
	gc_summary_name="summary_${app_name}_${input_size}_${exe_mem}_${cores}_${parallelism}_${rdd_compress}_${shuffle_compress}.log"
fi

executor_log=${EXECUTOR_ORI_LOG_DIR}"/"${common_log_name}
monitor_log=${MONITOR_ORI_LOG_DIR}"/"${common_log_name}
monitor_result_log=${MONITOR_RES_LOG_DIR}"/"${common_log_name}
gc_comm_log=${GC_ORI_LOG_DIR}"/"${common_log_name}
gc_detail_log=${GC_RES_LOG_DIR}"/"${gc_detail_name}
gc_summary_log=${GC_RES_LOG_DIR}"/"${gc_summary_name}


rm -rf ${executor_log}
rm -rf ${monitor_log}
rm -rf ${monitor_result_log}
rm -rf ${gc_comm_log}
rm -rf ${gc_detail_log}
rm -rf ${gc_summary_log}

echo "finish"




