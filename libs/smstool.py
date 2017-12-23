from twilio.rest import Client
from parseconf import *



def sms(conf_path, message):
    props = parse(conf_path)
    account = props.get('smsaccount')
    token = props.get('smstoken')
    from_no = props.get('smsfrom')
    to_no = props.get('smsto')
    client = Client(account, token)
    res = client.messages.create(to=to_no, from_=from_no, body=message)

