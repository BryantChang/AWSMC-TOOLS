from smstool import *
import sys
message="The sample generating is completed, and the sample log has been mailed to your mail-box, please check!!"
# message="hello world"
conf_path = sys.argv[1]
sms(conf_path, message)