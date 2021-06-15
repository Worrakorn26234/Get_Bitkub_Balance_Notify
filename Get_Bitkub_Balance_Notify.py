import hashlib
import hmac
import json
import requests
from songline import Sendline
import time
token = 'Your line token'
messenger = Sendline(token)

### API info ###

API_Host = 'https://api.bitkub.com'
API_KEY = 'Your API Key'
API_SECRET = b'Your API Secret'

##############################################################

def json_encode(data):
	return json.dumps(data, separators=(',', ':'), sort_keys=True)

def sign(data):
	j = json_encode(data)
	h = hmac.new(API_SECRET, msg=j.encode(), digestmod=hashlib.sha256)
	return h.hexdigest()

#################### ชุดคำสั่งเชื่อมต่อกับ API #################

while True:
        response = requests.get(API_Host + '/api/servertime')
        ts = int(response.text)

        response = requests.get(API_Host + '/api/market/ticker')
        result = response.json()
        
        header = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-BTK-APIKEY': API_KEY,
        }
        data = {
                'ts': ts,
        }
        signature = sign(data)
        data['sig'] = signature
        
################## Get XRP on last price ##############
        
        symbol = 'THB_XRP'
        XRP = result[symbol]
        last = XRP['last']
        
################### check balances #####################################

        response = requests.post(API_Host + '/api/market/balances', headers=header, data=json_encode(data))
        data = response.json()
        data = data['result']
        sym = 'XRP'
        price = data[sym]['available']
        price2 = float(price * last)

        print(messenger.sendtext('XRP '+ str(price2)))
        time.sleep(10)
