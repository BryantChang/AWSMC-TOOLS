import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from parseconf import *


conf_path = sys.argv[1]
log_name = sys.argv[2]
sample_log = sys.argv[3]


props = parse(conf_path)
sender = props.get('sender')
receiver = props.get('receiver')
username = props.get('username')
password = props.get('password')
server = props.get('smtpserver')

msgRoot = MIMEMultipart('related')
msgRoot['Subject'] = 'Sample Finished'

#构造附件
att = MIMEText(open(sample_log, 'rb').read(), 'base64', 'utf-8')
att["Content-Type"] = 'application/octet-stream'
att["Content-Disposition"] = 'attachment; filename=%s'%(log_name)
msgRoot.attach(att)


smtp = smtplib.SMTP()
smtp.connect(server)
smtp.login(username, password)
smtp.sendmail(sender, receiver, msgRoot.as_string())
smtp.quit()