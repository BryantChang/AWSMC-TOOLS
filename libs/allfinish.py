from smstool import *
import sys
message="All finished !!"
# message="hello world"
conf_path = sys.argv[1]
sms(conf_path, message)