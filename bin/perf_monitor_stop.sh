#!/bin/bash
ps -ef | grep python | kill -9  `awk '{if($11=="1"){print $2}}'`