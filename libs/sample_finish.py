from smstool import *
import sys

conf_path = sys.argv[1]
appname = sys.argv[2]
input = sys.argv[3]


message = "Sample generate of appName:%s begin!\ninput:%sMB" % (appname, input)

sms(conf_path, message)
