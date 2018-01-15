#!/bin/bash

function usage() {
    echo "Usage: $0"
}



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


begin_ts=`date +%Y-%m-%d-%H-%M-%S`
sample_dir_path=${SAMPLE_LOG}/sample_mem_${begin_ts}
log_path=${TMP_DIR}/${begin_ts}.log



if [[ -d ${sample_dir_path} ]]; then
    rm -rf ${sample_dir_path}
fi

echo "initializing" >> ${log_path}
echo "initializing"

mkdir -p ${TMP_DIR}
mkdir -p ${ERR_DIR}
mkdir -p ${EVENTLOG_DIR}
mkdir -p ${SAMPLE_LOG}
mkdir -p ${sample_dir_path}



echo "begin to generate"
tmp_no=0
while [[ ${tmp_no} -lt ${CATE_NO} ]]; do
    csv_name="regression_${tmp_no}.csv"
    csv_full_path=${sample_dir_path}/${csv_name}
    touch ${csv_full_path}
    log_str=""
    for metric in `cat ${CONF}/${METRICS_REGRESSION_CONF}`; do
        if [[ ${metric:0:1} = "#" ]]; then
            continue;
        fi
        log_str="${log_str},${metric}"
    done
    log_title=${log_str:1}

    tmp_no=`expr ${tmp_no} + 1`
    echo ${log_title} >> ${csv_full_path}
done



for app_line in `cat ${CONF}/apps_regression`; do
    app=`echo ${app_line} | cut -d '=' -f 1`
    type_no=`echo ${app_line} | cut -d '=' -f 2`
    for input_mem in `cat ${CONF}/input_mem_${app}`; do
        if [[ "${input_mem:0:1}" = "#" ]]; then
            continue;
        fi
        input=`echo ${input_mem} | cut -d '-' -f 1`
        init_mem=`echo ${input_mem} | cut -d '-' -f 2`
        echo "current input data size is ${input} M"
        echo "current input data size is ${input} M" >> ${log_path}
        echo "init mem is ${mem} m"
        echo "init mem is ${mem} m" >> ${log_path}
        ${bin}/sample_finish.sh ${CONF}/sysconf.properties ${app} ${input}
        #each parameter get one sample(the best memory configuration)
        for params in `cat ${CONF}/params_regression`; do
            if [[ "${params:0:1}" = "#" ]]; then
                continue;
            fi
            mem=${init_mem}
            spark_cores=`echo ${params} | cut -d '_' -f 1`
            block_size=`echo ${params} | cut -d '_' -f 2`
            spark_parallelism=`echo ${params} | cut -d '_' -f 3`
            rdd_compress=`echo ${params} | cut -d '_' -f 4`
            shuffle_compress=`echo ${params} | cut -d '_' -f 5`
            ${bin}/change_params.sh ${app} ${params} ${log_path}
            ${bin}/run_workload.sh ${app} ${input} ${mem} ${log_path}
            rec_count=`ssh ${SLAVE_HOST} cat ${GC_RES_LOG_DIR}/summary_${app}_${input}M_${mem}m_${spark_cores}_${spark_parallelism}_${rdd_compress}_${shuffle_compress}.log | grep ${app} | cut -f 7| sed s/[[:space:]]//g`
            gcsd=`ssh ${SLAVE_HOST} cat ${GC_RES_LOG_DIR}/summary_${app}_${input}M_${mem}m_${spark_cores}_${spark_parallelism}_${rdd_compress}_${shuffle_compress}.log | grep ${app} | cut -f 8| sed s/[[:space:]]//g`
            gcvc=`ssh ${SLAVE_HOST} cat ${GC_RES_LOG_DIR}/summary_${app}_${input}M_${mem}m_${spark_cores}_${spark_parallelism}_${rdd_compress}_${shuffle_compress}.log | grep ${app} | cut -f 9| sed s/[[:space:]]//g`
            if [[ ${rec_count} -eq 0 ]]; then
                if [[ ${gcsd} != "nan" ]]; then
                    if [[ ${gcvc} != "nan" ]]; then
                        ${bin}/generate_sample_regression.sh ${sample_dir_path}/regression_${type_no}.csv ${input}_${spark_cores}_${block_size}_${spark_parallelism}_${rdd_compress}_${shuffle_compress}_${mem}
                    fi
                fi
            fi
            mem=`expr ${mem} + ${MEM_STEP}`


        done

    done

done




#${bin}/sendmail.sh ${CONF}/sysconf.properties sample_pmc_${begin_ts}.csv ${sample_log_path}
${bin}/all_finish.sh ${CONF}/sysconf.properties


