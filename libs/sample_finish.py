from smstool import *
import sys

conf_path = sys.argv[1]
appname = sys.argv[2]
mem = sys.argv[3]


message = "Sample generate of appName:%s finished!\nmem:%sM" % (appname, mem)

sms(conf_path, message)
