from smstool import *
import sys

conf_path = sys.argv[1]
appname = sys.argv[2]
total_sample = sys.argv[3]


message = "Sample generate of appName:%s finished!\nsampleCount:%s" % (appname, total_sample)

sms(conf_path, message)
