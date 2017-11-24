#!/bin/bash
function usage(){
	echo "Usage: $0 <log_type>"
}

##argument check
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

log_type=$1

#if [[ $log_type = "gc" ]]; then
#elif [[ $log_type = "monitor" ]]

#
#cd ${log_dir}
#
#for file in `ls *.log`; do
#	echo "operating $file"
#	python $CURDIR/analyse_perf.py $file
#done
#
#echo "all done"









